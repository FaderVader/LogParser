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
        Set Query.results to contain all matches. Args: 'word', 'word', ...
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

    def MustBetween(self, start_date, end_date, is_sorted=False):  # date format: 2020-09-04-18:16:12.1515421
        """
        Truncate Query.results to a time-span. (start & end not included) \n 
        Date arg: normal time-string: 2020-12-01-00:00:00.0 \n
        If we know results are already ordered by date ascending, set flag is_sorted=True
        """
        is_sorted = self.MustBeAfter(start_date, is_sorted)
        self.MustBeFore(end_date, is_sorted)

    def MustBeFore(self, date, is_sorted=False): 
        """
        Truncate Query.results to only events before 
        Date arg: normal time-string: 2020-12-01-00:00:00.0 \n 
        If we know the result-set is already sorted, set is_sorted=True
        """
        end_date_epoch = LogLine.ConvertStringToTime(date)
        local_results = []

        if not is_sorted:
            sorted_results = self.SortOnTime()
            is_sorted = True
        else: 
            sorted_results = self.results   

        # edge-case: if cut-off date is later than last result
        # we just keep results intact
        last_line = sorted_results[len(sorted_results) - 1]
        last_line_time = self.GetLine(last_line).GetTimeStamp()
        if end_date_epoch >= last_line_time:
            return is_sorted

        for index, pointer in enumerate(sorted_results):
            actual_line = self.GetLine(pointer)
            time_stamp = actual_line.GetTimeStamp()
            if (time_stamp > end_date_epoch):
                local_results = sorted_results[:index]  # take rest
                break
        self.results = local_results
        return is_sorted

    def MustBeAfter(self, date, is_sorted=False):
        """
        Truncate Query.results to events later than date arg: normal time-string: 2020-12-01-00:00:00.0
        """
        start_date_epoch = LogLine.ConvertStringToTime(date)
        local_results = []

        if not is_sorted:
            sorted_results = self.SortOnTime()
            is_sorted = True
        else: 
            sorted_results = self.results   

        for index, pointer in enumerate(sorted_results):
            actual_line = self.GetLine(pointer)
            time_stamp = actual_line.GetTimeStamp()
            if (time_stamp > start_date_epoch):                
                local_results = sorted_results[index:]  # take rest
                break
        self.results = local_results
        return is_sorted

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
        max_interval = 120  # if an interval exceeds this value, we disregard as false 

        self.MustContainWords(*start_words)
        start_results = self.SortOnTime().copy()  # avoid by-ref 

        self.MustContainWords(*end_words)
        end_results = self.SortOnTime().copy()  # avoid by-ref 

        # For every hit of start-words, find next immediate match of end-words.
        # Then store line-pairs.
        for line_start in start_results:
            self.results = start_results.copy()
            actual_line_start = self.GetLine(line_start)
            actual_line_start_timestamp = actual_line_start.GetTimeStamp()
            actual_line_start_time = LogLine.ConvertTimestampToString(actual_line_start_timestamp)

            self.results = end_results.copy()
            self.MustBeFromClient(line_start.client)
            self.MustBeAfter(actual_line_start_time)
            try:
                # throws exception if no end-match is found -> then we skip pair
                line_end = self.results[0]  
                
                # pairs should be from same date/file (sanity check)
                if line_start.date != line_end.date:  
                    continue

                # filter false results
                delta = LogLine.GetTimeStamp(self.GetLine(line_end)) - actual_line_start_timestamp  
                if delta > max_interval:
                    continue

                pair = IntervalPair(None, line_start, line_end)
                IntervalPairs.append(pair)
            except: continue  
        
        # Pack the late line in pair into Terminator's/pointer's payload 
        interval_results = []
        for pair in IntervalPairs:
            payload = TermUtil.ToString(pair.pointer_B)
            term = Terminator(pair.pointer_A.client, pair.pointer_A.date, pair.pointer_A.linenumber, payload)
            interval_results.append(term)

        self.results = interval_results

    def ShowStats(self):
        """
        Iterate over results.
        if a result has payload, we get embedded pointer
            - then we calculate time-delta

        stringify all (t_delta, pointer) and load into a BST

        retrieve sorted, take 5 lowest, 5 highest, average
        show the low/high line-sets
        """
        delta_factor = 10**10      
        delta_padding = 20  
        bst = BST()

        for result in self.results:
            if result.payload is not None:
                line_start = self.GetLine(result)
                line_end_pointer = TermUtil.ToTerminator(result.payload)
                line_end = self.GetLine(line_end_pointer)

                # We must ensure sortability on delta-values    
                # - sort-as string fails to handle 10 and 1043 well
                t_delta = (line_end.GetTimeStamp() - line_start.GetTimeStamp()) 
                t_delta_factored = t_delta * delta_factor
                t_delta_string = (f'{t_delta_factored}').split('.')[0]

                length = len(t_delta_string)
                t_delta_formatted = ('0' * (delta_padding - length)) + t_delta_string  # pad with leading zero's

                # verify conversion error
                test = (int(t_delta_formatted)) / delta_factor
                if (t_delta - test) > 0.00001: 
                    print(t_delta - test)

                delta_set = f'{t_delta_formatted} ##{TermUtil.ToString(result)}'
                bst.add(delta_set)

        sorted_delta = bst.inOrder()
        
        top_bottom = 10
        bottom_five = sorted_delta[:top_bottom]  # fastest
        high_five = sorted_delta[-top_bottom:]   # slowest

        for bottom in bottom_five:
            delta_t_part = int(bottom.split()[0])
            pointers_part = bottom.split()[1]
            delta_t = int(delta_t_part) / delta_factor
            print(delta_t, pointers_part)

        for top in high_five:
            delta_t_part = int(top.split()[0])
            pointers_part = top.split()[1]
            delta_t = int(delta_t_part) / delta_factor
            print(delta_t, pointers_part)

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
    query.StartEnd(['setupsession', 'running'], ['setupsession', 'completed'])
    query.ShowStats()

    # test = query.GetClients()
    # print(test)
    # query.MustContainWords('setupsession', 'running')
    # query.MustBetween('2020-10-14-17:03:54.500050','2020-10-16-10:22:50.668270')
    # query.ShowResults(1)
