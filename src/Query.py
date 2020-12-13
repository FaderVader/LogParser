from Tries import SearchTrie
from Types import LogLine
from BinarySearchTree import BST
from PrepareTrie import PrepareTrie
from Types import Terminator as Terminator
from Types import IntervalPair as IntervalPair
from Utils import TermUtil as TermUtil
from Utils import EpochTimeUtil as EpochTimeUtil


class Query:
    """
    Low-level, generic methods for querying trie. Primary trie-building is invoked on instantiating.
    """
    # setup
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

    def buildSearchTrie(self, *args):
        """
        Build list of matches from search-words.
        Put returned pointers into sub-trie.
        """
        args_as_list = [*args]
        self.search_trie = SearchTrie()

        for arg in args_as_list:            
            word = arg.lower()  # all trie words are lowercased
            matches = self.log_trie.FindWord(word)  # get pointers to matches for every word

            # build search-trie of pointers - terminator accumulates hit-count
            [self.search_trie.AddPointer(match) for match in matches]

    # query utils
    def GetLine(self, pointer):
        return self.all_files[pointer.client][pointer.date][pointer.linenumber]

    # query methods
    def MustContainWords(self, *args):
        """
        Set Query.results to contain all matches. Args: 'word', 'word', ...
        """
        self.buildSearchTrie(*args)

        # any complete match must include one of the searchterms - we pick the first
        searchTerm = args[0].lower()
        log_pointers = self.log_trie.FindWord(searchTerm)

        # to satisfy criteria, a hit must contain at least all search-terms
        len_args = len(args)
        hit_set = {pointer for pointer in log_pointers if self.search_trie.FindPointer(pointer) >= len_args}

        self.results = list(hit_set)

    def StartEnd(self, start_words, end_words):
        """
        Find all delta time-intervals between two sets of occurrences.\n
        Parameters: start_words: [ list of words ], end_words: [ list of words ]
        """
        IntervalPairs = []
        max_interval = 120  # (seconds) if an interval exceeds this value, we disregard as false 

        # We build two sets of intermediary results
        self.MustContainWords(*start_words)
        start_results = self.SortOnTime().copy() 

        self.MustContainWords(*end_words)
        end_results = self.SortOnTime().copy() 

        # For every hit of start-words, find next immediate match of end-words.
        # Then store line-pairs.
        for line_start in start_results:
            self.results = start_results.copy()
            actual_line_start = self.GetLine(line_start)
            actual_line_start_timestamp = actual_line_start.GetTimeStamp()
            actual_line_start_time = LogLine.ConvertTimestampToString(actual_line_start_timestamp)

            self.results = end_results.copy()
            self.MustBeFromClient(line_start.client)
            self.MustBeAfter(actual_line_start_time, True)
            try:
                # throws exception if no end-match is found -> then we skip pair
                line_end = self.results[0]  

                # pairs should be from same date/file (sanity check)
                if line_start.date != line_end.date:  
                    continue

                # filter false results
                delta = LogLine.GetTimeStamp(self.GetLine(line_end)) - actual_line_start_timestamp  
                if delta > max_interval or delta <= 0:
                    continue

                pair = IntervalPair(None, line_start, line_end)
                IntervalPairs.append(pair)
            except: continue  

        # Fold the late line of pair into Terminator's/pointer's payload 
        interval_results = [Terminator(pair.pointer_A.client, 
                            pair.pointer_A.date, 
                            pair.pointer_A.linenumber, 
                            TermUtil.ToString(pair.pointer_B)) for pair in IntervalPairs]

        self.results = interval_results

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
        Truncate Query.results to contain only events before date.\n
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
        Truncate Query.results to events later than date arg: \n
        Normal time-string: 2020-12-01-00:00:00.0
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
        local_results = [pointer for pointer in self.results if pointer.client == client_name]
        self.results = local_results

    def SortOnTime(self):
        """
        Sort current results on time (ascending).
        Returns a sorted list.
        """
        bst = BST()

        if self.results is None:
            raise ValueError("Query.SortOnTime(): No results to sort.")

        for pointer in self.results:
            actual_line = self.GetLine(pointer)            
            line = f'{actual_line.GetTimeStamp()} {TermUtil.ToString(pointer)}'  # add delta time header to pointer 
            bst.add(line)  

        sorted = bst.inOrder()

        sorted_list = [TermUtil.StringToPointerWithPayload(line.split()[1]) for line in sorted]  # strip the delta time header off
        return sorted_list

    def GetClients(self):
        """
        If we have results, returns all clients across all results, otherwise across all files.
        """
        if self.results is None:
            clients = [*self.all_files]
            return clients

        found_clients = {pointer.client for pointer in self.results}
        return list(found_clients)

    # StartEnd helper methods
    def wrap_delta(self, pointer_start, delta_set_separator='##'):
        """
        Helper for StartEnd: We expect a pointer containing embedded/linked pointer.\n
        Calculate the time-delta between log-entries.\n
        Return values: 
        - delta-t
        - {delta_t}{separator}{pointer}
        """
        line_start = self.GetLine(pointer_start)

        # we unpack reference to end_line in order to calculate t_delta
        line_end_pointer = TermUtil.ToTerminator(pointer_start.payload)
        line_end = self.GetLine(line_end_pointer)                                
        t_delta = (line_end.GetTimeStamp() - line_start.GetTimeStamp())  
        t_delta_formatted = EpochTimeUtil.DeltaTimeWrap(t_delta)  # We must ensure sortability on delta-values    

        # pointer_start already contains embedded pointer, so we just convert to string
        delta_set = f'{t_delta_formatted}{delta_set_separator}{TermUtil.ToString(pointer_start)}'
        return t_delta, delta_set

    def unwrap_delta(self, item, delta_set_separator='##'):
        """
        Helper for StartEnd: unpack a string returned from BST.\n
        Expected arg-format: {delta_t}{separator}{pointer}
        """
        delta_t_part = int(item.split(delta_set_separator)[0])
        pointers_part = item.split(delta_set_separator)[1]
        delta_t = EpochTimeUtil.DeltaTimeUnWrap(delta_t_part)
        return delta_t, pointers_part

    # display results
    def ShowStats(self, format=1, top_bottom=10):
        """
        Iterate over results.
        if a result has payload, we get embedded pointer
            - then we calculate time-delta

        stringify all (t_delta, pointer) and load into a BST

        retrieve sorted, take 5 lowest, 5 highest, average
        show the low/high line-sets
        """
        delta_set_separator = '##'
        delta_sum = 0  # aggregate intervals for calculating average
        bst = BST()
        results_count = len(self.results)

        for result in self.results:
            if result.payload is not None:
                t_delta, delta_set = self.wrap_delta(result, delta_set_separator)
                bst.add(delta_set)
                delta_sum += t_delta  

        sorted_delta = bst.inOrder()

        # if less results than top_bottom, we override
        top_bottom_limit = results_count // 2
        if top_bottom_limit < top_bottom:
            top_bottom = top_bottom_limit

        bottom_slice = sorted_delta[:top_bottom]  # fastest
        top_slice = sorted_delta[-top_bottom:]   # slowest

        def print_lines(result_slice):
            for index, item in enumerate(result_slice):
                delta_t, pointers_part = self.unwrap_delta(item, delta_set_separator)
                print(f'#{index+1} - delta t: {delta_t}')

                # using a set of converters to build Terminator with embedded content.
                linked_pointers = [TermUtil.StringToPointerWithPayload(pointers_part)]
                self.ShowResults(format, linked_pointers)

        t_delta_average = delta_sum / results_count  # calculate average interval (sec)
        print(f'\nTotal results: {results_count} - Average interval: {t_delta_average} seconds.\n')

        print(f'SHORTEST INTERVAL - {top_bottom} items')
        print_lines(bottom_slice)

        print(f'LONGEST INTERVAL - {top_bottom} items')
        print_lines(top_slice)

        print(f'\nTotal results: {results_count} - Average interval: {t_delta_average} seconds.\n')

    def ShowResults(self, format=0, result_list=None):
        """
        Print the content of Query.results.
        Add argument 'format=1' to print time in true date, otherwise epoch.
        """
        if result_list is None:
            result_list = self.results

        def inner(pointer):
            if pointer is None: return

            # standard result-type - one line            
            self.print_logLine(pointer, format)

            if pointer.payload is not None:  
                # extended resulttype - payload has reference to linked line
                linked_line = TermUtil.ToTerminator(pointer.payload)
                self.print_logLine(linked_line, format)
                inner(TermUtil.ToTerminator(linked_line))  # any more ?
                
        for pointer in result_list:
            inner(pointer)
        print('')  # one line spacer
        # print(f'result count: {len(self.results)}')

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
    query.ShowStats(1, 3)

    # test = query.GetClients()
    # print(test)
    # query.MustContainWords('setupsession', 'running')
    # query.MustBetween('2020-10-14-17:03:54.500050', '2020-10-16-10:22:50.668270')
    # query.ShowResults(1)
