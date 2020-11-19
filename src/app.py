from Query import Query
from PrepareTrie import PrepareTrie


# Setup the tries
trie = PrepareTrie()

# load logs  
loaded_trie = trie.GetLogTrie()

# get the files in structured format
logs = trie.GetStructuredLogs()

# setup the query
query = Query(loaded_trie, logs)

# perform query
query.mustContainWords('SendEvent', 'StartGalaxy', 'Success', 'DALG2')
# query.mustBeAfter('2020-10-05-14:05:17.0')
# query.mustBeFore('2020-10-15-12:48:09.0')
# query.mustBeBetween('2020-10-05-14:05:17.0', '2020-10-15-12:48:09.0')
query.mustBeFromClient('TX82564')
query.sortOnTime()

# query.showResults()

print('done')