import torch
from flask import current_app

class FactClassifier():
    def __init__(self):
        self.model = current_app.FactClassifier

    def classify(self, sentence):
        
        inputs = current_app.tokenizer(sentence, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits[0]
        pred = torch.argmax(logits)

        # type           label                              
        # categorization 0     
        # extreme        1     
        # trend          2     
        # value          3     
        # association    4     
        # rank           5     
        # distribution   6     
        # outlier        7     
        # difference     8     
        # proportion     9     

        facts = ['proportion', 'association', 'extreme', 'difference', 'rank', 'categorization', 'outlier', 'distribution', 'value', 'trend']

        return facts[int(pred)]