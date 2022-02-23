import random
import itertools
from copy import copy, deepcopy
from sentence_transformers import  util
from .fact import Fact
from flask import current_app
from ..fact import *
import traceback
from gensim.parsing.preprocessing import remove_stopwords
import nltk
from flask import current_app
import numpy as np
from scipy.spatial import distance
class FactSearch():
    def __init__(self, schema, df, search_size, mentioned_fields = []):
        self.schema = schema
        self.df = df
        self.search_size = search_size

        self.mentioned_fields = list(map(lambda x: {"field":x, "type":self.schema.field2type[x]}, mentioned_fields))
        self.mentioned_fields_n = list(filter(lambda x: x['type'] == "numerical", self.mentioned_fields))
        self.mentioned_fields_c = list(filter(lambda x: x['type'] == "categorical", self.mentioned_fields))
        self.mentioned_fields_t = list(filter(lambda x: x['type'] == "temporal", self.mentioned_fields))
        self.mentioned_fields_g = list(filter(lambda x: x['type'] == "geographical", self.mentioned_fields))

        fields = list(map(lambda x: {"field":x, "type":self.schema.field2type[x]}, self.schema.fields))
        self.other_fields = list(filter(lambda x: x not in mentioned_fields, fields))
        self.other_fields_n = list(filter(lambda x: x['type'] == "numerical", self.other_fields))
        self.other_fields_c = list(filter(lambda x: x['type'] == "categorical", self.other_fields))
        self.other_fields_t = list(filter(lambda x: x['type'] == "temporal", self.other_fields))
        self.other_fields_g = list(filter(lambda x: x['type'] == "geographical", self.other_fields))

    def search(self, question, fact_type, canadiate_size):
        if fact_type == "association":
            facts = self.__search_association(question, canadiate_size)
        elif fact_type == "categorization":
            facts = self.__search_categorization(question, canadiate_size)
        elif fact_type == "difference":
            facts = self.__search_difference(question, canadiate_size)
        elif fact_type == "distribution":
            facts = self.__search_distribution(question, canadiate_size)
        elif fact_type == "extreme":
            facts = self.__search_extreme(question, canadiate_size)
        elif fact_type == "outlier":
            facts = self.__search_outlier(question, canadiate_size)
        elif fact_type == "proportion":
            facts = self.__search_proportion(question, canadiate_size)
        elif fact_type == "rank":
            facts = self.__search_rank(question, canadiate_size)
        elif fact_type == "trend":
            facts = self.__search_trend(question, canadiate_size)
        elif fact_type == "value":
            facts = self.__search_value(question, canadiate_size)

        facts = list(filter(lambda x:x.is_fullfilled(), facts))  
                
        return [x.__dict__ for x in facts]


    def __similarity_ByParallel(self, question, factlist):
        
        """Measure the similarity between the question and the facts

        Reference: https://github.com/UKPLab/sentence-transformers/blob/55756adf20ac61e1f5a9e931e1cb9645ee0e79fb/sentence_transformers/SentenceTransformer.py

        Args:
            question (String): a question
            factlist (Fact): a list of facts

        Returns:
            a list of float: every element represent the degree of the similarity (from 0 to 1)
        """ 
        try:
            sentences1 = [question]
            question_embeddings = current_app.sentence_bert.encode(sentences1)
            fact_sentenceslist = [fact.to_sentence() for fact in factlist]
            pool = current_app.sentence_bert.start_multi_process_pool(target_devices = current_app.device)
            fact_embeddingslist = current_app.sentence_bert.encode_multi_process(fact_sentenceslist, pool)
        except Exception as e:
            print(traceback.format_exc(),flush=True)
            print('cannot parallel embedding the sentence', flush=True)
            pass
        #Compute cosine-similarits
        cosine_scoreslist = []
        for sentence_embedding in fact_embeddingslist:
            try:
                cosine_scoreslist.append(util.pytorch_cos_sim(question_embeddings, sentence_embedding).item())
            except Exception as e:
                print(traceback.format_exc(),flush=True)
                print('cannot cosine', flush=True)
                cosine_scoreslist.append(-1)
            
        return cosine_scoreslist


    def __similarity(self, question, fact):
        """Measure the similarity between the question and the fact

        Reference: https://www.sbert.net/docs/usage/semantic_textual_similarity.html

        Args:
            question (String): a question
            fact (Fact): a fact

        Returns:
            float: the degree of the similarity (from 0 to 1)
        """ 
        try:
            sentences1 = [question]
            sentences2 = [fact.to_sentence()]
            embeddings1 = current_app.sentence_bert.encode(sentences1, convert_to_tensor=True)
            embeddings2 = current_app.sentence_bert.encode(sentences2, convert_to_tensor=True)

            #Compute cosine-similarits
            cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)

            return cosine_scores.item()
            
        except Exception as e:
            return -1

    def __similarity_word2vec(self, question, fact, num_features = 300):
        """Measure the similarity between the question and the fact by word2vec

        Args:
            question (String): a question
            fact (Fact): a fact

        Returns:
            float: the degree of the similarity (from 0 to 1)
        """ 
        sentences1 = remove_stopwords(question)
        sentences2 = remove_stopwords(fact.to_sentence())

        words1 = nltk.word_tokenize(sentences1)
        words2 = nltk.word_tokenize(sentences2)
        sentence1_vector = np.zeros((num_features,), dtype="float32")
        sentence2_vector = np.zeros((num_features,), dtype="float32")
        nwords1 = 0
        for word in words1:
            try:
                vector = current_app.word2vec[word]
                sentence1_vector = np.add(sentence1_vector, vector)
                nwords1 += 1
            except:
                pass
            
        nwords2 = 0
        for word in words2:
            try:
                vector = current_app.word2vec[word]
                sentence2_vector = np.add(sentence2_vector, vector)
                nwords2 += 1
            except:
                pass
        
        try:
            sentence1_vector = np.divide(sentence1_vector, nwords1)
            sentence2_vector = np.divide(sentence2_vector, nwords2)
            score = 1 - distance.cosine(sentence1_vector,sentence2_vector)
        except:
            score = -1
        
        return score


    def __search_association(self, question, canadiate_size):
        # 'association': ["measure1", "measure2", "breakdown", "subspace"]
        original_fact = Fact(type="association")
        candidates = [original_fact]

        # step 1: search measure
        mentioned_measure_fields = self.mentioned_fields_n
        if len(mentioned_measure_fields) > 1:
            candidates = self.__search_measure_2(question, candidates, mentioned_measure_fields, canadiate_size)
        else:
            return []

        # step 2: search breakdown
        mentioned_breakdown_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(mentioned_breakdown_fields) > 0:
            candidates = self.__search_breakdown(question, candidates, mentioned_breakdown_fields, canadiate_size)

        # step 3: search subspace
        potential_subspace_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(potential_subspace_fields) > 1:
            candidates = self.__search_subspace(question, candidates, potential_subspace_fields, canadiate_size)
        
        
        return candidates

    def __search_categorization(self, question, canadiate_size):
        # 'categorization': ["breakdown", "subspace"]
        original_fact = Fact(type="categorization")
        candidates = [original_fact]

        # step 1: search breakdown
        mentioned_breakdown_fields = self.mentioned_fields_c + self.mentioned_fields_g
        if len(mentioned_breakdown_fields) > 0:
            candidates = self.__search_breakdown(question, candidates, mentioned_breakdown_fields, canadiate_size)
        else:
            return []
        
        # step 2: search subspace
        potential_subspace_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(mentioned_breakdown_fields) > 1:
            candidates = self.__search_subspace(question, candidates, potential_subspace_fields, canadiate_size)
        
        return candidates

    def __search_difference(self, question, canadiate_size):
        # 'difference': ["measure", "breakdown", "subspace", "focus1", "focus2"]
        original_fact = Fact(type="difference")
        candidates = [original_fact]

        # step 1: search measure
        mentioned_measure_fields = self.mentioned_fields_n
        if len(mentioned_measure_fields) > 0:
            candidates = self.__search_measure(question, candidates, mentioned_measure_fields, canadiate_size)
        else:
            return []

        # step 2: search breakdown
        mentioned_breakdown_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(mentioned_breakdown_fields) > 0:
            candidates = self.__search_breakdown(question, candidates, mentioned_breakdown_fields, canadiate_size)
        else:
            return []
        
        # step 3: search subspace
        potential_subspace_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(potential_subspace_fields) > 1:
            candidates = self.__search_subspace(question, candidates, potential_subspace_fields, canadiate_size)
        # step 4: : search focus
        candidates = self.__search_focus_difference(question, candidates, canadiate_size)
        return candidates

    def __search_distribution(self, question, canadiate_size):
        # 'distribution': ["measure", "breakdown", "subspace"]
        original_fact = Fact(type="distribution")
        candidates = [original_fact]

        # step 1: search measure
        mentioned_measure_fields = self.mentioned_fields_n
        if len(mentioned_measure_fields) > 0:
            candidates = self.__search_measure(question, candidates, mentioned_measure_fields, canadiate_size)
        else:
            return []

        # step 2: search breakdown
        mentioned_breakdown_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(mentioned_breakdown_fields) > 0:
            candidates = self.__search_breakdown(question, candidates, mentioned_breakdown_fields, canadiate_size)
        else:
            return []
        
        # step 3: search subspace
        potential_subspace_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(potential_subspace_fields) > 1:
            candidates = self.__search_subspace(question, candidates, potential_subspace_fields, canadiate_size)
        
        return candidates

    def __search_extreme(self, question, canadiate_size):
        # 'extreme': ["measure", "breakdown", "subspace", "focus"]
        original_fact = Fact(type="extreme")
        candidates = [original_fact]

        # step 1: search measure
        mentioned_measure_fields = self.mentioned_fields_n
        if len(mentioned_measure_fields) > 0:
            candidates = self.__search_measure(question, candidates, mentioned_measure_fields, canadiate_size)
        else:
            return []

        # step 2: search breakdown
        mentioned_breakdown_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(mentioned_breakdown_fields) > 0:
            candidates = self.__search_breakdown(question, candidates, mentioned_breakdown_fields, canadiate_size)
        else:
            return []
        
        # step 3: search subspace
        potential_subspace_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(potential_subspace_fields) > 1:
            candidates = self.__search_subspace(question, candidates, potential_subspace_fields, canadiate_size)

        # step 4: : search focus
        candidates = self.__search_focus_outlier_extreme(question, self.df, candidates, canadiate_size)
        
        return candidates

    def __search_outlier(self, question, canadiate_size):
        # 'outlier': ["measure", "breakdown", "subspace", "focus"]
        original_fact = Fact(type="outlier")
        candidates = [original_fact]

        # step 1: search measure
        mentioned_measure_fields = self.mentioned_fields_n
        if len(mentioned_measure_fields) > 0:
            candidates = self.__search_measure(question, candidates, mentioned_measure_fields, canadiate_size)
        else:
            return []

        # step 2: search breakdown
        mentioned_breakdown_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(mentioned_breakdown_fields) > 0:
            candidates = self.__search_breakdown(question, candidates, mentioned_breakdown_fields, canadiate_size)
        else:
            return []
        
        # step 3: search subspace
        potential_subspace_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(potential_subspace_fields) > 1:
            candidates = self.__search_subspace(question, candidates, potential_subspace_fields, canadiate_size)

        # step 4: : search focus
        candidates = self.__search_focus_outlier_extreme(question, self.df, candidates, canadiate_size)
        
        return candidates

    def __search_proportion(self, question, canadiate_size):
        # 'proportion': ["measure", "breakdown", "subspace", "focus"]
        original_fact = Fact(type="proportion")
        candidates = [original_fact]

        # step 1: search measure
        mentioned_measure_fields = self.mentioned_fields_n
        if len(mentioned_measure_fields) > 0:
            candidates = self.__search_measure(question, candidates, mentioned_measure_fields, canadiate_size)
        else:
            return []

        # step 2: search breakdown
        mentioned_breakdown_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(mentioned_breakdown_fields) > 0:
            candidates = self.__search_breakdown(question, candidates, mentioned_breakdown_fields, canadiate_size)
        else:
            return []
        
        # step 3: search subspace
        potential_subspace_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(potential_subspace_fields) > 1:
            candidates = self.__search_subspace(question, candidates, potential_subspace_fields, canadiate_size)

        # step 4: search focus
        candidates = self.__search_focus(question, candidates, canadiate_size)
        
        return candidates

    def __search_rank(self, question, canadiate_size):
        # 'rank': ["measure", "breakdown", "subspace"]
        original_fact = Fact(type="rank")
        candidates = [original_fact]

        # step 1: search measure
        mentioned_measure_fields = self.mentioned_fields_n
        if len(mentioned_measure_fields) > 0:
            candidates = self.__search_measure(question, candidates, mentioned_measure_fields, canadiate_size)
        else:
            return []

        # step 2: search breakdown
        mentioned_breakdown_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(mentioned_breakdown_fields) > 0:
            candidates = self.__search_breakdown(question, candidates, mentioned_breakdown_fields, canadiate_size)
        else:
            return []
        
        # step 3: search subspace
        potential_subspace_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(potential_subspace_fields) > 1:
            candidates = self.__search_subspace(question, candidates, potential_subspace_fields, canadiate_size)
        
        return candidates

    def __search_trend(self, question, canadiate_size):
        # 'trend': ["measure", "breakdown", "subspace"]
        original_fact = Fact(type="trend")
        candidates = [original_fact]

        # step 1: search measure
        mentioned_measure_fields = self.mentioned_fields_n
        if len(mentioned_measure_fields) > 0:
            candidates = self.__search_measure(question, candidates, mentioned_measure_fields, canadiate_size)
        else:
            return []

        # step 2: search breakdown
        mentioned_breakdown_fields = self.mentioned_fields_t + self.other_fields_t
        mentioned_breakdown_fields = [dict(t) for t in set([tuple(d.items()) for d in mentioned_breakdown_fields])] # remove duplicate
        if len(mentioned_breakdown_fields) > 0:
            candidates = self.__search_breakdown(question, candidates, mentioned_breakdown_fields, canadiate_size)
        else:
            return []
        
        # step 3: search subspace
        potential_subspace_fields = self.mentioned_fields_c + self.mentioned_fields_g
        if len(potential_subspace_fields) > 0:
            candidates = self.__search_subspace(question, candidates, potential_subspace_fields, canadiate_size)
        
        return candidates

    def __search_value(self, question, canadiate_size):
        # 'value': ["measure", "subspace"]
        original_fact = Fact(type="value")
        candidates = [original_fact]

        # step 1: search measure
        mentioned_measure_fields = self.mentioned_fields_n
        if len(mentioned_measure_fields) > 0:
            candidates = self.__search_measure(question, candidates, mentioned_measure_fields, canadiate_size)
        else:
            return []
        
        # step 2: search subspace
        potential_subspace_fields = self.mentioned_fields_c + self.mentioned_fields_t + self.mentioned_fields_g
        if len(potential_subspace_fields) > 0:
            candidates = self.__search_subspace(question, candidates, potential_subspace_fields, canadiate_size)
        
        return candidates

    def __search_measure(self, question, candidates, mentioned_measure_fields, canadiate_size):
        candidates_to_add = []
        for candidate in candidates:
            for measure in mentioned_measure_fields:
                measure['aggregate'] = self.schema.field2aggregate[measure['field']]
                new_candidate = deepcopy(candidate)
                new_candidate.measure.append(measure)
                new_candidate.parameter = fact_scoring(new_candidate.__dict__, self.df, self.schema, method="sig")
                candidates_to_add.append(new_candidate)
        candidates += candidates_to_add
        if len(candidates) >= canadiate_size:
            candidates = random.sample(candidates, canadiate_size)
        
        # multi_process
        # cosine_similaritylist = self.__similarity_ByParallel(question, candidates)
        # zipped = zip(candidates, cosine_similaritylist)
        # sort_zipped = sorted(zipped, key =lambda x:x[1], reverse=True)
        # candidates , cosine_similaritylist = [list(x) for x in zip(*sort_zipped)]
        # single_process
        candidates.sort(reverse=True, key=lambda fact:self.__similarity_word2vec(question, fact))
        candidates = candidates[:self.search_size]
        return candidates

    def __search_measure_2(self, question, candidates, mentioned_measure_fields, canadiate_size):
        candidates_to_add = []
        for candidate in candidates:
            for measures in itertools.combinations(mentioned_measure_fields, 2):
                measures[0]['aggregate'] = self.schema.field2aggregate[measures[0]['field']]
                measures[1]['aggregate'] = self.schema.field2aggregate[measures[1]['field']]
                new_candidate = deepcopy(candidate)
                new_candidate.measure.append(measures[0])
                new_candidate.measure.append(measures[1])
                new_candidate.parameter = fact_scoring(new_candidate.__dict__, self.df, self.schema, method="sig")
                candidates_to_add.append(new_candidate)
        candidates += candidates_to_add
        if len(candidates) >= canadiate_size:
            candidates = random.sample(candidates, canadiate_size)
        # multi_process
        # cosine_similaritylist = self.__similarity_ByParallel(question, candidates)
        # zipped = zip(candidates, cosine_similaritylist)
        # sort_zipped = sorted(zipped, key =lambda x:x[1], reverse=True)
        # candidates , cosine_similaritylist = [list(x) for x in zip(*sort_zipped)]
        # single process        
        candidates.sort(reverse=True, key=lambda fact:self.__similarity_word2vec(question, fact))
        candidates = candidates[:self.search_size]
        return candidates

    def __search_breakdown(self, question, candidates, mentioned_breakdown_fields, canadiate_size):
        candidates_to_add = []
        for candidate in candidates:
            for breakdown in mentioned_breakdown_fields:
                new_candidate = deepcopy(candidate)
                new_candidate.breakdown.append(breakdown)
                new_candidate.parameter = fact_scoring(new_candidate.__dict__, self.df, self.schema, method="sig")
                candidates_to_add.append(new_candidate)
        candidates += candidates_to_add
        if len(candidates) >= canadiate_size:
            candidates = random.sample(candidates, canadiate_size)
        # multi_process
        # cosine_similaritylist = self.__similarity_ByParallel(question, candidates)
        # zipped = zip(candidates, cosine_similaritylist)
        # sort_zipped = sorted(zipped, key =lambda x:x[1], reverse=True)
        # candidates , cosine_similaritylist = [list(x) for x in zip(*sort_zipped)]
        # single process        
        candidates.sort(reverse=True, key=lambda fact:self.__similarity_word2vec(question, fact))
        candidates = candidates[:self.search_size]
        return candidates

    def __search_subspace(self, question, candidates, potential_subspace_fields, canadiate_size):
        candidates_to_add = []
        for candidate in candidates:
            for subspace_field in potential_subspace_fields:
                if subspace_field in candidate.breakdown:
                    continue
                else:
                    values = self.schema.field2values[subspace_field['field']]
                    for value in values:
                        subspace = deepcopy(subspace_field)
                        subspace['value'] = value
                        new_candidate = deepcopy(candidate)
                        new_candidate.subspace.append(subspace)
                        new_candidate.parameter = fact_scoring(new_candidate.__dict__, self.df, self.schema, method="sig")
                        candidates_to_add.append(new_candidate)
        candidates += candidates_to_add
        if len(candidates) >= canadiate_size:
            candidates = random.sample(candidates, canadiate_size)
        # multi_process
        # cosine_similaritylist = self.__similarity_ByParallel(question, candidates)
        # zipped = zip(candidates, cosine_similaritylist)
        # sort_zipped = sorted(zipped, key =lambda x:x[1], reverse=True)
        # candidates , cosine_similaritylist = [list(x) for x in zip(*sort_zipped)]
        # single process        
        candidates.sort(reverse=True, key=lambda fact:self.__similarity_word2vec(question, fact))
        candidates = candidates[:self.search_size]
        return candidates

    def __search_focus(self, question, candidates, canadiate_size):
        candidates_to_add = []
        for candidate in candidates:
            if len(candidate.breakdown) > 0:
                focus_field = candidate.breakdown[0]
                values = self.schema.field2values[focus_field['field']]
                for value in values:
                    focus = deepcopy(focus_field)
                    focus['value'] = value
                    new_candidate = deepcopy(candidate)
                    new_candidate.focus.append(focus)
                    new_candidate.parameter = fact_scoring(new_candidate.__dict__, self.df, self.schema, method="sig")
                    candidates_to_add.append(new_candidate)
                    
        candidates = candidates_to_add
        if len(candidates) >= canadiate_size:
            candidates = random.sample(candidates, canadiate_size)
        # multi_process
        # cosine_similaritylist = self.__similarity_ByParallel(question, candidates)
        # zipped = zip(candidates, cosine_similaritylist)
        # sort_zipped = sorted(zipped, key =lambda x:x[1], reverse=True)
        # candidates , cosine_similaritylist = [list(x) for x in zip(*sort_zipped)]
        # single process        
        candidates.sort(reverse=True, key=lambda fact:self.__similarity_word2vec(question, fact))
        candidates = candidates[:self.search_size]
        return candidates

    def __search_focus_outlier_extreme(self, question, df, candidates, canadiate_size):
        candidates_to_add = []
        for candidate in candidates:
            fact = candidate.__dict__
            focus = fact_focus(fact, df)
            new_candidate = deepcopy(candidate)
            new_candidate.focus = focus
            new_candidate.parameter = fact_scoring(new_candidate.__dict__, self.df, self.schema, method="sig")
            candidates_to_add.append(new_candidate)
                    
        candidates = candidates_to_add
        if len(candidates) >= canadiate_size:
            candidates = random.sample(candidates, canadiate_size)
        # multi_process
        # cosine_similaritylist = self.__similarity_ByParallel(question, candidates)
        # zipped = zip(candidates, cosine_similaritylist)
        # sort_zipped = sorted(zipped, key =lambda x:x[1], reverse=True)
        # candidates , cosine_similaritylist = [list(x) for x in zip(*sort_zipped)]
        # single process        
        candidates.sort(reverse=True, key=lambda fact:self.__similarity_word2vec(question, fact))
        candidates = candidates[:self.search_size]
        return candidates

    def __search_focus_difference(self, question, candidates, canadiate_size):
        candidates_to_add = []
        for candidate in candidates:
            if len(candidate.breakdown) > 0:
                focus_field = candidate.breakdown[0]
                values = self.schema.field2values[focus_field['field']]
                for value in itertools.combinations(values, 2):
                    focus1 = deepcopy(focus_field)
                    focus2 = deepcopy(focus_field)
                    focus1['value'] = value[0]
                    focus2['value'] = value[1]
                    new_candidate = deepcopy(candidate)
                    new_candidate.focus.append(focus1)
                    new_candidate.focus.append(focus2)
                    new_candidate.parameter = fact_scoring(new_candidate.__dict__, self.df, self.schema, method="sig")
                    candidates_to_add.append(new_candidate)
                    
                    
        candidates = candidates_to_add
        if len(candidates) >= canadiate_size:
            candidates = random.sample(candidates, canadiate_size)
        # multi_process
        # cosine_similaritylist = self.__similarity_ByParallel(question, candidates)
        # zipped = zip(candidates, cosine_similaritylist)
        # sort_zipped = sorted(zipped, key =lambda x:x[1], reverse=True)
        # candidates , cosine_similaritylist = [list(x) for x in zip(*sort_zipped)]
        # single process        
        candidates.sort(reverse=True, key=lambda fact:self.__similarity_word2vec(question, fact))
        candidates = candidates[:self.search_size]
        return candidates

    def __cos_sim(self, vector_a, vector_b):
        norma = np.linalg.norm(vector_a)
        normb = np.linalg.norm(vector_b)
        dot_products = np.dot(norma, normb)
        similarities = dot_products / (norma * normb)
        return similarities