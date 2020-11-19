"""
    Build generic methods for querying trie.
"""
from Tries import SearchTrie
from LogLine import LogLine
from BinarySearchTree import BST

class Query:
    def __init__(self, log_trie, all_files):
        self.log_trie = log_trie
        self.search_trie = SearchTrie()
        self.all_files = all_files
        self.results = None

    # 'private' method
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

        # to satisfy criteria, a hit must contain at least all search-terms
        hit_list = []
        for pointer in log_pointers:
            hits = self.search_trie.findPointer(pointer)
            if hits >= len(args):
                hit_list.append(pointer)
        self.results = hit_list    


    def mustBeBetween(self, start_date, end_date): # date format: 2020-09-04-18:16:12.1515421
        self.mustBeAfter(start_date)
        self.mustBeFore(end_date)


    def mustBeFore(self, date):
        end_date_epoch = LogLine.parseStringToTime(date)
        local_results = []

        for pointer in self.results:
            actual_line = self.all_files[pointer.client][pointer.date][pointer.linenumber]
            time_stamp = actual_line.GetTimeStamp()
            if (time_stamp <= end_date_epoch):
                local_results.append(pointer)
        self.results = local_results


    def mustBeAfter(self, date):
        start_date_epoch = LogLine.parseStringToTime(date)
        local_results = []

        for pointer in self.results:
            actual_line = self.all_files[pointer.client][pointer.date][pointer.linenumber]
            time_stamp = actual_line.GetTimeStamp()
            if (time_stamp >= start_date_epoch):
                local_results.append(pointer)
        self.results = local_results


    def mustBeFromClient(self, client_name):
        local_results = []

        for pointer in self.results:
            if pointer.client == client_name:
                local_results.append(pointer)
        self.results = local_results


    def sortOnTime(self):
        bst = BST()

        for pointer in self.results:
            actual_line = self.all_files[pointer.client][pointer.date][pointer.linenumber]
            bst.add(f'{actual_line.GetTimeStamp()} {actual_line.GetPayLoad()}')

        sorted = bst.inOrder()
        for line in sorted:
            print(line)

        

    def showResults(self, format=0):
        for pointer in self.results:
            actual_line = self.all_files[pointer.client][pointer.date][pointer.linenumber]
            print(f'Client: {pointer.client}, date: {pointer.date}, line: {pointer.linenumber}')
            if format != 0:
                time = LogLine.parseTimeStampToString(actual_line.GetTimeStamp())
            else:
                time = actual_line.GetTimeStamp()

            print(time, actual_line.GetPayLoad())

