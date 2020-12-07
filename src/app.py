from QueryParser import QueryParser
from Types import QuerySyntax as QuerySyntax


# def query(StartEnd=None, Find=None, Between=None, Client=None, Sort=None, ShowStats=None):
#     return QuerySyntax(StartEnd, Find, Between, Client, Sort, ShowStats)


queryParser = QueryParser()

# q = query(StartEnd=[["setupsession", "running"], ["setupsession", "completed"]], Between=["2020-10-01-12:0:0.0", "2020-10-01-23:59:59.9"], Sort=1)
# q = query(Find=["setupsession", "running"], Client="AX82017", Between=["2020-10-01-0:0:0.0", "2020-10-02-23:59:59.9"], Sort=1)
# q = query(StartEnd=[["SendEvent", "DaletService", "Waiting"], ["SendEvent", "DaletService", "Success"]], Sort=1, Client="TX84402")    
# q = query(StartEnd=[["SendEvent", "DaletService", "Waiting"], ["SendEvent", "DaletService", "Success"]], Sort=1, ShowStats=1, Client="TX84402")    
# q = query(Find=["@GetDaletServiceIsInstalled"], Sort=1)
# q = query(Find=["found"], Sort=1) 

# q = {"StartEnd": [["setupsession", "running"], ["setupsession", "completed"]], "Client": "TX84402"}  # 
q = {"Find": ["setupsession", "running"], "ShowStats": 5, "Sort": True}  # 
# q = {"StartEnd": [["setupsession", "running"], ["setupsession", "completed"]], "Between": ["2020-10-01-12:0:0.0", "2020-10-01-23:59:59.9"]}

result = queryParser.Parse(q)

print('Query complete.')
