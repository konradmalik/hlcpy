import time
from pytest import approx
from hlcpy.hlc import HLC


def test_comparing():
    h1 = HLC()
    h2 = HLC.from_now()
    h1.set_time(time.time() + 1000)
    assert h2 == h2
    assert h2 < h1


def test_sync():
    h1 = HLC()
    h1.set_time(time.time() + 1000)
    h1.sync()
    _, logical = h1.tuple()
    # Logical must have ticked, because micros
    # should be in the future
    assert logical == 1


def test_merge():
    h1 = HLC()
    h1.set_time(time.time() + 3)
    original_micros, _ = h1.tuple()
    event = HLC()
    # event is 2 seconds in the future
    event.set_time(time.time() + 2)
    h1.merge(event)
    micros, logical = h1.tuple()
    assert logical == 1
    approx(micros, original_micros)
    time.sleep(3)
    # The wall clock catches up to HLC and resets logical
    h1.sync()
    micros, logical = h1.tuple()
    assert logical == 0
