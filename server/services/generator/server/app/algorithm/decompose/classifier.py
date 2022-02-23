import sys
import torch
from tqdm import tqdm 
import pandas as pd
import numpy as np
from flask import current_app

class Classifier:
    def __init__(self):
        self.model = current_app.QuestionClassifier
        pass

    def classify(self, question):

        # type           label                              
        # BottomUp           0
        # TopDown            1


        if len(sys.argv) > 1:
            question = sys.argv[1]

        inputs = current_app.tokenizer(question, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs[0]
        pred = torch.argmax(logits)
        types = ['BottomUp', 'TopDown']

        return types[int(pred)]
