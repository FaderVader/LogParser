from logLoader import LoadAllLogs, SearchLogsForPhrase, LoadLogsFromStructure
from StructureBuilder import StructureBuilder
from parseLog import LogTrie


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

fileStructure = StructureBuilder.CreateFileStructure(logList)
all_files = LoadLogsFromStructure(fileStructure)
one_line = all_files['AX82017']['20201004'][2]
one_file = all_files['AX82017']['20201004']

trie = LogTrie()

for client in fileStructure:
    for log in fileStructure[client]:
        log_file = all_files[client][log]
        trie.addLog(log_file, (client, log))
# trie.addLog(one_file, ('AX82017', '20201004'))
log_entry_1 = trie.findWord('Application')
log_entry_2 = trie.findWord('[WRN]')

for pointer in log_entry_2:
    client = pointer[0]
    date = pointer[1]
    line = pointer[2]
    actual_line = all_files[client][date][line]
    print(f'Client: {client} - date: {date} - line: {line}')
    print(actual_line.lineElements[1])

print('pause')



# tests
for filename in LoadLogsFromStructure(fileStructure):
    print(filename)

fileStructure['AX82017']['20200930'] = [(10, '10-lines'), (20, '20-lines'), (30, '30-lines')]
test = fileStructure['AX82017']['20200930'][0] 

for client in fileStructure:
    for logfile in fileStructure[client]:
        print(f'{client}: \t{logfile}')

print('end')
