from QueryParser import QueryParser

queryParser = QueryParser()

# q = {"STARTEND": [["SendEvent", "DaletService", "Waiting"], ["SendEvent", "DaletService", "Success"]], "BETWEEN": ["2020-10-01-12:0:0.0", "2020-10-01-23:59:59.9"], "SORT":True}
# q = {"STARTEND": [["setupsession", "running"], ["setupsession", "completed"]], "CLIENT": "TX84402"}  # 
# q = {"FIND": ["setupsession", "running"], "SORT": True}  # 
q = {"STARTEND": [["setupsession", "running"], ["setupsession", "completed"]], "BETWEEN": ["2020-10-01-12:0:0.0", "2020-10-01-23:59:59.9"], "SHOWSTATS": 2}

result = queryParser.Parse(q)

print('Query complete.')
