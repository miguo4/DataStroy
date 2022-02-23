from flask import Flask
from flask_cors import CORS
from .config import Config
from .api import api_blueprint
from gensim.models import KeyedVectors
from sentence_transformers import SentenceTransformer
from transformers import BertForSequenceClassification, BertTokenizer
import torch
from attrdict import AttrDict 
from .algorithm.decompose.models import EncoderRNN, Decomposer, DecoderRNN, GreedySearchDecoder

import torch.nn as nn


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    app.word2vec = KeyedVectors.load_word2vec_format(Config.Word2Vec, binary=True)
    app.sentence_bert = SentenceTransformer(Config.SentenceBERT, device = app.device)
    app.tokenizer = BertTokenizer.from_pretrained(Config.BERT, local_files_only=True, do_lower_case=True)
    app.FactClassifier = BertForSequenceClassification.from_pretrained(Config.BERT,      
                                                        local_files_only=True,
                                                        num_labels=10,
                                                        output_attentions=False,
                                                        output_hidden_states=False)
    app.FactClassifier.to(app.device)
    app.FactClassifier.load_state_dict(torch.load(Config.FactClassificationModel, map_location=app.device))
    app.candidate_size = Config.candidate_size
    app.search_size = Config.search_size
    app.QuestionClassifier = BertForSequenceClassification.from_pretrained(Config.BERT,      
                                                            local_files_only=True,
                                                            num_labels=2,
                                                            output_attentions=False,
                                                            output_hidden_states=False)
    app.QuestionClassifier.to(app.device)
    app.QuestionClassifier.load_state_dict(torch.load(Config.QuestionClassificationModel, map_location=app.device))
        
    checkpoint = torch.load(Config.CheckPoints, map_location=app.device)

    app.voc = AttrDict(checkpoint['voc_dict'])
    app.max_length=checkpoint['maxlen']

    app.embedding = nn.Embedding(app.voc.num_words + Config.max_length, Config.hidden_size)

    app.embedding.load_state_dict(checkpoint['embed'])

    app.encoder = EncoderRNN(Config.hidden_size, app.embedding, Config.encoder_n_layers, Config.dropout)
    app.decomposer = Decomposer(Config.hidden_size+2, Config.sub_hidden_size, Config.dropout)
    app.decoder = DecoderRNN(Config.attn_model, Config.copy_model, app.embedding, Config.sub_hidden_size, app.voc.num_words, Config.max_length, Config.max_length, Config.decoder_n_layers, Config.dropout)

    app.decoder.load_state_dict(checkpoint['de'])
    app.encoder.load_state_dict(checkpoint['en'])
    app.decomposer.load_state_dict(checkpoint['decp'])

    print(app)
    CORS(app)
    app.config.from_object(Config)
    app.register_blueprint(api_blueprint, url_prefix = '')
    return app