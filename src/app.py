from QueryParser import QueryParser

queryParser = QueryParser()
q = '{"Find": ["setupsession", "running"], "Between": ["2020-10-06-0:0:0.0", "2020-10-06-23:59:59.9"], "Client": "TX82564"}'
q2 = '{"Find": ["setupsession", "completed"], "Between": ["2020-10-06-0:0:0.0", "2020-10-06-23:59:59.9"], "Client": "TX82564"}'
queryParser.Parse(q)
print('-------')
queryParser.Parse(q2)

print('done')
