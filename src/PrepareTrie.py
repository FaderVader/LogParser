from FileLoader import LoadLogsFromStructure
from StructureBuilder import StructureBuilder
from Tries import LogTrie
from FindLogsInFolder import GetListOfFiles


class PrepareTrie:
    def __init__(self, base_path='./testSources/'):
        self.base_path = base_path     # config - if debug: './testSources/'   if run from shell: '../testSources/'
        self.logList = GetListOfFiles(self.base_path)
        self.fileStructure = StructureBuilder.CreateFileStructure(self.logList)
        self.all_files = LoadLogsFromStructure(self.fileStructure, self.base_path)
        self.log_trie = None

    def loadLogs(self):
        """
        Transform all log-files into trie-structure:
        [client][file][linenumber]
        """
        trie = LogTrie()
        for client in self.fileStructure:
            for log in self.fileStructure[client]:
                log_file = self.all_files[client][log]
                value = LogTrie.Terminator(client, log, None)
                trie.AddLog(log_file, value)
        self.log_trie = trie

    def GetLogTrie(self):
        """
        Get trie from all logs
        """
        if self.log_trie is None:
            self.loadLogs()
        return self.log_trie

    def GetStructuredLogs(self):
        """
        Get all logs as structured object: [client][file][linenumber]
        """
        return self.all_files
