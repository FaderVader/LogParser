import sys


class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


class BST:
    def __init__(self):
        self.root = None
        sys.setrecursionlimit(10**6)  # raises the ceiling - but we can still break it!

    # tree building
    def add(self, data):
        def searchTree(data, node):
            if data < node.data:
                if node.left is None:
                    node.left = Node(data)
                elif node.left is not None:
                    return searchTree(data, node.left)
            elif data > node.data:
                if node.right is None:
                    node.right = Node(data)
                    return
                elif node.right is not None:
                    return searchTree(data, node.right)
            else:
                return None

        node = self.root
        if node is None:
            self.root = Node(data)
            return
        else:
            return searchTree(data, node)

    def remove(self, value):
        def removeNode(node, value):
            if node is None: return None

            if value == node.data:
                if node.left is None and node.right is None:  # node has no children
                    return None

                # node has no left child
                if node.left is None:
                    return node.right

                # node has no right child
                if node.right is None:
                    return node.left

                # node has two children
                tempNode = node.right
                while tempNode.left is not None:
                    tempNode = tempNode.left
                node.data = tempNode.data
                node.right = removeNode(node.right, tempNode.data)
                return node

            elif value < node.data:
                node.left = removeNode(node.left, value)
                return node

            else:
                node.right = removeNode(node.right, value)
                return node

        self.root = removeNode(self.root, value)

    # tree introspection
    def isPresent(self, value):
        current = self.root
        while current is not None:
            if current.data == value:
                return True
            if current.data < value:
                current = current.right
            else:
                current = current.left
        return False

    def isPresent_recursive(self, value):
        def inner(node):
            if node.data == value:
                return True
            elif value < node.data and node.left is not None:
                return inner(node.left)
            elif value > node.data and node.right is not None:
                return inner(node.right)
            else:
                return False

        return inner(self.root)

    def findMin(self):
        current = self.root
        while current.left is not None:
            current = current.left
        return current.data

    def findMax(self):
        current = self.root
        while current.right is not None:
            current = current.right
        return current.data

    def minHeight(self, node=None):
        if node is None:
            node = self.root

        def findMinHeight(node):
            if node is None:
                return -1

            left = findMinHeight(node.left)
            right = findMinHeight(node.right)

            if left < right:
                return left + 1
            else:
                return right + 1
        return findMinHeight(node)

    def maxHeight(self, node=None):
        if node is None:
            node = self.root

        def findMaxHeight(node):
            if node is None:
                return -1

            left = findMaxHeight(node.left)
            right = findMaxHeight(node.right)

            if left > right:
                return left + 1
            else:
                return right + 1

        return findMaxHeight(node)

    def isBalanced(self):
        return self.minHeight() >= self.maxHeight() - 1

    # get tree-content
    def inOrder(self):
        if self.root is None: return None
        result = []

        def traverseInOrder(node):
            if node.left is not None: traverseInOrder(node.left)
            result.append(node.data)
            if node.right is not None: traverseInOrder(node.right)
        traverseInOrder(self.root)
        return result

    def preOrder(self):
        if self.root is None: return None
        result = []

        def traversePreOrder(node):
            result.append(node.data)
            if node.left is not None: traversePreOrder(node.left)
            if node.right is not None: traversePreOrder(node.right)
        traversePreOrder(self.root)
        return result

    def postOrder(self):
        if self.root is None: return None
        result = []

        def traversePostOrder(node):
            if node.left is not None: traversePostOrder(node.left)
            if node.right is not None: traversePostOrder(node.right)
            result.append(node.data)
        traversePostOrder(self.root)
        return result

    def levelOrder(self):
        result = []
        Q = []
        if self.root is not None:
            Q.append(self.root)

            while len(Q) > 0:
                node = Q[0]
                Q = Q[1:]
                result.append(node.data)
                if node.left is not None:
                    Q.append(node.left)
                if node.right is not None:
                    Q.append(node.right)

            return result
        else:
            return None
