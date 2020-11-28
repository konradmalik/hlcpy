import time
from hlcpy import HLC


def test_str():
    h1 = HLC()
    h1.set_nanos(time.time_ns() + 10e9)
    h2 = HLC.from_str(str(h1))
    assert h2 == h1

    h1 = HLC()
    h1._set(123, 4)
    h2 = HLC.from_str(str(h1))
    assert str(h1).split("_")[1] == '4'
    assert h2 == h1


def test_compare():
    h1 = HLC()
    h2 = HLC()
    h1.set_nanos(time.time_ns() + 10e9)
    assert h2 == h2
    assert h2 < h1


def test_sync():
    future_nanos = time.time_ns() + 10e9
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
    event.set_nanos(wall_nanos + 3e9)

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
