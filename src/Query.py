from Tries import SearchTrie
from LogLine import LogLine
from BinarySearchTree import BST
from Types import Terminator as Terminator
import inspect


class Query:
    """
    Low-level, generic methods for querying trie.
    """
    def __init__(self, log_trie, all_files):
        self.log_trie = log_trie
        self.search_trie = SearchTrie()
        self.all_files = all_files
        self.results = None

    def buildSearchTrie(self, *args):
        """
        Build list of matches from search-words. 
        Put returned pointers into sub-trie.
        """
        args_as_list = [*args]

        for arg in args_as_list:            
            # get pointer to matches for every word
            word = arg.lower()
            matches = self.log_trie.FindWord(word) 

            # build trie of pointers, terminator indicates number of hits
            for match in matches:
                self.search_trie.addPointer(match)

    def GetLine(self, pointer):
        return self.all_files[pointer.client][pointer.date][pointer.linenumber]

    def MustContainWords(self, *args):
        """
        Set Query.results to contain all matches
        """
        self.buildSearchTrie(*args)

        # any complete match must include one of the searchterms - we pick the first
        searchTerm = args[0].lower()
        log_pointers = self.log_trie.FindWord(searchTerm)

        # to satisfy criteria, a hit must contain at least all search-terms
        hit_list = []
        for pointer in log_pointers:
            hits = self.search_trie.findPointer(pointer)
            if hits >= len(args):
                hit_list.append(pointer)
        self.results = hit_list

    def MustBetween(self, start_date, end_date):  # date format: 2020-09-04-18:16:12.1515421
        """
        Truncate Query.results to a time-span
        """
        self.MustBeAfter(start_date)
        self.MustBeFore(end_date)

    def MustBeFore(self, date):
        """
        Truncate Query.results to only events before 
        """
        end_date_epoch = LogLine.ConvertStringToTime(date)
        local_results = []

        for pointer in self.results:
            actual_line = self.GetLine(pointer)
            time_stamp = actual_line.GetTimeStamp()
            if (time_stamp <= end_date_epoch):
                local_results.append(pointer)
        self.results = local_results

    def MustBeAfter(self, date):
        """
        Truncate Query.results to only events after
        """
        start_date_epoch = LogLine.ConvertStringToTime(date)
        local_results = []

        for pointer in self.results:
            actual_line = self.GetLine(pointer)
            time_stamp = actual_line.GetTimeStamp()
            if (time_stamp >= start_date_epoch):
                local_results.append(pointer)
        self.results = local_results

    def MustBeFromClient(self, client_name):
        """
        Truncate Query.results to only be from specified client
        """
        local_results = []

        for pointer in self.results:
            if pointer.client == client_name:
                local_results.append(pointer)
        self.results = local_results

    def SortOnTime(self):
        """
        For every Query.results, create line incl timestamp.
        Add complete line to BST and new sorted trie.
        """
        bst = BST()

        for pointer in self.results:
            actual_line = self.GetLine(pointer)
            bst.add(f'{actual_line.GetTimeStamp()} ##{pointer.client}#{pointer.date}#{pointer.linenumber}')  # store pointer as string for later deconstruct

        sorted = bst.inOrder()
        sorted_list = []
        for line in sorted:
            pointer_parts = line.split('##')[1].split('#')  # re-creating pointer as Terminator tuple
            term = Terminator(pointer_parts[0], pointer_parts[1], int(pointer_parts[2]))
            sorted_list.append(term)
        return sorted_list

    def ShowResults(self, format=0):
        """
        Print the content of Query.results.
        Add argument 'format=1' to print time in true date, otherwise epoch.
        """

        if len(self.results) <= 0:
            return

        for pointer in self.results:
            actual_line = self.GetLine(pointer)
            print(f'Client: {pointer.client}, date: {pointer.date}, line: {pointer.linenumber}')
            if format != 0:
                time = LogLine.ConvertTimestampToString(actual_line.GetTimeStamp())
            else:
                time = actual_line.GetTimeStamp()

            print(time, actual_line.GetPayLoad())
