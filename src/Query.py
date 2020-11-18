"""
    Build generic methods for querying trie.
"""
from Tries import SearchTrie

class Query:
    def __init__(self, log_trie, all_files):
        self.log_trie = log_trie
        self.search_trie = SearchTrie()
        self.all_files = all_files
        self.result = None

    def _buildSearchTrie(self, *args):
        for arg in args:            
            # get pointer to matches for every word
            word = arg.lower()
            matches = self.log_trie.findWord(word) 
            
            # build trie of pointers, terminator indicates number of hits
            for match in matches:
                self.search_trie.addPointer(match)

    def mustContainWords(self, *args):
        self._buildSearchTrie(*args)
    
        # any complete match must include one of the searchterms - we pick the first
        searchTerm = args[0].lower()
        log_pointers = self.log_trie.findWord(searchTerm)

        hit_list = []
        for pointer in log_pointers:
            hits = self.search_trie.findPointer(pointer)
            if hits >= len(args):
                hit_list.append(pointer)

        self.result = hit_list    

    def mustBeBetween(self, start_date, end_date):
        pass

    def mustBeFore(self, date):
        pass

    def mustBeAfter(self, date):
        pass

    def mustBeFromClient(self, client_name):
        pass

    def ShowResults(self):
        for pointer in self.result:
            actual_line = self.all_files[pointer.client][pointer.date][pointer.linenumber]
            print(f'Client: {pointer.client}, date: {pointer.date}, line: {pointer.linenumber}')
            print(actual_line.GetTimeStamp(), actual_line.GetPayLoad())

