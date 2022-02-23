######################################################################
# Encoder
# ~~~~~~~
# Bidirectional RNN:
#
# Using a bidirectional GRU will give us the advantage of encoding both
# past and future context.
#
# Note that an ``embedding`` layer is used to encode our word indices in
# an arbitrarily sized feature space. For our models, this layer will map
# each word to a feature space of size *hidden_size*. When trained, these
# values should encode semantic similarity between similar meaning words.
#
# if passing a padded batch of sequences to an RNN module, we
# must pack and unpack padding around the RNN pass using
# ``nn.utils.rnn.pack_padded_sequence`` and
# ``nn.utils.rnn.pad_packed_sequence`` respectively.
#
# **Computation Graph:**
#
#    1) Convert word indexes to embeddings.
#    2) Pack padded batch of sequences for RNN module.
#    3) Forward pass through GRU.
#    4) Unpack padding.
#    5) Sum bidirectional GRU outputs.
#    6) Return output and final hidden state.
#
# **Inputs:**
#
# -  ``input_seq``: batch of input sentences; shape=\ *(max_length,
#    batch_size)*
# -  ``input_lengths``: list of sentence lengths corresponding to each
#    sentence in the batch; shape=\ *(batch_size)*
# -  ``hidden``: hidden state; shape=\ *(n_layers x num_directions,
#    batch_size, hidden_size)*
#
# **Outputs:**
#
# -  ``outputs``: output features from the last hidden layer of the GRU
#    (sum of bidirectional outputs); shape=\ *(max_length, batch_size,
#    hidden_size)*
# -  ``hidden``: updated hidden state from GRU; shape=\ *(n_layers x
#    num_directions, batch_size, hidden_size)*
#
#

import torch
import torch.nn as nn
import torch.nn.functional as F

class EncoderRNN(nn.Module):
    def __init__(self, hidden_size, embedding, n_layers=1, dropout=0):
        super(EncoderRNN, self).__init__()
        self.n_layers = n_layers
        self.hidden_size = hidden_size
        self.embedding = embedding

        # Initialize GRU; the input_size and hidden_size params are both set to 'hidden_size'
        #   because our input size is a word embedding with number of features == hidden_size
        self.gru = nn.GRU(hidden_size, hidden_size, n_layers,
                          dropout=(0 if n_layers == 1 else dropout), bidirectional=True)

    def forward(self, input_seq, input_lengths, questiontype, device, hidden=None):
        # Convert word indexes to embeddings
        embedded = self.embedding(input_seq)
        # Pack padded batch of sequences for RNN module
        packed = nn.utils.rnn.pack_padded_sequence(embedded, input_lengths)
        # Forward pass through GRU
        outputs, hidden = self.gru(packed, hidden)
        # Unpack padding
        outputs, _ = nn.utils.rnn.pad_packed_sequence(outputs)
        # Sum bidirectional GRU outputs
        outputs = outputs[:, :, :self.hidden_size] + outputs[:, : ,self.hidden_size:]
        # Return output and final hidden state
        
        #************feb22th, add complex question type into hidden tensor, 
        # for topdown question, we add [1,0] at the end of origin tensor, 
        # for bottomup question, we add [0,1] at the end of origin tensor,
        hidden_with_type=torch.zeros([hidden.shape[0],hidden.shape[1],hidden.shape[2]+2],device=device)
        if isinstance(questiontype, str):
            if questiontype == 'topdown':
                for i in range(hidden.shape[0]):
                    hidden_with_type[i][0] = torch.cat((hidden[i][0],torch.tensor([1,0],device=device)),0)                
            else:
                for i in range(hidden.shape[0]):
                    hidden_with_type[i][0] = torch.cat((hidden[i][0],torch.tensor([0,1],device=device)),0)                
        else:
            for i in range(len(questiontype)):
                if questiontype[i] == 'topdown':
                    for j in range(hidden.shape[0]):
                        hidden_with_type[j][i] = torch.cat((hidden[j][i],torch.tensor([1,0],device=device)),0)                
                    
                else:
                    for j in range(hidden.shape[0]):
                        hidden_with_type[j][i] = torch.cat((hidden[j][i],torch.tensor([0,1],device=device)),0)                
        
        # print(hidden_with_type.shape)

        return outputs, hidden, hidden_with_type