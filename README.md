# Hybrid Logical Clock

Python implementation of Hybrid Logical Clock.

Requires Python version >= 3.7.

You can install this package from [PyPI](https://pypi.org/project/hlcpy/):

```bash
$ pip install hlcpy
```

## Exemplary usage

```python
import hlcpy

# BASIC USAGE
# Instantiate HLC
c = hlcpy.HLC()

# specify starting nanos and logical time
c = hlcpy.HLC(nanos=123, logical=0)

# create from current time
c = hlcpy.HLC.from_now()

# create from iso8601 time
c = hlcpy.HLC.from_str('2020-01-01T00:00:00Z')

# string representation of HLC
print(str(c))
#>>> 2020-01-01T00:00:00.000000000Z_0

# create from string representation
c1 = hlcpy.HLC.from_str(str(c))

# refresh the clock
c.sync()

# supports comparison
print(c > c1)
#>>> True

# merge two events
c.merge(c1)
print(c)
#>>> 2021-04-24T18:42:47.001864924Z_0

# merge event that occured in the future to see the logical tick
import time
future = hlcpy.HLC(nanos=int(time.time_ns() + 3e9))
c.merge(future)
print(c)
#>>> 2021-04-24T18:42:50.001891328Z_1

# More examples - see tests/unit/test_hlc.py

```

## Credits

Based on:
https://www.cse.buffalo.edu/tech-reports/2014-04.pdf

Inspired by:

- https://www.youtube.com/watch?v=iEFcmfmdh2w
- https://github.com/adsharma/hlcpy (based on but heavily rewritten)
- https://bartoszsypytkowski.com/hybrid-logical-clocks/
