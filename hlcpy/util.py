from datetime import datetime, timezone
import numpy


def synchronized(fn):
    """Synchronization for object methods using self.lock"""

    def wrapper(self, *args, **kwargs):
        with self.lock:
            return fn(self, *args, **kwargs)
    return wrapper


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def nanos_to_iso8601(nanos: int) -> str:
    nanos_order = int(1e9)
    dt = datetime.fromtimestamp(nanos // nanos_order)
    return '{}.{:09.0f}Z'.format(
        dt.strftime('%Y-%m-%dT%H:%M:%S'),
        nanos % nanos_order)


def iso8601_to_nanos(s: str) -> int:
    dt = numpy.datetime64(s)
    return dt.astype('datetime64[ns]').astype('int')
