import torch
import torch.nn as nn
import torch.nn.functional as F

class Decomposer(nn.Module):
    def __init__(self, input_size, decompose_size, dropout=0.1):
        super(Decomposer, self).__init__()

        self.input_size = input_size
        self.decompose_size = decompose_size
        self.dropout = dropout

        self.fc1 = nn.Sequential(
            nn.Linear(input_size, decompose_size),
            nn.Dropout(dropout),
            nn.Hardtanh(-10, 10),
            nn.Linear(decompose_size, decompose_size),
            nn.Dropout(dropout),
            nn.Hardtanh(-10, 10),
        )

        self.fc2 = nn.Sequential(
            nn.Linear(input_size, decompose_size),
            nn.Dropout(dropout),
            nn.Hardtanh(-10, 10),
            nn.Linear(decompose_size, decompose_size),
            nn.Dropout(dropout),
            nn.Hardtanh(-10, 10),
        )

        # self.decompose = nn.Sequential(
        #     nn.Linear(input_size, 2*decompose_size),
        #     nn.Dropout(dropout),
        #     # nn.Linear(2*decompose_size, 2*decompose_size), # in case for 2 layers
        #     # nn.Dropout(dropout),
        #     nn.Hardtanh(-10, 10),
        # )

    def forward(self, inputs):
        sub_hidden_1 = self.fc1(inputs)
        sub_hidden_2 = self.fc2(inputs)

        # sub_hidden = self.decompose(inputs)
        # sub_hidden_1, sub_hidden_2 = torch.split(sub_hidden, [self.decompose_size, self.decompose_size], dim=2)

        return sub_hidden_1, sub_hidden_2