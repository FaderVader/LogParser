from FileLoader import LoadLogsFromStructure
from StructureBuilder import StructureBuilder
from ParseLog import LogTrie
from FindLogsInFolder import GetListOfFiles

# config - if debug: './testSources/'   if run from shell: '../testSources/'
base_path = '../testSources/' 

# get list of log-files
logList = GetListOfFiles(base_path)

# build structured file-list, based on client-name and date
fileStructure = StructureBuilder.CreateFileStructure(logList)

# load all logs into structure
all_files = LoadLogsFromStructure(fileStructure, base_path)

# transform all log-files in trie-structure
trie = LogTrie()
for client in fileStructure:
    for log in fileStructure[client]:
        log_file = all_files[client][log]
        value = LogTrie.Terminator(client, log, None)
        trie.addLog(log_file, value)


# POC - searching trie
log_entry_1 = trie.findWord('Application')
log_entry_2 = trie.findWord('[WRN]')

# POC - show hits
for pointer in log_entry_2:
    actual_line = all_files[pointer.client][pointer.date][pointer.linenumber]
    print(f'Client: {pointer.client}, date: {pointer.date}, line: {pointer.linenumber}')
    print(actual_line.GetPayLoad())

print('done')