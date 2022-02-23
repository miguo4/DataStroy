import torch
import torch.nn as nn

# Default word tokens
PAD_token = 0  # Used for padding short sentences
SOS_token = 1  # Start-of-sentence token
EOS_token = 2  # End-of-sentence token

class GreedySearchDecoder(nn.Module):
    def __init__(self, encoder, decomposer, decoder, device):
        super(GreedySearchDecoder, self).__init__()
        self.encoder = encoder
        self.decomposer = decomposer
        self.decoder = decoder
        self.device = device

    def forward(self, input_seq, input_length, max_length, questiontype):
        # Forward input through encoder model
        encoder_outputs, encoder_hidden, encoder_hidden_with_type = self.encoder(input_seq, input_length, questiontype, self.device)
        # decompose encoder's final hidden state
        sub_hidden_1, sub_hidden_2 = self.decomposer(encoder_hidden_with_type[:self.encoder.n_layers])
        # Initialize decoder input with SOS_token
        decoder_input_1 = torch.ones(1, 1, device=self.device, dtype=torch.long) * SOS_token
        decoder_input_2 = torch.ones(1, 1, device=self.device, dtype=torch.long) * SOS_token
        # Initialize tensors to append decoded words to
        all_tokens_1 = torch.zeros([0], device=self.device, dtype=torch.long)
        all_scores_1 = torch.zeros([0], device=self.device)
        all_tokens_2 = torch.zeros([0], device=self.device, dtype=torch.long)
        all_scores_2 = torch.zeros([0], device=self.device)
        # Iteratively decode one word token at a time
        for _ in range(max_length):
            # Forward pass through decoder
            decoder_output, sub_hidden_1 = self.decoder(
                decoder_input_1, sub_hidden_1, encoder_outputs, self.device
            )
            # Obtain most likely word token and its softmax score
            decoder_scores, decoder_input_1 = torch.max(decoder_output, dim=1)
            # Record token and score
            all_tokens_1 = torch.cat((all_tokens_1, decoder_input_1), dim=0)
            all_scores_1 = torch.cat((all_scores_1, decoder_scores), dim=0)
            # Prepare current token to be next decoder input (add a dimension)
            decoder_input_1 = torch.unsqueeze(decoder_input_1, 0)
        for _ in range(max_length):
            # Forward pass through decoder
            decoder_output, sub_hidden_2 = self.decoder(
                decoder_input_2, sub_hidden_2, encoder_outputs, self.device
            )
            # Obtain most likely word token and its softmax score
            decoder_scores, decoder_input_2 = torch.max(decoder_output, dim=1)
            # Record token and score
            all_tokens_2 = torch.cat((all_tokens_2, decoder_input_2), dim=0)
            all_scores_2 = torch.cat((all_scores_2, decoder_scores), dim=0)
            # Prepare current token to be next decoder input (add a dimension)
            decoder_input_2 = torch.unsqueeze(decoder_input_2, 0)
        # Return collections of word tokens and scores
        return all_tokens_1, all_scores_1, all_tokens_2, all_scores_2