import time
import pytest
from hlcpy import HLC


def test_too_large():
    with pytest.raises(ValueError):
        HLC(2 ** 43 * 1e6, 0)
    HLC((2 ** 43 - 1) * 1e6, 0)

    with pytest.raises(ValueError):
        HLC(2 ** 43 * 1e6 - 1, 2 ** 16)
    HLC(2, 2 ** 16 - 1)


def test_bin():
    h1 = HLC(int(3e6), 2)
    h2 = HLC.from_bytes(h1.to_bytes())
    assert h2 == h1

    # nanos are not supported in binary representation
    # so reconstructed element should be later than the former
    h1 = HLC(int(3e5), 4)
    h2 = HLC.from_bytes(h1.to_bytes())
    assert h2 > h1


def test_str():
    h1 = HLC()
    h1.set_nanos(int(time.time_ns() + 10e9))
    h2 = HLC.from_str(str(h1))
    assert h2 == h1

    h1 = HLC()
    h1._set(123, 4)
    h2 = HLC.from_str(str(h1))
    assert str(h1).split("_")[1] == "4"
    assert h2 == h1

    h1 = HLC.from_str("2020-01-01T00:00:00Z")
    assert h1.nanos == 1577836800000000000


def test_compare():
    h1 = HLC()
    h2 = HLC()
    h1.set_nanos(int(time.time_ns() + 10e9))
    assert h2 == h2
    assert h2 < h1


def test_sync():
    future_nanos = int(time.time_ns() + 10e9)
    h1 = HLC()
    h1.set_nanos(future_nanos)
    h1.sync()
    nanos, logical = h1.tuple()
    # Logical must have ticked, because nanos
    # should be in the future
    assert logical == 1
    assert nanos == future_nanos


def test_merge():
    wall_nanos = time.time_ns()
    h1 = HLC()
    h1.set_nanos(wall_nanos)
    original_nanos, _ = h1.tuple()
    event = HLC()
    # event is 10 seconds in the future
    event.set_nanos(int(wall_nanos + 3e9))

    h1.merge(event)
    nanos, logical = h1.tuple()
    assert logical == 1

    h1.merge(event)
    nanos, logical = h1.tuple()
    assert logical == 2

    h1.merge(event)
    nanos, logical = h1.tuple()
    assert logical == 3
    assert original_nanos == wall_nanos
    assert nanos > wall_nanos + 1000

    # The wall clock catches up to HLC and resets logical
    time.sleep(4)
    h1.sync()
    _, logical = h1.tuple()
    assert logical == 0
