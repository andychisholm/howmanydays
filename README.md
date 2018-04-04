howmanydays
===========

### Setup

```
unzip howmanydays.zip -d howmanydays
cd howmanydays
```

### Run the CLI
```
python3 cli.py <from_date> <to_date>
```

### Run the tests
```
python3 -m unittest discover
```

### The unzipped folder is also a python module, so you may use the API

```python
from howmanydays.dates import to_date, get_days_between

a = to_date(2, 6, 1983)
b = to_date(22, 6, 1983)
get_days_between(a, b) == 19  # returns True
```

