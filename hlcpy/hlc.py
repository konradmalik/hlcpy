from __future__ import annotations
import threading
import time
from datetime import datetime
from typing import Union


def synchronized(fn):
    """Synchronization for object methods using self.lock"""

    def wrapper(self, *args, **kwargs):
        with self.lock:
            return fn(self, *args, **kwargs)
    return wrapper


class HLC:
    _usec_per_sec = 1e6
    _k_logical_bits = 12
    _k_logical_mask = (1 << _k_logical_bits) - 1

    @staticmethod
    def from_now():
        hlc = HLC()
        hlc.set_time(time.time())
        return hlc

    def __init__(self, micros: int = 0, logical: int = 0):
        self.format = "%s.%f"
        self.lock = threading.Lock()
        self._set(micros, logical)

    def set_time(self, t: Union[int, float]):
        "Takes unix epoch seconds"
        now = int(t * self._usec_per_sec)
        self._set(now, 0)

    def from_state(self, state: int):
        self._state = state

    def _set(self, micros, logical):
        self._state = (micros << self._k_logical_bits) | logical

    def set_format(self, fmt: str):
        "Used by __str__ method"
        self.format = fmt

    def tuple(self):
        """Returns a tuple of <microseconds since epoch, logical clock>"""
        return self._state >> self._k_logical_bits, self._state & self._k_logical_mask

    def __str__(self):
        fmt = self.format
        physical_time, logical_time = self.tuple()
        physical_time = physical_time / self._usec_per_sec
        physical_time = datetime.fromtimestamp(physical_time)
        return '{} {}'.format(physical_time.strftime(fmt), logical_time)

    def __eq__(self, other):
        return self.tuple() == other.tuple()

    def __lt__(self, other):
        return self.tuple() < other.tuple()

    def __sub__(self, other):
        "Ignores logical. Difference in microsecs"
        micros1, _ = self.tuple()
        micros2, _ = other.tuple()
        return micros1 - micros2

    @synchronized
    def sync(self):
        "Used to refresh the clock"
        wall = HLC.from_now()
        cmicros, clogical = self.tuple()
        wmicros, _ = wall.tuple()
        micros = max(cmicros, wmicros)
        if micros == cmicros:
            logical = clogical + 1
        else:
            logical = 0
        self._set(micros, logical)

    @synchronized
    def merge(self, event: HLC):
        "To be used on receiving an event"
        cmicros, clogical = self.tuple()
        emicros, elogical = event.tuple()
        wall = HLC.from_now()
        wmicros, _ = wall.tuple()
        micros = max(cmicros, emicros, wmicros)
        if micros == emicros and micros == cmicros:
            logical = max(clogical, elogical) + 1
        elif micros == cmicros:
            logical = clogical + 1
        elif micros == emicros:
            logical = elogical + 1
        else:
            logical = 0
        self._set(micros, logical)
