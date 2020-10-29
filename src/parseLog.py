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

    # struct
    Terminator = namedtuple("Terminator", "client date linenumber")

    # actual trie parser
    def addWord(self, word, terminator):
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
    
    # format to words
    def addLine(self, line, terminator):
        words = line.split()
        for word in words:
            self.addWord(word, terminator)

    # get file and split into lines
    def addLog(self, logFile, terminator=Terminator('*', '*', '*')): 
        for linenumber, line in enumerate(logFile):
            text = line.GetPayLoad()
            lineId = self.Terminator(terminator.client, terminator.date, linenumber)
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
            