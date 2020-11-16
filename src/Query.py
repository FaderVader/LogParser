"""
    Build generic methods for querying trie.
"""
from TrieBuilder import SearchTrie

class Query:
    def __init__(self, log_trie):
        self.log_trie = log_trie
        self.search_trie = SearchTrie()

    def mustContainWords(self, *args):
        for arg in args:            
            # get pointer to matches for every word
            word = arg.lower()
            matches = self.log_trie.findWord(word) 
            
            # build trie of pointers, terminator indicates number of hits
            for match in matches:
                self.search_trie.addPointer(match)
    
        # any complete match must include one of the searchterms - we pick the first
        searchTerm = args[0].lower()
        log_pointers = self.log_trie.findWord(searchTerm)

        hit_list = []
        for pointer in log_pointers:
            hits = self.search_trie.findPointer(pointer)
            if hits >= len(args):
                hit_list.append(pointer)
        return hit_list

    def mustBeBetween(self, start_date, end_date):
        pass

    def mustBeFore(self, date):
        pass

    def mustBeAfter(self, date):
        pass

    def mustByFromClient(self, client_name):
        pass