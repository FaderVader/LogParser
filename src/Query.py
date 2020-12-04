from Tries import SearchTrie
from LogLine import LogLine
from BinarySearchTree import BST
from PrepareTrie import PrepareTrie
from Types import Terminator as Terminator
from Types import IntervalPair as IntervalPair
from Utils import TermUtil as TermUtil


class Query:
    """
    Low-level, generic methods for querying trie. Primary trie-building is invoked on instantiating.
    """
    def __init__(self):
        self.log_trie = None      # main trie - contains content of all logs
        self.all_files = None     # all log-files in structured object
        self.search_trie = None   # trie used for coordinating word-searches
        self.results = None       # aggregated result-set
        self.setup()

    def setup(self):
        trie = PrepareTrie()                       # setup the tries
        self.log_trie = trie.GetLogTrie()          # load log-trie
        self.all_files = trie.GetStructuredLogs()  # get the files in structured format
        self.search_trie = None

    def buildSearchTrie(self, *args):
        """
        Build list of matches from search-words.
        Put returned pointers into sub-trie.
        """
        args_as_list = [*args]
        self.search_trie = SearchTrie()

        for arg in args_as_list:
            # get pointer to matches for every word
            word = arg.lower()
            matches = self.log_trie.FindWord(word) 

            # build trie of pointers, terminator indicates number of hits
            for match in matches:
                self.search_trie.addPointer(match)

    def GetLine(self, pointer):
        return self.all_files[pointer.client][pointer.date][pointer.linenumber]

    def GetClients(self):
        """
        Returns all clients across all logfiles.
        """
        clients = [*self.all_files]
        return clients

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
            if (time_stamp < end_date_epoch):
                local_results.append(pointer)
        self.results = local_results

    def MustBeAfter(self, date):  # TODO we could sort .results and stop iterating after first match, then slice the list
        """
        Truncate Query.results to only events after
        """
        start_date_epoch = LogLine.ConvertStringToTime(date)
        local_results = []

        for pointer in self.results:
            actual_line = self.GetLine(pointer)
            time_stamp = actual_line.GetTimeStamp()
            if (time_stamp > start_date_epoch):
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
            bst.add(f'{actual_line.GetTimeStamp()} ##{pointer.client}#{pointer.date}#{pointer.linenumber}#{pointer.payload}')  # store pointer as string for later deconstruct
            # TODO: we should encapsulate in a method

        sorted = bst.inOrder()
        sorted_list = []
        for line in sorted:
            pointer_parts = line.split('##')[1].split('#')  # re-creating pointer as Terminator tuple
            if pointer_parts[3] == "None": pointer_parts[3] = None  # survive the stringiness
            term = Terminator(pointer_parts[0], pointer_parts[1], int(pointer_parts[2]), pointer_parts[3])
            sorted_list.append(term)
        return sorted_list

    def StartEnd(self, start_words, end_words):
        """
        Find all intervals between two sets of occurrences.
        start_words:[list of words], end_words:[list of words]
        """
        IntervalPairs = []

        self.MustContainWords(*start_words)
        start_results = self.results.copy()  # avoid by-ref 

        self.MustContainWords(*end_words)
        end_results = self.results.copy()  # avoid by-ref

        # TODO : pairs should be from same date/file (sanity check)

        # For every hit of start-words, find next immediate match of end-words.
        # Then store line-pairs.
        for line_start in start_results:
            self.results = start_results.copy()
            actual_line_start = self.GetLine(line_start)
            actual_line_start_time = LogLine.ConvertTimestampToString(actual_line_start.GetTimeStamp())

            self.results = end_results.copy()
            self.MustBeFromClient(line_start.client)
            self.MustBeAfter(actual_line_start_time)
            try:
                line_end = self.results[0]  # throws exception if no end-match is found -> then we skip pair
                pair = IntervalPair(line_start, line_end)
                IntervalPairs.append(pair)
            except: continue  
        
        # Pack the late line in pair into Terminator's/pointer's payload 
        interval_results = []
        for pair in IntervalPairs:
            payload = TermUtil.ToString(pair.pointer_B)
            term = Terminator(pair.pointer_A.client, pair.pointer_A.date, pair.pointer_A.linenumber, payload)
            interval_results.append(term)

        self.results = interval_results

    def ShowResults(self, format=0):
        """
        Print the content of Query.results.
        Add argument 'format=1' to print time in true date, otherwise epoch.
        """
        for pointer in self.results:
            print('')  # one line spacer

            def inner(pointer):
                if pointer is None: return

                # standard result-type - one line            
                self.print_logLine(pointer, format)

                if pointer.payload is not None:  
                    # extended resulttype - payload has reference to linked line
                    linked_line = TermUtil.ToTerminator(pointer.payload)
                    self.print_logLine(linked_line, format)
                    inner(TermUtil.ToTerminator(linked_line))  # any more ?
            inner(pointer)
        print(f'result count: {len(self.results)}')

    def print_logLine(self, pointer, format=0):
        """
        Takes a Terminator as pointer to log-line and prints it.
        """
        actual_line = self.GetLine(pointer)
        print(f'Client: {pointer.client}, date: {pointer.date}, line: {pointer.linenumber}')

        if format != 0:
            time = LogLine.ConvertTimestampToString(actual_line.GetTimeStamp())
        else:
            time = actual_line.GetTimeStamp()
        print(time, actual_line.GetPayLoad())


if __name__ == "__main__":
    query = Query()
    query.setup()
    test = query.GetClients()
    print(test)
