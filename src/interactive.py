from QueryParser import QueryParser
from Types import QuerySyntax as QuerySyntax
import cmd
import sys
from os import path as check_path
import datetime


class Build(cmd.Cmd):
    def __init__(self):
        super().__init__()       
        print("Loading all log-files ....")
        self.prompt = "LogParser> "

        # properties        
        self.startend = None
        self.find = None
        self.between = None
        self.client = None
        self.sort = None
        self.queryParser = QueryParser()

        # always show help-text on startup
        self.show_help()

    def Syntax(self, StartEnd=None, Find=None, Between=None, Client=None, Sort=None):
        return QuerySyntax(StartEnd, Find, Between, Client, Sort)

    def catch(func):
        """
        Error-wrapper for query-building commands
        """
        def inner(*args):
            try:
                return func(*args)
            except:
                print("Failed to parse command.")
        return inner

    def show_help(self):
        path = "help.txt"
        if not check_path.isfile(path):
            path = "src/help.txt"

        with open(path) as help:
            for line in help:
                print(line, end="")

    def parse_dates(self, args):
        dates = args.split()

        if len(dates) < 1:
            raise Exception("No date arguments provided")

        parsed_dates = []
        for i, date in enumerate(dates):
            if date == "today" and i == 0:
                date = datetime.date.today().strftime("%Y-%m-%d") + "-0:0:0.0"
            if date == "today" and i == 1:
                date = datetime.date.today().strftime("%Y-%m-%d") + "-23:59:59.9"
            parsed_dates.append(date)
        self.between = parsed_dates

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

    @catch
    def do_startend(self, args):
        parts = args.split(',')
        part_start = parts[0].split()
        part_end = parts[1].split()
        print(f'Adding STARTEND to query: {args}')
        self.startend = [part_start, part_end]

    @catch
    def do_find(self, args):
        words = args.split()
        if len(words) < 1: raise Exception("No search words provided")
        self.find = words
        print(f'Adding FIND to query: {args}')

    @catch
    def do_between(self, args):
        self.parse_dates(args)
        print(f'Adding BETWEEN to query: {args}')

    @catch
    def do_client(self, arg):
        client = arg.upper()
        print(f'Adding CLIENT to query: {client}')
        self.client = client

    @catch
    def do_sort(self, arg):
        self.sort = int(arg)
        print(f'Adding SORT to query: {arg}')

    def do_get_clients(self, arg):
        clients = self.queryParser.GetClients()
        print(f'Clients: {clients}')

    def do_show(self, args):
        print(self.Syntax(self.startend, self.find, self.between, self.client, self.sort))

    def do_run(self, arg):
        final_query = self.Syntax(self.startend, self.find, self.between, self.client, self.sort)
        print(final_query)
        self.execute_query(final_query)

    def execute_query(self, syntax):
        try:
            self.queryParser.Parse(syntax)
        except:
            print("Failed to execute query.")


if __name__ == "__main__":
    build = Build()
    build.cmdloop()
