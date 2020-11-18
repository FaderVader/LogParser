from Query import Query
from PrepareTrie import PrepareTrie


"""
This is bad structure - with a 3rd-party reference shared between two classes
Refactor for higher cohesion!
"""
trie = PrepareTrie()
loaded = trie.LoadLogs()
logs = trie.GetStructuredLogs()
query = Query(loaded)
query.mustContainWords('SendEvent', 'StartGalaxy', 'Success', 'DALG0')
query.ShowResults(logs)

print('done')