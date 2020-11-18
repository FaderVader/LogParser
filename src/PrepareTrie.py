from FileLoader import LoadLogsFromStructure
from StructureBuilder import StructureBuilder
from Tries import LogTrie
from FindLogsInFolder import GetListOfFiles

class PrepareTrie:
    def __init__(self, base_path = './testSources/'):
        self.base_path = base_path     # config - if debug: './testSources/'   if run from shell: '../testSources/'
        self.logList = GetListOfFiles(self.base_path)
        self.fileStructure = StructureBuilder.CreateFileStructure(self.logList)
        self.all_files = LoadLogsFromStructure(self.fileStructure, self.base_path)
        self.log_trie = None


    def LoadLogs(self):        
        # transform all log-files in trie-structure
        trie = LogTrie()
        for client in self.fileStructure:
            for log in self.fileStructure[client]:
                log_file = self.all_files[client][log]
                value = LogTrie.Terminator(client, log, None)
                trie.addLog(log_file, value)

        return trie

    def GetLogTrie(self):
        if self.log_trie is None:
            self.log_trie = self.LoadLogs()
        return self.log_trie

    def GetStructuredLogs(self):
        return self.all_files
