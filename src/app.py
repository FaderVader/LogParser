from QueryParser import QueryParser
from collections import namedtuple

queryParser = QueryParser()
# q = '{"Find": ["setupsession", "running"], "Between": ["2020-10-06-0:0:0.0", "2020-10-06-23:59:59.9"], "Client": "TX82564"}'
# q2 = '{"Find": ["setupsession", "completed"], "Between": ["2020-10-06-0:0:0.0", "2020-10-06-23:59:59.9"], "Client": "TX82564"}'
# queryParser.Parse(q)
# print('-------')
# queryParser.Parse(q2)

# q = '{"Find": ["setupsession", "running"], "Between": ["2020-10-01-0:0:0.0", "2020-10-02-23:59:59.9"], "Client": "TX82564", "Sort": 1}'

Query = namedtuple("Query", "StartEnd Find Between Client Sort")


def query(StartEnd=None, Find=None, Between=None, Client=None, Sort=None):
    return Query(StartEnd, Find, Between, Client, Sort)


q = query(StartEnd=[["setupsession", "running"], ["setupsession", "completed"]])
# q = query(Find=["setupsession", "running"], Client="AX82017", Between=["2020-10-01-0:0:0.0", "2020-10-02-23:59:59.9"], Sort=1)

result = queryParser.Parse(q)

print('done')
