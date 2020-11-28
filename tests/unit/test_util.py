from hlcpy import util


def test_nanos_to_str():
    nanos = 1606141759 * 1e9
    assert util.nanos_to_iso8601(nanos) == '2020-11-23T14:29:19.000000000Z'
    nanos = 1606141759000000001
    assert util.nanos_to_iso8601(nanos) == '2020-11-23T14:29:19.000000001Z'
    nanos = 1606141759001001001
    assert util.nanos_to_iso8601(nanos) == '2020-11-23T14:29:19.001001001Z'


def test_str_to_nanos():
    s = '2020-11-23T14:29:19.000000001Z'
    nanos = 1606141759000000001
    assert util.iso8601_to_nanos(s) == nanos

    s = '2020-11-23T14:29:19.000000000Z'
    nanos = 1606141759 * 1e9
    assert util.iso8601_to_nanos(s) == nanos

    s = '2020-11-23T14:29:19.001001001Z'
    nanos = 1606141759001001001
    assert util.iso8601_to_nanos(s) == nanos

    s = '2020-11-23T14:29:19.0011Z'
    nanos = 1606141759001100000
    assert util.iso8601_to_nanos(s) == nanos
