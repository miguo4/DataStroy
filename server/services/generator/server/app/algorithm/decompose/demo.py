import torch
import torch.nn as nn
from evaluate import evaluateInput
from models import EncoderRNN, Decomposer, LuongAttnDecoderRNN, GreedySearchDecoder
from config import Config
from attrdict import AttrDict





model_name = Config.model_name
attn_model = Config.attn_model
hidden_size = Config.hidden_size
sub_hidden_size = Config.sub_hidden_size
encoder_n_layers = Config.encoder_n_layers
decoder_n_layers = Config.decoder_n_layers
dropout = Config.dropout
batch_size = Config.batch_size


PATH = 'data/trainedmodels/trained_decompose.tar'

if torch.cuda.is_available():
    map_location=lambda storage, loc: storage.cuda()
else:
    map_location='cpu'
    
checkpoint = torch.load(PATH, map_location=map_location)


voc = AttrDict(checkpoint['voc_dict'])


MAX_LENGTH=checkpoint['maxlen']

embedding = nn.Embedding(voc.num_words, hidden_size)
embedding.load_state_dict(checkpoint['embed'])

encoder = EncoderRNN(hidden_size, embedding, encoder_n_layers, dropout)
decomposer = Decomposer(hidden_size+2, sub_hidden_size, dropout)
decoder = LuongAttnDecoderRNN(attn_model, embedding, sub_hidden_size, voc.num_words, decoder_n_layers, dropout)

decoder.load_state_dict(checkpoint['de'])
encoder.load_state_dict(checkpoint['en'])
decomposer.load_state_dict(checkpoint['decp'])


encoder.eval()
decomposer.eval()
decoder.eval()

device = torch.device("cpu")

# # Initialize search module
searcher = GreedySearchDecoder(encoder, decomposer, decoder, device)

# # Begin to decompose
evaluateInput(searcher, voc, MAX_LENGTH, device)