from Query import Query
import json
import inspect


class QueryParser:
    """
    Frontend for queries. 
    """
    def __init__(self):
        self.query_methods = ['StartEnd', 'Find', 'Between', 'Client', 'Sort']  # index of supported operations
        self.query = None    # base query instance - should be reset before every parse-op

    # parsing utils
    def parse_json(self, query):
        if isinstance(query, str):
            return json.loads(query)
        else:
            return query

    def get_args_from_query(self, query, element):
        arguments = query.__getattribute__(element)
        return arguments

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
        Primary entry-point. Process the search-args.
        Supported syntax: {"Find": [list of words], "Between": [startdate, enddate], "Client": clientname}
        """
        self.query = Query()  # setup/reset base query between parse-operations
        try:
            self.invoke_query(args)
            self.query.ShowResults(1)
        except:
            print("No results found!")            

    # eDSL key-words 
    def Find(self, args):
        user_query = self.parse_json(args)
        arguments = [*self.get_args_from_query(user_query, 'Find')]
        self.query.MustContainWords(*arguments)

    def Between(self, args):
        user_query = self.parse_json(args)
        arguments = [*self.get_args_from_query(user_query, 'Between')]
        self.query.MustBetween(*arguments)

    def Client(self, args):
        user_query = self.parse_json(args)
        arguments = self.get_args_from_query(user_query, 'Client')
        self.query.MustBeFromClient(arguments)

    def Sort(self, args):
        sorted_list = self.query.SortOnTime()
        self.query.results = sorted_list

    def StartEnd(self, args):
        """
        Find all intervals between two sets of occurrences.
        "StartEnd": [[list of words], [list of words]
        """

        user_query = self.parse_json(args)
        start_words = [*self.get_args_from_query(user_query, 'StartEnd')[0]]
        end_words = [*self.get_args_from_query(user_query, 'StartEnd')[1]]

        self.query.StartEnd(start_words, end_words)
