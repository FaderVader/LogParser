from Query import Query
from PrepareTrie import PrepareTrie
import json
import inspect


class QueryParser:
    """
    Frontend for queries. Instantiating invokes primary trie-building.
    """
    def __init__(self):
        self.query_methods = ['Find', 'Between', 'Client']
        self.base_query = None    # base query instance - should be reset before every parse-op
        self.loaded_trie = None   # Main trie - contains content of all logs
        self.logs = None          # all log-files in structured object
        self.setup()

    def setup(self):
        trie = PrepareTrie()                  # setup the tries
        self.loaded_trie = trie.GetLogTrie()  # load log-trie
        self.logs = trie.GetStructuredLogs()  # get the files in structured format

    def parse_json(self, query):
        data = json.loads(query)
        return data

    def get_query(self):
        query = Query(self.loaded_trie, self.logs)
        return query

    def invoke_query(self, args):
        user_query = self.parse_json(args)
        all_members = inspect.getmembers(QueryParser, inspect.isfunction)

        for query in self.query_methods:
            if query in user_query:
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
        result = [*query['Find']]
        self.base_query.MustContainWords(*result)

    def Between(self, args):
        query = self.parse_json(args)
        result = [*query['Between']]
        self.base_query.MustBetween(*result)

    def Client(self, args):
        query = self.parse_json(args)
        result = query['Client']
        self.base_query.MustBeFromClient(result)
