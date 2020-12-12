"https://www.askpython.com/python-modules/python-inspect-module"

import inspect 
from Query import Query

methods = []
all_members = inspect.getmembers(Query, inspect.isfunction)
for a, b in all_members:
    if not a.startswith('__'):
        methods.append({a, b})

test = methods