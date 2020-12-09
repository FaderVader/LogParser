# LogParser (prototype)
##  A tool for Application Insights ##



### Project description ###

The goal of the LogParser-project is to create a python-based application that will let its user parse the combined daily log-output from many hundred instances of a critical target-application and extract statistical data from these logs.

The intended users of LogParser is the team supporting the users of the target-application.
The project is currently developed to a prototype-stage.

### Getting Results ###

Examples of useful output from LogParser:

**Usage stats:** 

- How long is the average session?

- Min, Max, Average response-times for target-application service-restart

**App Health:**

- what are the most frequent errors generated by the target-app?
- Top 10 clients with fatal errors

### Interactive shell ###

The application is accessed via a command line interface, used for building queries. At startup, all log-files are loaded and a brief help-screen outlines available commands. When a query is executed, the application will query the data-structure, and present the results in the shell as printed lines.

### Application Structure ###

**Internal data representation**

All loaded log-files are contained in a single datastructure, consisting of nested dictionarys and lists. \
The filename of the logs are indicative of this structure:

GalaxySiteSelector-AX82017-20201001.log    (appname-client-date.extension)

**{ client { logfile [ (timestamp, payload) ] } }** \

`clients = {"AX82017": {}, "AX82018": {}, "TX45046": {} }` # dict enforces uniqueness \
`file = {'20200101': [], '20200102': [], '20200103': []}`\
`lines = [(10, 'logline 1'), (20, 'logline 2'), (30, 'logline 2')]`  # (epoch timestamp, payload) 

**\# retrieve** \
`print(all_files['AX82017']['20201001'][123]) ` 

Prints line 123 from file 20200101 of client AX82017 

**Log trie**

On initialization, every available log-file is fed into the primary search-tool, a word-based trie-structure. For every completed word-boundary in a branch, the terminator-value is set to this pointer.

[trie-tree_terminators.png]

For every hit to same node, the new pointer is chained after the existing pointer.

**Search trie**

Search-trie is used for doing multiword-searches. For every word-hit, the returned pointer is serialized and added to a trie. Here, the terminator is the accumulated count of hits for every unique pointer. When retrieving, we grab all hits for the **first** search-word from the log-trie, and lookup this pointer in the search-trie. All values that match the count of search-words are added to result-list.

**Application structure**

The functionality of LogParser is manifested through a number of modules and classes. The application entry-point is `Shell`, which instantiates it's direct dependency, `QueryParser`, which in turn instantiates `Query`, etc. Query is main-class for orchestrating the tries, including the Binary Search Tree which handles the sorting of results.

[LogParser_Architecture.png]



### Running LogParser ###

LogParser does not rely on OS-specific libraries, and can be executed on *nix/windows system, by cloning the repository to your local machine, opening a terminal to the directory and executing python with `shell.py` as argument.



### Next Step ###

In the current implementation, LogParser relies on it's data-sources being present locally. The capability to acquire the log-files directly from the pool of application-hosts (clients) is an obvious next step. The target-application can be queried via a REST interface, so acquisition over REST is simple.



