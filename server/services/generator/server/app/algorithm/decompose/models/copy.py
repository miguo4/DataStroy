######################################################################
# Gu, Jiatao, et al. "Incorporating copying mechanism in sequence-to-sequence learning." 
# <https://arxiv.org/pdf/1603.06393.pdf>`

import torch
import torch.nn as nn
import torch.nn.functional as F

# Copy net layer
class Copy(nn.Module):
    def __init__(self, hidden_size, source_size):
        super(Copy, self).__init__()
        self.hidden_size = hidden_size
        self.source_size = source_size
        self.copy = nn.Sequential(
            nn.Linear(self.hidden_size, self.hidden_size),
            nn.Hardtanh(-10, 10),
        )
        self.w_a = nn.Linear(hidden_size, 1)
        self.u_a = nn.Linear(hidden_size, 1)
        self.v_a = nn.Linear(hidden_size, 1)

    def forward(self, input_embedded_word, hidden, context, encoder_outputs):

        # Self-Attention Guided Copy Mechanism for Abstractive Summarization
        # Eq.(8)
        input_embedded_word = input_embedded_word.squeeze(0)
        sig = nn.Sigmoid()
        p_copy = sig(self.w_a(context) + self.u_a(hidden) + self.u_a(input_embedded_word))

        # Incorporating Copying Mechanism in Sequence-to-Sequence Learning Eq(8)
        hT = encoder_outputs.transpose(0, 1)
        tanh_hTW = self.copy(hT)
        hidden = hidden.unsqueeze(2)
        output = tanh_hTW.bmm(hidden)
        output = output.squeeze(2)



        return output, p_copy