from QueryParser import QueryParser
from Types import QuerySyntax as QuerySyntax
import cmd
import sys


class Build(cmd.Cmd):
    def __init__(self):
        super().__init__()        
        print("Starting up ....")        
        self.startend = None
        self.find = None
        self.between = None
        self.client = None
        self.sort = None
        self.queryParser = QueryParser()
        self.show_help()

    def Syntax(self, StartEnd=None, Find=None, Between=None, Client=None, Sort=None):
        return QuerySyntax(StartEnd, Find, Between, Client, Sort)

    def show_help(self):
        with open("src/help.txt") as help:
            for line in help:
                print(line, end="")

    def do_help(self, args):
        self.show_help()

    def do_reset(self, args):
        self.startend = None
        self.find = None
        self.between = None
        self.client = None
        self.sort = None

    def do_exit(self, args):
        print("Goodbye ....")
        sys.exit()

    def do_startend(self, args):
        print(f'Adding STARTEND to query: {args}')
        parts = args.split(',')
        part_start = parts[0].split()
        part_end = parts[1].split()
        self.startend = [part_start, part_end]

    def do_find(self, args):
        print(f'Adding FIND to query: {args}')
        words = args.split()
        self.find = words

    def do_between(self, args):
        print(f'Adding BETWEEN to query: {args}')
        dates = args.split()
        self.between = dates

    def do_client(self, arg):
        print(f'Adding CLIENT to query: {arg}')
        self.client = arg

    def do_sort(self, arg):
        print(f'Adding SORT to query: {arg}')
        self.sort = int(arg)

    def do_show(self, args):
        print(self.Syntax(self.startend, self.find, self.between, self.client, self.sort))

    def do_execute(self, arg):
        final_query = self.Syntax(self.startend, self.find, self.between, self.client, self.sort)
        print(final_query)
        self.execute_query(final_query)

    def execute_query(self, syntax):
        self.queryParser.Parse(syntax)


if __name__ == "__main__":
    build = Build()
    build.cmdloop()
