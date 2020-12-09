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

*GalaxySiteSelector-AX82017-20201001.log*              (appname-client-date.extension)

**{ client { logfile [ (timestamp, payload) ] } }** \

`clients = {"AX82017": {}, "AX82018": {}, "TX45046": {} }` # dict enforces uniqueness \
`file = {'20200101': [], '20200102': [], '20200103': []}`\
`lines = [(10, 'logline 1'), (20, 'logline 2'), (30, 'logline 2')]`  # (epoch timestamp, payload) 

**\# retrieve** \
`print(all_files['AX82017']['20201001'][123]) ` 

Prints line 123 from file 20200101 of client AX82017 

**Log trie**

On initialization, every available log-file is fed into the primary search-tool, a word-based trie-structure. For every completed word-boundary in a branch, the terminator-value is set to this pointer.

<img src="https://github.com/FaderVader/LogParser/blob/master/img/trie-tree_terminators.png?raw=true" alt="trie-tree_terminators.png" style="zoom:33%;" />

For every hit to same node, the new pointer is chained after the existing pointer.

**Search trie**

Search-trie is used for doing multiword-searches. For every word-hit, the returned pointer is serialized and added to a trie. Here, the terminator is the accumulated count of hits for every unique pointer. When retrieving, we grab all hits for the **first** search-word from the log-trie, and lookup this pointer in the search-trie. All values that match the count of search-words are added to result-list.

**Application structure**

The functionality of LogParser is manifested through a number of modules and classes. The application entry-point is `Shell`, which instantiates it's direct dependency, `QueryParser`, which in turn instantiates `Query`, etc. `Query` is responsible for orchestrating the tries, including the `BinarySearchTree` which is used for the sorting of results.

<img src="https://github.com/FaderVader/LogParser/blob/master/img/LogParser_Architecture_medium.png?raw=true" alt="LogParser_Architecture.png" style="zoom:33%;" />



### Running LogParser ###

LogParser does not rely on OS-specific libraries, and can be executed on *nix/windows system, by cloning the repository to your local machine, opening a terminal to the directory and executing python with `shell.py` as argument.

**How to use**

When the application is started, and all logs are loaded (currently from /testSources), the shell-prompt shows `LogParser>`

From the prompt, you add the query-components that you need:

`find daletservice running` will add the words "daletservice", "running" to the list of criteria for a positive match.

`client ax82017` will limit results to be only from client AX82017.

`startend SendEvent DaletService Waiting, SendEvent DaletService Success` will search for a pattern where a line contains the first set of words, and a later line must match the second set of words. `startend` and `find` are mutually exclusive, so defining one will remove the other from the active query.

`sort true` will ensure all results are returned sorted ascending according to time.

`stats 3` will instruct the application to show results as a bottom/top 3, measured by the interval/delta time between first set and second set of startend matches. It will also display the average across all hits.

`get_clients` will either display all clients in current set of log-files, or, if a search has been run, the clients in current result-set.

`run`		    Execute the active query \
`show`		  Display the currently active query \
`reset` 	   Reset all parameters \
`help`		  Display help-hints \
`exit`		  Exit the application 



## Technology ##

**Trie**

2 discreet tries are used in LogParser. Trie/LogTrie contains pointers to every occurence of any word found in any log-file. Trie/SearchTrie is used for keeping track of word-hits when searching for multiple words. 

**LogTrie** uses Terminators for word-boundary demarcation. A Terminator defines a reference to the originating client, the date of the logfile, and the line where the match was found. The terminator is serialized, and multiple hits are concatenated.

**SearchTrie** uses same methodology, only the terminators are integers.



**Binary Search Tree**

The BST is currently only used for sorting the results according to time. We use the In Order traversal of tree-nodes to acquire the sorted set.



**eDSL**

`Shell` invokes `QueryParser` via JSON data-sets. The JSON is built by `Shell` when the user request to run a search. The `Shell` uses a set of commands and associated arguments to assemble the query.



### Next Step ###

In the current implementation, LogParser relies on it's data-sources being present locally. The capability to acquire the log-files directly from the pool of application-hosts (clients) is an obvious next step. The target-application can be queried via a REST interface, so acquisition over REST is simple.



