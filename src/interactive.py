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

        self.queryParser = QueryParser()
        self.init_vars()

        # always show help-text on startup
        self.show_help()

    def init_vars(self):
        """
        Build a set of variables, based on the methods defined in QueryParser
        """
        var_names = self.queryParser.query_methods
        for var in var_names:
            setattr(self, var, None)  # Initialize to None

    def catch(func):
        """
        Error-wrapper for query-building commands
        """
        def inner(*args):
            try:
                return func(*args)
            except AttributeError as e:
                print(f"AttributeError - failed to parse command: {e}")
            except ValueError as e:
                print(f"ValueError - failed to parse command: {e}")
            except:
                print("Failed to parse command")
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
            raise ValueError("No date arguments provided")

        parsed_dates = []
        for i, date in enumerate(dates):
            if date == "today" and i == 0:
                date = datetime.date.today().strftime("%Y-%m-%d") + "-0:0:0.0"
            if date == "today" and i == 1:
                date = datetime.date.today().strftime("%Y-%m-%d") + "-23:59:59.9"
            parsed_dates.append(date)
        return parsed_dates

    def build_query(self):  # init
        """
        Build a dict-object as argument to be passed to QueryParser.
        """
        var_names = self.queryParser.query_methods

        query_list = {}
        try:
            for var in var_names:
                value = self.__getattribute__(var)
                if value is not None:
                    query_list[var] = value

        except AttributeError as e:
            raise AttributeError(f'Build.build_query(): failed to parse key/value set: {e}')

        return query_list

    # cli commands - query build
    @catch
    def do_startend(self, args):
        parts = args.split(',')
        if len(parts) < 2: 
            raise ValueError("Must provide minimum 2 words separated by ,")
        part_start = parts[0].split()
        part_end = parts[1].split()
        setattr(self, 'StartEnd', [part_start, part_end])
        print(f'Adding STARTEND to query: {args}')

    @catch
    def do_find(self, args):
        words = args.split()
        if len(words) < 1: 
            raise ValueError("No search words provided")
        setattr(self, 'Find', words)
        print(f'Adding FIND to query: {words}')

    @catch
    def do_between(self, args):
        dates = self.parse_dates(args)
        setattr(self, 'Between', dates)
        print(f'Adding BETWEEN to query: {dates}')

    @catch
    def do_client(self, args):
        client = args.upper()
        setattr(self, 'Client', client)
        print(f'Adding CLIENT to query: {client}')

    @catch
    def do_sort(self, args):
        setattr(self, 'Sort', int(args))
        print(f'Adding SORT to query: {args}')

    @catch
    def do_stats(self, args):
        setattr(self, 'ShowStats', int(args))
        print('Adding SHOWSTATS to query')

    def do_get_clients(self, args):
        clients = self.queryParser.GetClients()
        print(f'Clients: {clients}')

    # cli commands - query management 
    def do_help(self, args):
        self.show_help()

    def do_reset(self, args):
        self.init_vars()

    def do_exit(self, args):
        print("Goodbye ....")
        sys.exit()

    def do_show(self, args):
        print(self.build_query())

    def do_run(self, args):
        final_query = self.build_query()
        self.execute_query(final_query)

    def execute_query(self, final_query):
        try:
            self.queryParser.Parse(final_query)
        except AttributeError as e:
            print(f"Failed to execute query - AttributeError: {e}")
        except ValueError as e:
            print(f"Failed to execute query - ValueError: {e}")
        except:
            print("Failed to execute query.")


if __name__ == "__main__":
    build = Build()
    build.cmdloop()
