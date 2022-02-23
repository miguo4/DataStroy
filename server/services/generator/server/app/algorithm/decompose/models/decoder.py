import torch
import torch.nn as nn
import torch.nn.functional as F
from .attention import Attn
from .copy import Copy

class DecoderRNN(nn.Module):
    def __init__(self, attn_model, copy_model, embedding, hidden_size, vocab_size, source_size, sentence_size, n_layers=1, dropout=0.1):
        super(DecoderRNN, self).__init__()

        # Keep for reference
        self.attn_model = attn_model
        self.copy_model = copy_model
        self.hidden_size = hidden_size
        self.vocab_size = vocab_size
        self.source_size = source_size
        self.output_size = vocab_size + source_size
        self.sentence_size = sentence_size
        self.n_layers = n_layers
        self.dropout = dropout

        # Define layers
        self.embedding = embedding
        self.embedding_dropout = nn.Dropout(dropout)
        self.gru = nn.GRU(hidden_size, hidden_size, n_layers, dropout=(0 if n_layers == 1 else dropout))
        self.concat = nn.Linear(hidden_size * 2, hidden_size)
        # self.out = nn.Linear(hidden_size, output_size)
        self.out = nn.Linear(hidden_size, vocab_size)

        self.attn = Attn(attn_model, hidden_size)
        self.copy = Copy(hidden_size, source_size)

    def forward(self, input_step, last_hidden, encoder_outputs, device):
        # Note: we run this one step (word) at a time
        # Get embedding of current input word
        embedded_word = self.embedding(input_step)
        embedded_word = self.embedding_dropout(embedded_word)
        # Forward through unidirectional GRU
        rnn_output, hidden = self.gru(embedded_word, last_hidden)
        # Calculate attention weights from the current GRU output
        attn_weights = self.attn(rnn_output, encoder_outputs)
        # Multiply attention weights to encoder outputs to get new "weighted sum" context vector
        context = attn_weights.bmm(encoder_outputs.transpose(0, 1))
        # Concatenate weighted context vector and GRU output using Luong eq. 5
        rnn_output = rnn_output.squeeze(0)
        context = context.squeeze(1)
        concat_input = torch.cat((rnn_output, context), 1)
        concat_output = torch.tanh(self.concat(concat_input))
        # Predict next word using Luong eq. 6
        attn_output = self.out(concat_output)
        # attn_output = F.softmax(attn_output, dim=1)

        # Predict next word using copy Mechanism
        copy_output, p_copy = self.copy(embedded_word, hidden[self.n_layers-1], context, encoder_outputs)
        # copy_output = F.softmax(copy_output, dim=1)
        
        # Return output and final hidden state
        output = torch.cat((attn_output, copy_output), dim=1)
        output = F.softmax(output, dim=1)

        # Generate mode and Copy mode
        p_gen = torch.ones(p_copy.shape, device=device) - p_copy
        p_gen = p_gen.repeat(1,self.vocab_size)
        p_copy = p_copy.repeat(1,copy_output.shape[1])
        p = torch.cat((p_gen, p_copy), dim=1)
        output = output.mul(p)

        return output, hidden