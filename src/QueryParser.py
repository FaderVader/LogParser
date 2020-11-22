from Query import Query
from PrepareTrie import PrepareTrie
import json
import inspect


class QueryParser:
    def __init__(self):
        self.query_methods = ['find', 'between', 'client']
        self.base_query = None    # base query instance - should be reset before every parse-op
        self.loaded_trie = None   # Main trie - contains content of all logs
        self.logs = None          # all log-files in structured object
        self.setup()

    def setup(self):
        trie = PrepareTrie()  # setup the tries
        self.loaded_trie = trie.GetLogTrie()  # load log-trie
        self.logs = trie.GetStructuredLogs()  # get the files in structured format

    def getQuery(self):
        query = Query(self.loaded_trie, self.logs)
        return query

    def parse(self, args):
        self.base_query = self.getQuery()
        self.invoke_query(args)
        self.base_query.showResults(1)

    def parse_json(self, query):
        data = json.loads(query)
        return data

    def invoke_query(self, args):
        user_query = self.parse_json(args)
        all_members = inspect.getmembers(QueryParser, inspect.isfunction)

        for query in self.query_methods:
            if query in user_query:
                for function_name, function_obj in all_members:
                    if query == function_name:
                        method = getattr(QueryParser, function_name)
                        method(self, args)

    # DSL
    def find(self, args):
        query = self.parse_json(args)
        result = [*query['find']]
        self.base_query.mustContainWords(*result)

    def between(self, args):
        query = self.parse_json(args)
        result = [*query['between']]
        self.base_query.mustBeBetween(*result)

    def client(self, args):
        query = self.parse_json(args)
        result = query['client']
        self.base_query.mustBeFromClient(result)
