from logLoader import LoadAllLogs, SearchLogsForPhrase, LoadLogsFromStructure
from StructureBuilder import StructureBuilder
from parseLog import LogTrie
from findLogs import getListOfFiles

# get list of log-files
logList = getListOfFiles()

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
    client = pointer[0]
    date = pointer[1]
    line = pointer[2]
    actual_line = all_files[client][date][line]
    print(f'Client: {client} - date: {date} - line: {line}')
    print(actual_line.lineElements[1])

print('end')
