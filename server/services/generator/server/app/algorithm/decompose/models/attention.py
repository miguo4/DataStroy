######################################################################
# The decoder RNN generates the response sentence in a token-by-token
# fashion. It uses the encoder’s context vectors, and internal hidden
# states to generate the next word in the sequence. It continues
# generating words until it outputs an *EOS_token*, representing the end
# of the sentence. 
# A common problem with a vanilla seq2seq decoder is that
# if we rely soley on the context vector to encode the entire input
# sequence’s meaning, it is likely that we will have information loss.
# This is especially the case when dealing with long input sequences,
# greatly limiting the capability of our decoder.
#
# To combat this, `Bahdanau et al. <https://arxiv.org/abs/1409.0473>`__
# created an “attention mechanism” that allows the decoder to pay
# attention to certain parts of the input sequence, rather than using the
# entire fixed context at every step.
#
# At a high level, attention is calculated using the decoder’s current
# hidden state and the encoder’s outputs. The output attention weights
# have the same shape as the input sequence, allowing us to multiply them
# by the encoder outputs, giving us a weighted sum which indicates the
# parts of encoder output to pay attention to. `Sean
# Robertson’s <https://github.com/spro>`__ figure describes this very
# well:
#
#
# Luong et al. <https://arxiv.org/abs/1508.04025>`__ improved upon
# Bahdanau et al.’s groundwork by creating “Global attention”. The key
# difference is that with “Global attention”, we consider all of the
# encoder’s hidden states, as opposed to Bahdanau et al.’s “Local
# attention”, which only considers the encoder’s hidden state from the
# current time step. Another difference is that with “Global attention”,
# we calculate attention weights, or energies, using the hidden state of
# the decoder from the current time step only. Bahdanau et al.’s attention
# calculation requires knowledge of the decoder’s state from the previous
# time step. Also, Luong et al. provides various methods to calculate the
# attention energies between the encoder output and decoder output which
# are called “score functions”:
#
#
#
# Note that we will implement the “Attention Layer” as a
# separate ``nn.Module`` called ``Attn``. The output of this module is a
# softmax normalized weights tensor of shape *(batch_size, 1,
# max_length)*.
#

import torch
import torch.nn as nn
import torch.nn.functional as F

# Luong attention layer
class Attn(nn.Module):
    def __init__(self, method, hidden_size):
        super(Attn, self).__init__()
        self.method = method
        if self.method not in ['dot', 'general', 'concat']:
            raise ValueError(self.method, "is not an appropriate attention method.")
        self.hidden_size = hidden_size
        if self.method == 'general':
            self.attn = nn.Linear(self.hidden_size, hidden_size)
        elif self.method == 'concat':
            self.attn = nn.Linear(self.hidden_size * 2, hidden_size)
            self.v = nn.Parameter(torch.FloatTensor(hidden_size))

    def dot_score(self, hidden, encoder_output):
        return torch.sum(hidden * encoder_output, dim=2)

    def general_score(self, hidden, encoder_output):
        energy = self.attn(encoder_output)
        return torch.sum(hidden * energy, dim=2)

    def concat_score(self, hidden, encoder_output):
        energy = self.attn(torch.cat((hidden.expand(encoder_output.size(0), -1, -1), encoder_output), 2)).tanh()
        return torch.sum(self.v * energy, dim=2)

    def forward(self, hidden, encoder_outputs):
        # Calculate the attention weights (energies) based on the given method
        if self.method == 'general':
            attn_energies = self.general_score(hidden, encoder_outputs)
        elif self.method == 'concat':
            attn_energies = self.concat_score(hidden, encoder_outputs)
        elif self.method == 'dot':
            attn_energies = self.dot_score(hidden, encoder_outputs)

        # Transpose max_length and batch_size dimensions
        attn_energies = attn_energies.t()

        # Return the softmax normalized probability scores (with added dimension)
        return F.softmax(attn_energies, dim=1).unsqueeze(1)