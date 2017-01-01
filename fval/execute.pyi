# -*- coding: utf-8 -*-
import threading
from typing import List, Dict, Optional, AnyStr


class Counter(object):
    def __init__(self, start: Optional[int] = 0) -> None:
        self.lock = threading.Lock()
        self.value = start

    def increment(self): pass


def _check_worker(cmdline_args: Dict, config: Dict, rel_unit_path: AnyStr, check_name: AnyStr,
                  check_args: List, unit_file_content: AnyStr,
                  error_counter: Counter): pass


def execute_plan(plan: List, config: Dict) -> int: pass
