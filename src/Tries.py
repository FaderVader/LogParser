"""
Build trie from logfile:
    - get one log file, parse each line
    - add every word to shared Trie-structure
        terminator is reference to {client, date, linenumber}

"""
from collections import namedtuple
import re


class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.children = {}


class LogTrie:
    def __init__(self):
        self.root = Node()

    # struct
    Terminator = namedtuple("Terminator", "client date linenumber")

    # actual trie builder
    def addWord(self, word, terminator):
        def inner(word, node):
            if len(word) == 0:
                if node.value is None:
                    node.value = [terminator] 
                else:
                    node.value.append(terminator) #elements are concatenated: multiple hits are expected 
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
        pattern = r'[()\[\]"\.:]'
        cleaned_line = re.sub(pattern, ' ', line.lower())

        words = cleaned_line.split()
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


class LogTrieSorted:
    def __init__(self):
        self.root = Node()

    # struct
    Terminator = namedtuple("Terminator", "client date linenumber")

    # actual trie builder
    def addWord(self, word, terminator):
        def inner(word, node):
            if len(word) == 0:
                if node.value is None:
                    node.value = [terminator] 
                else:
                    node.value.append(terminator)  # elements are concatenated: multiple hits are expected
                return
            elif word[0] not in node.children:
                newNode = Node(word[0])
                node.children[word[0]] = newNode
                return inner(word[1:], newNode)
            else: 
                return inner(word[1:], node.children[word[0]])
        return inner(word, self.root)

    def addLine(self, line, terminator):
        pattern = r'[()\[\]":]'
        cleaned_line = re.sub(pattern, ' ', line.lower())

        words = cleaned_line.split()
        for word in words:
            self.addWord(word, terminator)

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


class SearchTrie:
    def __init__(self):
        self.root = Node()
        self._sep = '.' # pointer elements delimimiter


    def pointer_as_string(self, pointer):
        return f'{pointer.client}{self._sep}{pointer.date}{self._sep}{pointer.linenumber}'
    

    def addPointer(self, pointer):
        pointer_as_string = self.pointer_as_string(pointer)

        def inner(pointer, node):
            if len(pointer) == 0:
                if node.value is None:
                    node.value = 1 # occured once 
                else:
                    node.value = node.value + 1 # inc up on every hit 
                return
            elif pointer[0] not in node.children:
                newNode = Node(pointer[0])
                node.children[pointer[0]] = newNode
                return inner(pointer[1:], newNode)
            else: 
                return inner(pointer[1:], node.children[pointer[0]])
        return inner(pointer_as_string, self.root)
    
    
    def findPointer(self, pointer):
        currentPointer = self.pointer_as_string(pointer)
        currentNode = self.root

        while len(currentPointer) > 0:
            if currentPointer[0] in currentNode.children:
                currentNode = currentNode.children[currentPointer[0]]
                currentPointer = currentPointer[1:]
            else:
                return None
        return currentNode.value