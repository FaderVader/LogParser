from logLoader import LoadAllLogs, SearchLogsForPhrase

def executeSearch(searchPhrase, messageLength, logList):
    allLogs = LoadAllLogs(logList)
    hits = SearchLogsForPhrase(searchPhrase, allLogs)

    for hit in hits:
        print(f'time:{hit[0]} - message: {hit[1][0: messageLength]}')
        
    print(f'Matches found: {len(hits)}')

logList = ['GalaxySiteSelector-AX82017-20200929',
'GalaxySiteSelector-AX82017-20200930',
'GalaxySiteSelector-AX82017-20201001',
'GalaxySiteSelector-AX82017-20201002',
'GalaxySiteSelector-AX82017-20201004',
'GalaxySiteSelector-AX82017-20201005',
'GalaxySiteSelector-AX82017-20201006',
'GalaxySiteSelector-JAKOB-LAPTOP-20200904',
'GalaxySiteSelector-JAKOB-LAPTOP-20200905',
'GalaxySiteSelector-JAKOB-LAPTOP-20200909',
'GalaxySiteSelector-JAKOB-LAPTOP-20200918',
'GalaxySiteSelector-JAKOB-LAPTOP-20200919']

executeSearch('WRN', 50, logList)