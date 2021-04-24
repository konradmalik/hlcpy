from datetime import datetime, timezone
from iso8601 import parse_date


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
    dt = datetime.fromtimestamp(nanos // nanos_order, tz=timezone.utc)
    return "{}.{:09.0f}Z".format(dt.strftime("%Y-%m-%dT%H:%M:%S"), nanos % nanos_order)


def iso8601_to_nanos(s: str) -> int:
    """
    Converts iso8601 string to nanoseconds
    Supports nanosecods and does not trim/round them
    """
    # this if-else branch handles potential nanoseconds
    if "." in s:
        last_dot = s.rindex(".")
        zone_sep = s.index("Z") if "Z" in s else s.index("+")
        decimals_str = s[last_dot:zone_sep]
        s_clean = s.replace(decimals_str, "")
    else:
        s_clean = s
        decimals_str = ""
    dt = parse_date(s_clean)
    # rounding discards nothing, just to int
    seconds = round(dt.timestamp())
    decimals_str = decimals_str.replace(".", "").ljust(9, "0")
    full_str = str(seconds) + decimals_str
    return int(full_str)
