from LogLine import LogLine

def loadOneLogfile(path):
    allLines = []
    with open(path) as file:
        for line in file:
            allLines.append(LogLine(line))
    return allLines


def LoadAllLogs(logList):
    logs = []
    basePath = './testSources/' # run = '../'    debug = './'
    extension = '.log'

    # load all logs
    for logfile in logList:
        logs.append(loadOneLogfile(basePath + logfile + extension))
    return logs


def SearchLogsForPhrase(searchPhrase, logs):
    hits = []
    for log in logs:
        for logLine in log:
            if logLine.GetPayLoad().find(searchPhrase) > -1:
                hits.append((logLine.GetTimeStamp(), logLine.GetPayLoad())) # store as tuple
    return hits


def executeSearch(searchPhrase, messageLength, logList):
    allLogs = LoadAllLogs(logList)
    hits = SearchLogsForPhrase(searchPhrase, allLogs)

    print(f'Matches found: {len(hits)}')

    for hit in hits:
        print(f'time:{hit[0]} - message: {hit[1][0: messageLength]}')