import uuid
import copy
from .fact import fact_equation

class Node:
    def __init__(self, fact, relation, parent=None):
        self.id = str(uuid.uuid4())
        self.fact = fact
        self.relation = relation # record the last relation
        self.parent = None
        self.children = []
        self.reward = 0

    def __str__(self):
        return str((self.relation, self.fact))

class Tree:
    def __init__(self, root = None):
        self.tree = {} # this is a node dictionary for the tree
        self.root = Node(None, "none")
        self.tree[self.root.id] = self.root

    def getRoot(self):
        return self.root

    def getLeaves(self):
        nodes = self.tree.values()
        leaves = list(filter(lambda x:len(x.children)==0, nodes))
        return leaves

    def addChild(self, parent, child):
        if parent.id not in self.tree:
            return False
        elif self.existInPath(parent, child):
            return False
        else:
            child.parent = parent.id
            self.tree[child.id] = child
            self.tree[parent.id].children.append(child.id)
            return True

    def getChildren(self, node):
        children = list(map(lambda x:self.tree[x], node.children))
        return children

    def bestnode(self):
        return self.bestchild(self.root)

    def bestleaf(self):
        leaves = self.getLeaves()
        best_leaf = max(leaves, key=lambda x:x.reward)
        return best_leaf

    def bestchild(self, parent):
        children = self.getChildren(parent)
        if len(children) == 0:
            return parent
        else:
            best = parent
            for node in children:
                node_child = self.bestchild(node)
                if node_child.reward >= best.reward:
                    best = node_child
            return best

    def path(self, node):
        if node.id not in self.tree or node.fact is None:
            return []
        else:
            path = [copy.deepcopy(node)]
            while node.parent is not None:
                node = self.tree[node.parent]
                path.insert(0, copy.deepcopy(node))
            return path[1:]

    def bestpath(self):
        best_leaf = self.bestleaf()
        best_path = self.path(best_leaf)
        return best_path

    def existInPath(self, parent, child):
        path = self.path(parent)
        for node in path:
            if fact_equation(node.fact, child.fact):
                return True
        return False
                
    def update(self, node):
        while node.parent is not None:
            parent = self.tree[node.parent]
            parent.reward = max(parent.reward, node.reward)
            node = parent
            