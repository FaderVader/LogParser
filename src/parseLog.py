"""
get one log file, parse each line
add every word to shared Trie-structure
terminator is reference to {client, date, linenumber}

Lines should be cleaned:
lowercased
"""
from collections import namedtuple



class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.children = {}

class LogTrie():
    def __init__(self):
        self.root = Node()

    # Test
    Terminator = namedtuple("Terminator", "client date linenumber")

    def addWord(self, word, terminator='terminator'):
        def inner(word, node):
            if len(word) == 0:
                if node.value is None:
                    node.value = [terminator] 
                else:
                    temp = node.value
                    temp.append(terminator) #elements are concatenated: multiple hits are expected 
                    node.value = temp
                return
            elif word[0] not in node.children:
                newNode = Node(word[0])
                node.children[word[0]] = newNode
                return inner(word[1:], newNode)
            else: 
                return inner(word[1:], node.children[word[0]])
        return inner(word, self.root)
    
    def addLine(self, line, terminator='terminator'):
        words = line.split()
        for word in words:
            self.addWord(word, terminator)

    def addLog(self, logFile, terminator='terminator'):
        for linenumber, line in enumerate(logFile):
            text = line.GetPayLoad()
            lineId = (terminator[0], terminator[1], linenumber)
            self.addLine(text, lineId)
    
    def findWord(self, word):
        currentWord = word
        currentNode = self.root
        while len(currentWord) > 0:
            if currentWord[0] in currentNode.children:
                currentNode = currentNode.children[currentWord[0]]
                currentWord = currentWord[1:]
            else:
                return None
        return currentNode.value
            