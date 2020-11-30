from Query import Query
from PrepareTrie import PrepareTrie
from LogLine import LogLine
from Types import IntervalPair as IntervalPair
import json
import inspect


class QueryParser:
    """
    Frontend for queries. Primary trie-building is invoked on instantiating.
    """
    def __init__(self):
        self.query_methods = ['StartEnd', 'Find', 'Between', 'Client', 'Sort']
        self.base_query = None    # base query instance - should be reset before every parse-op
        self.loaded_trie = None   # Main trie - contains content of all logs
        self.logs = None          # all log-files in structured object
        self.setup()

    def setup(self):
        trie = PrepareTrie()                  # setup the tries
        self.loaded_trie = trie.GetLogTrie()  # load log-trie
        self.logs = trie.GetStructuredLogs()  # get the files in structured format

    # parsing utils
    def parse_json(self, query):
        if isinstance(query, str):
            return json.loads(query)
        else:
            return query

    def get_args_from_query(self, query, element):
        arguments = query.__getattribute__(element)
        return arguments

    def get_query(self):
        """
        Used for resetting query and current result-list
        """
        query = Query(self.loaded_trie, self.logs)
        return query

    def invoke_query(self, args):
        user_query = self.parse_json(args)
        all_members = inspect.getmembers(QueryParser, inspect.isfunction)

        for query in self.query_methods:
            if query in user_query._fields and user_query.__getattribute__(query) is not None:  # _fields: attribute containing the fields of the tuple
                for function_name, function_obj in all_members:
                    if query == function_name:
                        method = getattr(QueryParser, function_name)
                        method(self, args)

    def Parse(self, args):
        """
        Process the search-args.
        Supported syntax: {"Find": [list of words], "Between": [startdate, enddate], "Client": clientname}
        """
        self.base_query = self.get_query()
        self.invoke_query(args)
        self.base_query.ShowResults(1)

    # eDSL key-words 
    def Find(self, args):
        query = self.parse_json(args)
        arguments = [*self.get_args_from_query(query, 'Find')]
        self.base_query.MustContainWords(*arguments)

    def Between(self, args):
        query = self.parse_json(args)
        arguments = [*self.get_args_from_query(query, 'Between')]
        self.base_query.MustBetween(*arguments)

    def Client(self, args):
        query = self.parse_json(args)
        arguments = self.get_args_from_query(query, 'Client')
        self.base_query.MustBeFromClient(arguments)

    def Sort(self, args):
        sorted_list = self.base_query.SortOnTime()
        self.base_query.results = sorted_list

    def StartEnd(self, args):
        """
        Find all intervals between two sets of occurrences.
        "StartEnd": [[list of words], [list of words]
        """
        IntervalPairs = []

        query = self.parse_json(args)
        start_words = [*self.get_args_from_query(query, 'StartEnd')[0]]
        end_words = [*self.get_args_from_query(query, 'StartEnd')[1]]

        self.base_query.MustContainWords(*start_words)
        start_results = self.base_query.results.copy()  # avoid by-ref 

        self.base_query = self.get_query()  
        self.base_query.MustContainWords(*end_words)
        end_results = self.base_query.results.copy()  # avoid by-ref

        for result in start_results:
            self.base_query.results = start_results.copy()
            actual_line_start = self.base_query.GetLine(result)
            actual_line_start_time = LogLine.ConvertTimestampToString(actual_line_start.GetTimeStamp())

            self.base_query.results = end_results.copy()
            self.base_query.MustBeFromClient(result.client)
            self.base_query.MustBeAfter(actual_line_start_time)
            try:
                line_end = self.base_query.results[0]  # throws exception if no end-match is found - then we skip pair
                actual_line_end = self.base_query.GetLine(line_end)

                t_delta = actual_line_end.GetTimeStamp() - actual_line_start.GetTimeStamp()
                pair = IntervalPair(t_delta, result, line_end)
                IntervalPairs.append(pair)
            except: continue  

        self.base_query.results = []  # ensure queue is empty after parsing

        for pair in IntervalPairs:
            t_delta = pair.delta
            pointer_start = self.base_query.GetLine(pair.pointer_A)
            pointer_end = self.base_query.GetLine(pair.pointer_B)

            print(pair.pointer_A, LogLine.ConvertTimestampToString(t_delta))
            print(f'{LogLine.ConvertTimestampToString(pointer_start.GetTimeStamp())} {pointer_start.GetPayLoad()}')
            print(f'{LogLine.ConvertTimestampToString(pointer_end.GetTimeStamp())} {pointer_end.GetPayLoad()}')
            print('')
