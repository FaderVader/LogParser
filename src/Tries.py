from Types import Terminator as Terminator
from Utils import TermUtil as TermUtil
import re


class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.children = {}


class LogTrie:
    """
    Main container for content of all log-files.
    Build trie from logfile:
    - get one log file, parse each line
    - add every word to shared Trie-structure
    Terminator is reference to {client, date, linenumber, (payload)}
    """
    def __init__(self):
        self.root = Node()

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

    # clean, filter and split to words
    def addLine(self, line, terminator):
        pattern = r'[()\[\]"\.:,]'  # filter out these characters
        cleaned_line = re.sub(pattern, ' ', line.lower())
        words = cleaned_line.split()
        [self.addWord(word, terminator) for word in words]

    def AddLog(self, logFile, terminator=Terminator('*', '*', '*', None)):
        """
        Takes a log-file as argument and split into lines.\n
        The terminator-items should be: [client][filedate]
        - Linenumber identifier will be added during line-by-line parsing.
        """
        for linenumber, line in enumerate(logFile):
            text = line.GetPayLoad()
            lineId = Terminator(terminator.client, terminator.date, linenumber, None)
            self.addLine(text, lineId)

    def FindWord(self, word):
        """
        Return all matches for search-word as pointers.
        """
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
    """
    Container for all pointers - is used for counting occurrences of search-phrase within a pointer.\n
    We use SearchTrie for counting multi-word hits on a line.
    """
    def __init__(self):
        self.root = Node()

    def AddPointer(self, pointer):
        pointer_as_string = TermUtil.ToString(pointer)

        def inner(pointer, node):
            if len(pointer) == 0:
                if node.value is None:
                    node.value = 1  # first occurence
                else:
                    node.value = node.value + 1  # increment on every following hit
                return
            elif pointer[0] not in node.children:
                newNode = Node(pointer[0])
                node.children[pointer[0]] = newNode
                return inner(pointer[1:], newNode)
            else:
                return inner(pointer[1:], node.children[pointer[0]])
        return inner(pointer_as_string, self.root)

    def FindPointer(self, pointer):
        """
        Returns the number of hits accumulated for the specified pointer-parameter.
        """
        currentPointer = TermUtil.ToString(pointer)
        currentNode = self.root

        while len(currentPointer) > 0:
            if currentPointer[0] in currentNode.children:
                currentNode = currentNode.children[currentPointer[0]]
                currentPointer = currentPointer[1:]
            else:
                return None
        return currentNode.value  
