# LogParser

##  Generate Stats & Application insights ##



### Project description ###

The goal of the LogParser-project is to create a python-based application that will let a user parse the log-output from many hundred instances of an certain other application and extract statistical data from these logs.

The intended users of LogParser is the team supporting the users of the target-application.

We want LogParser to generate reports that will show and highlight key performance aspects of the target-application. These data are generated by parsing several hundred log-files, generated by daily users across a large IT-centric organisation.

The reports we're looking to generate, must offer us insights into the health of the installed base of the target application. We want to present the user with relevant statistical **Key Performance Indicators**, that helps the user offer relevant support, and understand the current state of the target-application across all the installed instances, and the associated usage-patterns.

The target-application is a "configuration-handler" that serves as a user-facing tool to manage how to logon to a radio-production application, in a "boot-strapping" fashion.

### Report Generator ###

The output from LogParser should be reports, which can contain a mix of text and graphical representation of KPI data.

We're looking for data such as:

**Usage stats:** 

- how many times per day are users starting and interacting with the app?

- How long is the average session?

- Min, Max, Average response-times for target-application service-restart

**App Health:**

- what are the most frequent errors generated by the target-app?
- How is the distribution of errors related to time-of-day?
- Top 10 clients with fatal errors

### Data ###

The target-app will respond to REST-queries, and return requested data. The log-data should be fetched via REST, by querying all instances of target-app and request they submit all log-files. LogParser should only acquire new-to-it files, or log-files updated since last run.



### Data - Internal structure and representation ###

**{ client { logfile [ timestamp, payload ] } }** \
`clients = {"AX82017": {}, "AX82018": {}, "TX45046": {} }` # dict enforces uniqueness \
`file = {'file1': [], 'file2': [], 'file3': []}`\
`lines = [(10, '10-lines'), (20, '20-lines'), (30, '30-lines')]`  # (timestamp, payload) \

**\# assignment** \
`clients['AX82018'] = file` \
`clients['AX82018']['file2'] = lines` \

**\# retrieve** \
`print(clients['AX82018']['file2']) ` \



### Development agenda - Tech ###

In order to get useful stats from the log-file collection, I expect to use various sorting and tree-search algorithms to generate the reports.



### Development agenda - Slices ###

The first 4 sub-goals of the initial development phase can be identified so:

####  Phase 1 ####

- Using local files as source. 
- Represent logs as one list pr. client. 
- Parse timestamp of each log-line into epoch. 
- Make text-part searchable and demonstrate simple text-pattern search

####  Phase 2 ####  

- Be able to generate report on statistics of service-interaction on target-app.
- Min, Max, Average response times across all sampled logs.

####  Phase 3 ####  

- MVP: Be able to generate additional text-based reporting, on critical KPI's as described above.

- Nice-to-have: generate a number of graphics-based reports.

####  Phase 4 ####

- Implement logfile acquisition from clients via REST