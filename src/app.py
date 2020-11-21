from Query import Query
from PrepareTrie import PrepareTrie
from QueryParser import QueryParser


# Setup the tries
trie = PrepareTrie()

# load logs
loaded_trie = trie.GetLogTrie()

# get the files in structured format
logs = trie.GetStructuredLogs()

# setup the query
query = Query(loaded_trie, logs)

# setup query-parser
queryParser = QueryParser(query)
q = '{"find": ["setupsession", "running"], "between": ["2020-10-06-0:0:0.0", "2020-10-06-23:59:59.9"], "client": "TX82564"}'
q2 = '{"find": ["setupsession", "completed"], "between": ["2020-10-06-0:0:0.0", "2020-10-06-23:59:59.9"], "client": "TX82564"}'
queryParser.parse(q)
print('-------')
queryParser.parse(q2)  # must reset found items betweem queries


# perform query
# query.mustContainWords('SendEvent', 'StartGalaxy', 'Success', 'DALG2')
# query.mustContainWords('setupsession', "completed")  # "completed"  "running"
# query.mustBeAfter('2020-10-05-14:05:17.0')
# query.mustBeFore('2020-10-15-12:48:09.0')
# query.mustBeBetween('2020-10-05-14:05:17.0', '2020-10-15-12:48:09.0')
# query.mustBeBetween('2020-10-06-0:0:0.0', '2020-10-06-23:59:59.9')
# query.mustBeFromClient('TX82564')
# query.sortOnTime()

# query.showResults()

print('done')
