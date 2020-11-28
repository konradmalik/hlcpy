from __future__ import annotations
import threading
import time
from hlcpy.util import synchronized, nanos_to_iso8601, iso8601_to_nanos


class HLC:
    def __init__(self, nanos: int = 0, logical: int = 0):
        self.lock = threading.Lock()
        self._set(nanos, logical)

    @staticmethod
    def from_now():
        return HLC(nanos=time.time_ns())

    @classmethod
    def from_str(cls, s: str) -> HLC:
        spl = s.split('_')
        nanos = iso8601_to_nanos(spl[0])
        logical = int(spl[1]) if len(spl) > 1 else 0
        return cls(nanos, logical)

    @property
    def nanos(self) -> int:
        return self._nanos

    @property
    def logical(self) -> int:
        return self._logical

    def set_nanos(self, nanos: int):
        "Takes unix epoch nanoseconds"
        self._set(nanos, 0)

    def _set(self, nanos: int, logical: int):
        self._nanos = nanos
        self._logical = logical

    def tuple(self):
        """Returns a tuple of <nanoseconds since unix epoch, logical clock>"""
        return self.nanos, self.logical

    def __str__(self) -> str:
        return '{}_{}'.format(nanos_to_iso8601(self.nanos), self.logical)

    def __repr__(self) -> str:
        return 'HLC(nanos={},logical={})'.format(self.nanos, self.logical)

    def __eq__(self, other) -> bool:
        return self.tuple() == other.tuple()

    def __lt__(self, other) -> bool:
        return self.tuple() < other.tuple()

    @synchronized
    def sync(self):
        "Used to refresh the clock"
        wall = HLC.from_now()
        cnanos, clogical = self.tuple()
        wnanos, _ = wall.tuple()
        nanos = max(cnanos, wnanos)
        if nanos == cnanos:
            logical = clogical + 1
        else:
            logical = 0
        self._set(nanos, logical)

    @synchronized
    def merge(self, event: HLC, sync: bool = True):
        "To be used on receiving an event"
        cnanos, clogical = self.tuple()
        enanos, elogical = event.tuple()
        wall = HLC.from_now()
        wnanos, _ = wall.tuple()
        nanos = max(cnanos, enanos, wnanos)
        if nanos == enanos and nanos == cnanos:
            logical = max(clogical, elogical) + 1
        elif nanos == cnanos:
            logical = clogical + 1
        elif nanos == enanos:
            logical = elogical + 1
        else:
            logical = 0
        self._set(nanos, logical)
