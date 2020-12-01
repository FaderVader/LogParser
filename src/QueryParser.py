from Query import Query
from PrepareTrie import PrepareTrie
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

        query = self.parse_json(args)
        start_words = [*self.get_args_from_query(query, 'StartEnd')[0]]
        end_words = [*self.get_args_from_query(query, 'StartEnd')[1]]

        self.base_query.StartEnd(start_words, end_words)
