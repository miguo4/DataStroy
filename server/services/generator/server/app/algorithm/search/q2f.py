import os
import nltk
from .search import FactSearch
from .fact import Fact
from .classifier import FactClassifier
from gensim.parsing.preprocessing import remove_stopwords
from gensim.models import KeyedVectors
from flask import current_app

class Question2Fact():
    def __init__(self, schema,df):
        self.schema = schema
        self.df = df
        self.fact_cls = FactClassifier()
        self.search_size = current_app.search_size

    def generate(self, question) :
        """Generate the most related fact from the question. 

        Args:
            question (String): an input querstion

        Returns:
            Fact: the most related fact
        """  
        question = question.lower() # set to lowercase
        fact_type = self.__type(question)
        # print("Type: %s"%fact_type)
        entities = self.__ner(question)
        # print("Entities: %s"%(entities))
        fields = self.__entities2fields(entities, threshold=0)
        # print("Selected fields: %s"%(fields))
        facts = self.__search(question, fact_type, fields)

        return facts

    def __type(self, question):
        """Classify the fact type of the question

        Args:
            question (String): an input question

        Returns:
            String: fact type (10 types)
        """   
        fact_type = self.fact_cls.classify(question)    
        return fact_type

    def __ner(self, sentence):
        """Detect the entities in the sentence

        Args:
            sentence (String): an input sentence

        Returns:
            [String]: entities
        """    

        # Remove stop words
        sentence = remove_stopwords(sentence)

        # Create NLTK data directory
        NLTK_DATA_DIR = './nltk_data'
        # if not os.path.exists(NLTK_DATA_DIR):
        #         os.makedirs(NLTK_DATA_DIR)
        nltk.data.path.append(NLTK_DATA_DIR)
        # nltk.download('averaged_perceptron_tagger', download_dir=NLTK_DATA_DIR)

        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)

        # The list of POS tags is as follows
        # NN noun, singular ‘desk’
        # NNS noun plural ‘desks’
        # NNP proper noun, singular ‘Harrison’
        # NNPS proper noun, plural ‘Americans’

        entities = []
        for tagged_token in tagged:
            if tagged_token[1] in ['NN', 'NNS', 'NNP', 'NNPS'] or tagged_token[0] in self.schema.fields:
                entities.append(tagged_token[0])
                
        return entities

    def __entities2fields(self, entities, threshold = 0.2):
        """Find fields that related to the entities

        Args:
            entities ([String]): entities

        Returns:
            [String]: fields
        """        
        selected_fields = []
        for entity in entities:
            if entity == "<" or entity == ">":
                continue
            max_similarity = 0
            selected_field = ""
            for field in self.schema.fields:
                similarity = current_app.word2vec.similarity(entity, field)
                # print("the similarity between %s and %s is %s"%(entity, field, similarity))
                if similarity > max_similarity:
                    selected_field = field
                    max_similarity = similarity
            if max_similarity > threshold and selected_field not in selected_fields:
                selected_fields.append(selected_field)
        
        return selected_fields

    def __search(self, question, fact_type, fields):
        """Search the fact based on question and given fields

        Args:
            question (String): input question
            fact_type (String): fact type
            fields ([String]): fields
            search_size: search size
        Returns:
            [Fact]: related facts
        """    
        searcher = FactSearch(schema = self.schema, df = self.df, search_size = self.search_size, mentioned_fields = fields)
        facts = searcher.search(question, fact_type, current_app.candidate_size)
        return facts
    