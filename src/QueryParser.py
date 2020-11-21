import json
import inspect


class QueryParser:
    def __init__(self, query):
        self.query_methods = ['find', 'between', 'client']
        self.main_query = query

    def parse(self, args):
        self.get_members(args)
        self.main_query.showResults(1)

    def parse_json(self, query):
        data = json.loads(query)
        return data

    def get_members(self, args):
        user_query = self.parse_json(args)
        all_members = inspect.getmembers(QueryParser, inspect.isfunction)

        for query in self.query_methods:
            if query in user_query:
                for function_name, function_obj in all_members:
                    if query == function_name:
                        method = getattr(QueryParser, function_name)
                        method(self, args)

    def find(self, args):
        query = self.parse_json(args)
        result = [*query['find']]
        self.main_query.mustContainWords(*result)

    def between(self, args):
        query = self.parse_json(args)
        result = [*query['between']]
        self.main_query.mustBeBetween(*result)

    def client(self, args):
        query = self.parse_json(args)
        result = query['client']
        self.main_query.mustBeFromClient(result)



# qp = QueryParser()
# query = '{"find": ["setupsession", "running"], "between": ["2020-10-06-0:0:0.0", "2020-10-06-23:59:59.9"], "client": "AX82017"}'
# qp.parse(query)