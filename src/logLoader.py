from LogLine import LogLine

def loadOneLogfile(path):
    allLines = []
    with open(path) as file:
        for line in file:
            allLines.append(LogLine(line))
    return allLines


def LoadLogsFromStructure(fileStructure):
    base_path = './testSources/'  # if debug: './testSources/'   if run from shell: '../testSources/'
    app_name = 'GalaxySiteSelector'
    file_ext = '.log'

    for client in fileStructure:
        for logfile in fileStructure[client]:
            complete_filename = f'{app_name}-{client}-{logfile}{file_ext}'
            file_contents = loadOneLogfile(f'{base_path}{complete_filename}')
            fileStructure[client][logfile] = file_contents 
    return fileStructure


# deprecated
def LoadAllLogs(logList):
    logs = []
    basePath = './testSources/' # run = '../'    debug = './'
    extension = '.log'

    # load all logs
    for logfile in logList:

        # log-lines should eventually be stored by {clientname: {filename: [loglines ]}}
        logs.append(loadOneLogfile(basePath + logfile + extension))
    return logs

# deprecated
def SearchLogsForPhrase(searchPhrase, logs):
    hits = []
    for log in logs:
        for logLine in log:
            if logLine.GetPayLoad().find(searchPhrase) > -1:
                hits.append((logLine.GetTimeStamp(), logLine.GetPayLoad())) # store as tuple
    return hits