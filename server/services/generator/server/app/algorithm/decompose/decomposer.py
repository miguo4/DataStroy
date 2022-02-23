import torch
from .evaluate import evaluateInput
from .models import GreedySearchDecoder
from attrdict import AttrDict 
from .classifier import Classifier
import os 
from flask import current_app

class DecomposerModel:
    def __init__(self, file_schema):
        self.file_schema = file_schema
        self.voc = current_app.voc
        self.max_length = current_app.max_length

        self.embedding = current_app.embedding

        self.encoder = current_app.encoder
        self.decomposer = current_app.decomposer
        self.decoder = current_app.decoder



        self.encoder.eval()
        self.decomposer.eval()
        self.decoder.eval()

        self.device = current_app.device

        self.classifier = Classifier()


    def __addschema(self,question):
        cg_fields = list(filter(lambda x:x['type'] != 'numerical' and x['type'] != 'temporal' and len(x['values']) > 1, self.file_schema["fields"])) 
        t_fields = list(filter(lambda x:x['type'] == 'temporal' and len(x['values']) > 1, self.file_schema["fields"])) 
        n_fields = list(filter(lambda x:x['type'] == 'numerical', self.file_schema["fields"])) 

        cg_lists = list(map(lambda x: x['field'].lower() , cg_fields))
        t_lists = list(map(lambda x: x['field'].lower() , t_fields))
        n_lists = list(map(lambda x: x['field'].lower() , n_fields))

        schema_string = " <SEPNUM> " + ' '.join(map(str, n_lists))+ " <SEPTEP> " + ' '.join(map(str, t_lists))+ " <SEPCAT> " + ' '.join(map(str, cg_lists))

        question = question.rstrip() + schema_string
        
        print(question)
        
        return question


    def decompose(self, question):

        question = self.__addschema(question)
        
        questiontype = self.classifier.classify(question)

        searcher = GreedySearchDecoder(self.encoder, self.decomposer, self.decoder, self.device)
        
        decomposed_question1, decomposed_question2 = evaluateInput(question, questiontype, searcher, self.voc, self.max_length, self.device)

        # searcher, voc, max_length, device

        return decomposed_question1, decomposed_question2
