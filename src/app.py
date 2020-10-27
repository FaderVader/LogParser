from FileLoader import LoadLogsFromStructure
from StructureBuilder import StructureBuilder
from ParseLog import LogTrie
from FindLogsInFolder import GetListOfFiles

# get list of log-files
logList = GetListOfFiles()

# build structured file-list, based on client-name and date
fileStructure = StructureBuilder.CreateFileStructure(logList)

# load all logs into structure
all_files = LoadLogsFromStructure(fileStructure)

trie = LogTrie()

for client in fileStructure:
    for log in fileStructure[client]:
        log_file = all_files[client][log]
        trie.addLog(log_file, (client, log))

log_entry_1 = trie.findWord('Application')
log_entry_2 = trie.findWord('[WRN]')

for pointer in log_entry_1:
    client, date, line = pointer[0], pointer[1], pointer[2]
    actual_line = all_files[client][date][line]
    print(f'Client: {client} - date: {date} - line: {line}')
    print(actual_line.lineElements[1])

print('end')
