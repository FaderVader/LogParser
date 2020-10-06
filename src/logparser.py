from logLoader import logLoader, LogLine

def ParseLogs(searchTerm, logList):
    logs = []
    basePath = '../testSources/' # run = '../'    debug = './'
    extension = '.log'

    # load all logs
    for logfile in logList:
        logs.append(logLoader(basePath + logfile + extension))

    # search all logs
    hits = []
    for log in logs:
        for logLine in log:
            if logLine.GetPayLoad().find(searchTerm) > -1:
                hits.append((logLine.GetTimeStamp(), logLine.GetPayLoad())) # store as tuple
    return hits


def executeSearch(searchPhrase, messageLength):
    hits = ParseLogs(searchPhrase, logList)

    print(f'Matches found: {len(hits)}')

    for hit in hits:
        print(f'time:{hit[0]} - message: {hit[1][0: messageLength]}')


logList = ['GalaxySiteSelector-JAKOB-LAPTOP-20200904',
'GalaxySiteSelector-JAKOB-LAPTOP-20200905',
'GalaxySiteSelector-JAKOB-LAPTOP-20200918',
'GalaxySiteSelector-JAKOB-LAPTOP-20200919',
'GalaxySiteSelector-JAKOB-LAPTOP-20200909',]

executeSearch('WRN', 50)