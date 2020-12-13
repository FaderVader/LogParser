from Loader import Loader
from Tries import LogTrie
from Types import Terminator as Terminator


class PrepareTrie:
    def __init__(self):
        loader = Loader()
        self.fileStructure = loader.GetStructure()
        self.all_files = loader.GetStructuredLogs()
        self.log_trie = None

    def buildTrie(self):
        """
        Transform all log-files into trie-structure:
        [client][file][linenumber]
        """
        trie = LogTrie()
        for client in self.fileStructure:
            for log in self.fileStructure[client]:
                log_file = self.all_files[client][log]
                terminator = Terminator(client, log, None, None)
                trie.AddLog(log_file, terminator)
        self.log_trie = trie

    def GetLogTrie(self):
        """
        Get trie from all logs
        """
        if self.log_trie is None:
            self.buildTrie()
        return self.log_trie

    def GetStructuredLogs(self):
        """
        Get all logs as structured object: [client][file][linenumber]
        """
        return self.all_files
