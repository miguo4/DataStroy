from .tree import Tree, Node
from .factfactory import FactFactory
import time
import copy
import math
import random
import datetime
import json
import jsonpickle
from .fact import fact2relation, fact2prerelation
from .data import check_coverage

class Generator:
    def __init__(self, df, schema, goal, reward, factory, tree = None, story = []):

        # data frame & schema
        self.df = df
        self.schema = schema

        # search goal: length & information & timelimit
        self.G = goal

        # reward paramters
        self.gamma1 = reward['logicality']
        self.gamma2 = reward['diversity']
        self.gamma3 = reward['integrity']

        # search tree
        if tree is None:
            self.T = Tree()
        else:
            self.T = tree

        # factory
        self.factory = factory

        # the optimal story
        self.S = story

    # 
    # generate a story via MCTS
    # steplimit: the maximum time cost on each simulation
    # scale : expanding scale
    #
    def generate(self, scale = 1000):

        steplimit = self.G['limit']
        
        iteration = 0
        # iteratively searching the data space
        while not self._fullfilled(self.S):
            # 1.Selection
            node = self.select(self.T)
            # 2.Expansion
            nodes = self.expand(node, scale)
            if len(nodes) == 0:
                continue
            # 3.Simulation
            opt_node = self.simulate(node, nodes, steplimit)
            # 4.BackPropagation
            success = self.T.addChild(node, opt_node)
            if success:
                self.backpropogation(self.T, opt_node)
            # Pick best path
            self.S = self.T.bestpath()

            print("iteration: %s, length: %s"%(iteration, len(self.S)))
            iteration += 1

        return self._jsonify(self.S)

    def generateIteratively(self, scale = 1000):

        steplimit = self.G['limit']
        
        if not self._fullfilled(self.S):
            # 1.Selection
            node = self.select(self.T)
            # 2.Expansion
            nodes = self.expand(node, scale)
            if len(nodes) == 0:
                #TODO: cannot expand anymore
                tree = jsonpickle.encode(self.T)
                return self._jsonify(self.S), tree
            # 3.Simulation
            opt_node = self.simulate(node, nodes, steplimit)
            # 4.BackPropagation
            success = self.T.addChild(node, opt_node)
            if success:
                self.backpropogation(self.T, opt_node)
            # Pick best path
            self.S = self.T.bestpath()

        # tree = json.dumps(self.T.tree)
        tree = jsonpickle.encode(self.T)

        return self._jsonify(self.S), tree

    # 
    # select a fact in the search tree with the largest reward
    # 
    def select(self, T):
        return T.bestnode()

    #
    # expand facts based on logic
    #
    def expand(self, node, scale = 1000):
        nodes = []
        fact = node.fact
        if fact is None:
            # initial facts
            facts = self.factory.createByInitialation()
            for newfact in facts:
                newnode = Node(newfact, "none")
                # rel_nodes.append(newnode)
                # if len(rel_nodes) >= rel_count:
                #     break
                nodes.append(newnode)
        else:
            # other facts
            rel_probability = fact2relation[fact['type']]
            for rel in rel_probability:
                probability = rel_probability[rel]
                rel_nodes = []
                rel_count = int(probability * scale)
                facts = self.factory.createByLogic(fact, rel)
                random.shuffle(facts)
                for newfact in facts:
                    newnode = Node(newfact, rel)
                    if self.T.existInPath(node, newnode):
                        continue
                    rel_nodes.append(newnode)
                    if len(rel_nodes) >= rel_count:
                        break
                nodes += rel_nodes

        return nodes

    #
    # look a few steps furthure in a simulation tree to find the best searching direction
    #
    def simulate(self, focus, candidates, timelimit):

        tmp_root = copy.deepcopy(focus)
        tmp_root.parent = None
        tmp_tree = Tree(tmp_root)
        tmp_focus = focus
        tmp_candidates = copy.deepcopy(candidates)
        opt_node = candidates[0]
        t = time.time()
        
        while time.time() - t < timelimit/1000:
            
            tmp_opt_node = self._getOptNode(tmp_tree, tmp_focus, tmp_candidates)

            tmp_tree.addChild(tmp_focus, tmp_opt_node)
            self.backpropogation(tmp_tree, tmp_opt_node)

            # find the best candidate based on the new reward
            for candidate in candidates:
                if opt_node.reward < candidate.reward:
                    opt_node = candidate
                
            tmp_focus = self.select(tmp_tree)

            tmp_candidates = self.expand(tmp_focus)

        return opt_node

    #
    # update the reward score and add the node in the tree
    # return the fact with the best reward in the tree
    #
    def backpropogation(self, tree, node):
        tree.update(node)

    # 
    # Calculate the reward score
    #
    def reward(self, story):
        storylength = len(story)
        if storylength < 1:
            return 0

        facts = list(map(lambda x:x.fact, story))
        relations = list(map(lambda x:x.relation, story))

        total_importance_score = 0
        total_logic_score = 0
        fact_types = []
        fact_type_dict = {}

        for index, fact in enumerate(facts):
            # importance
            total_importance_score += fact['possibility'] * fact['score']
            # logic
            logic_score = 0
            if index != 0:
                logic_score = fact2prerelation[fact['type']][relations[index]]
            total_logic_score += logic_score
            # fact type
            fact_types.append(fact['type'])
            if fact['type'] in fact_type_dict:
                fact_type_dict[fact['type']] += 1
            else:
                fact_type_dict[fact['type']] = 1

        # Importance
        importance = total_importance_score

        # Logicality
        w1 = self.gamma1
        logicality = 0
        if storylength > 1:
            avg_logic_score = total_logic_score/(storylength-1)
            logicality = avg_logic_score

        # Diversity: normalized Shannon's diversity index
        w2 = self.gamma2
        fact_type_count = len(set(fact_types))
        nSDI = 1
        if fact_type_count > 1:
            # \hat{H}=-\frac{\sum_{j=1}^{i} \hat{p}_{j} \cdot \ln \left(\hat{p}_{j}\right)}{\ln (s)}
            N = len(fact_types)
            H = 0
            for key in fact_type_dict:
                n = fact_type_dict[key]
                H -= (float(n)/N) * math.log(float(n)/N)
            s = len(set(fact_types))
            nSDI = H / math.log(s)
        storylength_cut = storylength
        if storylength_cut > 10:
            storylength_cut = 10
        diversity = ( fact_type_count / storylength_cut ) * nSDI

        # Integrity
        w3 = self.gamma3
        integrity = check_coverage(facts, self.schema, self.df)

        reward = (w1*logicality + w2*diversity + w3*integrity) * importance
        # return reward
        return importance

    def _getStory(self, tree, node):
        path = tree.path(node)
        return path

    def _getOptNode(self, T, focus, nodes):
        opt_node = None
        reward = 0
        story = T.path(focus)
        for node in nodes:
            newstory = copy.deepcopy(story)
            newstory.append(node)
            node.reward = self.reward(newstory)
            if node.reward > reward:
                opt_node = node
        return opt_node

    def _fullfilled(self, story):
        if len(story) < self.G['length']:
            return False
        # TODO: info goal
        # I = 0
        # for node in story:
        #     I += node.fact['possibility'] * node.fact['score']
        # if I < self.G['info']:
        #     return False
        return True

    def _jsonify(self, story):
        facts = list(map(lambda x:x.fact, story))
        relations = list(map(lambda x:x.relation, story))
        for fact in facts:
            for i, focus in enumerate(fact['focus']):
                # if isinstance(focus['value'], datetime.datetime) or not isinstance(focus['value'], str):
                if isinstance(focus['value'], datetime.datetime):
                    date_text = str(focus['value'])[:10]
                    date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
                    fact['focus'][i]['value'] = "%s/%s/%s"%(date.year,date.month,date.day)
                else:
                    fact['focus'][i]['value'] = str(fact['focus'][i]['value'])
            for i, subspace in enumerate(fact['subspace']):
                # if isinstance(subspace['value'], datetime.datetime) or not isinstance(subspace['value'], str):
                if isinstance(focus['value'], datetime.datetime):
                    date_text = str(subspace['value'])[:10]
                    date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
                    fact['subspace'][i]['value'] = "%s/%s/%s"%(date.year,date.month,date.day)
                else:
                    fact['subspace'][i]['value'] = str(fact['subspace'][i]['value'])
        output = {
            'coverage': check_coverage(facts, self.schema, self.df),
            'relations': relations,
            'facts': facts
        }
        return output
