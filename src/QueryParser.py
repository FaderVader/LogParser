from Query import Query
import json
import inspect


class QueryParser:
    """
    Frontend for queries. Depends on Query.
    """
    def __init__(self):
        self.query_methods = ['StartEnd', 'Find', 'Between', 'Client', 'Sort', 'ShowStats']  # index of supported syntax
        self.query = Query()    # base query instance

    # if query is json-shaped, deserialize 
    def parse_json(self, query):
        if isinstance(query, str):
            return json.loads(query)
        else:
            return query

    # extract required element from query
    def get_args_from_query(self, query, element):
        arguments = query[element]  
        return arguments

    # use a little reflection to invoke functions
    def invoke_query(self, args):
        """
        Acquire delegate and invoke with arguments
        """
        user_query = self.parse_json(args)
        all_members = inspect.getmembers(QueryParser, inspect.isfunction)

        for query in self.query_methods:  
            if query in user_query:  
                for function_name, function_obj in all_members:
                    if query == function_name:
                        method = getattr(QueryParser, function_name)
                        arguments = self.get_args_from_query(user_query, function_name)
                        method(self, arguments)

    def GetClients(self):
        """
        Returns all clients, aggregated across all log-files.
        """
        clients = self.query.GetClients()
        return clients

    def Parse(self, args):
        """
        Primary entry-point. Process the search-args.\n
        Supported syntax: 
            "StartEnd": [[word list], [word list]], 
            "Find": [list of words], 
            "Between": [startdate, enddate], 
            "Client": clientname,
            "Sort": (any value)
        """
        try:
            self.invoke_query(args)
            self.query.ShowResults(1)
        except AttributeError as e:
            print(f"Program error - Attribute error: {str(e)}")
        except ValueError as e:
            print(f"Program error - Value error: {str(e)}")
        except:
            print("No results found!")            

    # eDSL key-words 
    def Find(self, args):
        self.query.MustContainWords(*args)

    def Between(self, args):
        self.query.MustBetween(*args)

    def Client(self, args):
        self.query.MustBeFromClient(args)

    def Sort(self, arg): 
        if arg is True:
            sorted_list = self.query.SortOnTime()
            self.query.results = sorted_list

    def StartEnd(self, args):
        """
        Find all intervals between two sets of occurrences.
        "StartEnd": [[list of words], [list of words]
        """
        start_words = args[0]
        end_words = args[1]

        self.query.StartEnd(start_words, end_words)

    def ShowStats(self, args):
        self.query.ShowStats(args)
