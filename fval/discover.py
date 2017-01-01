# -*- coding: utf-8 -*-
import os
from collections import OrderedDict
from os.path import splitext, isfile


def walk_path(path, depth=None):
    """ Yield the specified path with the dirs and files it contains.

    Args:
        path: The path to start walking from
        depth: Number of levels down to recurse

    Yields:
        A 3-tuple (root, dirs, files)

    """

    path = path.rstrip(os.path.sep)
    assert os.path.isdir(path)
    num_sep = path.count(os.path.sep)
    for root, dirs, files in os.walk(path):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if depth and depth >= 0 and num_sep + depth <= num_sep_this:
            del dirs[:]


def discover(config=None):
    """ Find fval files

    Args:
        config: Options provided in configuration file and
                through command line options

    Returns:
        tuple: A list of discovered paths and a list
               of redundant/orphan fval files

    """
    logger = config['logger']
    discovered = list()
    orphaned = list()

    config_exclusions = config.get('exclusions')
    path_exclusions = config_exclusions.get('paths')
    dir_exclusions = config_exclusions.get('dirs')

    # Walk through specified path, looking for files to evaluate
    for current_path, dirs, file_list in walk_path(config.get('path'), config.get('depth')):
        # SKIP WHOLE DIR IF IT EXISTS IN PATH EXCLUSIONS
        if path_exclusions and current_path in path_exclusions:
            logger.debug('Skipping path: {0} - due to path exclusion'.format(current_path))
            del dirs[:]
            continue

        # Skip whole dir if it is listed in dir exclusions
        if dir_exclusions:
            current_dir = os.path.basename(
                os.path.normpath(current_path))
            if current_dir in dir_exclusions:
                logger.debug('Skipping path: {0} - due to dir exclusion'.format(current_path))
                del dirs[:]
                continue

        dir_fval_found = False
        # If there's a file called .fval in the dir, then
        # all non .fval files are in scope
        if os.path.isfile(os.path.join(current_path, '.fval')):
            dir_fval_found = True
        for filename in file_list:
            discovery_entry = OrderedDict()

            # Excluding files with these excluded extensions
            if splitext(filename)[1] not in config_exclusions:

                # 1 REVERSE LOOKUP
                # If file ends in .fval but it isn't a dir fval file,
                # then it relates to a unit file
                if filename.endswith('.fval') and not filename == '.fval':
                    # Look for file it refers to
                    fval_file = filename
                    # TODO: Messy
                    possible_unit_file_paths = (os.path.join(current_path,
                                                             fval_file[:-5]),
                                                os.path.join(current_path,
                                                             fval_file[1:-5]))
                    found_unit_file = False
                    for possible_unit_file_path in possible_unit_file_paths:
                        if isfile(possible_unit_file_path):
                            discovery_entry['unit_path'] = os.path.join(
                                possible_unit_file_path)
                            discovery_entry['fval_path'] = os.path.join(
                                current_path, filename)
                            found_unit_file = True
                    if not found_unit_file:
                        orphaned.append(os.path.join(
                            current_path, filename))
                # 2 FORWARD LOOKUP
                # If .fval in dir and it's not a unit specific fval file...
                if dir_fval_found and not filename == '.fval' and \
                        not filename.endswith('.fval'):
                    discovery_entry['dir_fval_path'] = os.path.join(
                        current_path, '.fval')
                    discovery_entry['unit_path'] = os.path.join(
                        current_path, filename)

                # 3 USER SPECIFIED '-all', SO BRING THEM ALL IN,
                # EVEN IF NO .fval FILE IN PATH
                if config.get('all') and not filename == '.fval' and \
                        not filename.endswith('.fval'):
                    discovery_entry['unit_path'] = os.path.join(
                        current_path, filename)

            # At this point, we may have discovered a file (unit_path) that's previously been associated
            # with a file specific or dir specific fval file, so need to ensure we capture both...

            # Discovered a new entry
            if discovery_entry:
                # Loop through previously discovered
                for existing_entry in discovered:
                    # Check if there are any with an identical unit path
                    if existing_entry.get('unit_path') == \
                            discovery_entry.get('unit_path'):
                        # Create a new dict (a copy of the newly discovered entry)
                        updated_entries = discovery_entry.copy()
                        # Update the newly discovered entry from the existing entry
                        updated_entries.update(existing_entry)
                        # Remove existing this entry from the 'discovered' list
                        discovered[:] = [d for d in discovered if
                                         d.get('unit_path') !=
                                         discovery_entry['unit_path']]
                        # Add this new merged entry
                        discovered.append(updated_entries)
                        break
                # If this doesn't match an existing entry, just append it to the list
                else:
                    discovered.append(discovery_entry)
    for d in discovered:
        logger.debug('Discovered Unit: {0} fval: {1}'.format(d.get('unit_path'), d.get('dir_fval_path')))
    return discovered, orphaned
