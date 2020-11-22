from QueryParser import QueryParser

queryParser = QueryParser()
q = '{"find": ["setupsession", "running"], "between": ["2020-10-06-0:0:0.0", "2020-10-06-23:59:59.9"], "client": "TX82564"}'
q2 = '{"find": ["setupsession", "completed"], "between": ["2020-10-06-0:0:0.0", "2020-10-06-23:59:59.9"], "client": "TX82564"}'
queryParser.parse(q)
print('-------')
queryParser.parse(q2)

print('done')
