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
query.mustContainWords('SendEvent', 'StartGalaxy', 'Success', 'DALG0')
query.ShowResults()

print('done')