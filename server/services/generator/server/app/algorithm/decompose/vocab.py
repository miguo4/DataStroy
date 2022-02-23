# -*- coding: utf-8 -*-

# Default word tokens
PAD_token = 0  # Used for padding short sentences
SOS_token = 1  # Start-of-sentence token
EOS_token = 2  # End-of-sentence token
UNK_token = 3  # Unknown token
SEPNUM_token = 4  # Numerical table header
SEPCAT_token = 5  # Categorical table header
SEPTEP_token = 6  # Temporal table header

class Voc:
    def __init__(self, name):
        self.name = name
        self.trimmed = False
        self.word2index = {"<PAD>": PAD_token, "<SOS>": SOS_token, "<EOS>": EOS_token, "<UNK>": UNK_token, "<SEPNUM>": SEPNUM_token, "<SEPTEP>":SEPTEP_token, "<SEPCAT>":SEPCAT_token }
        self.word2count = {"<PAD>": 0, "<SOS>": 0, "<EOS>": 0, "<UNK>": 0, "<SEPNUM>": 0, "<SEPTEP>":0, "<SEPCAT>":0 }
        self.word_is_in_input = {"<PAD>": True, "<SOS>": True, "<EOS>": True, "<UNK>": True, "<SEPNUM>": True, "<SEPTEP>":True, "<SEPCAT>":True }        
        self.index2word = {PAD_token: "<PAD>", SOS_token: "<SOS>", EOS_token: "<EOS>", UNK_token: "<UNK>", SEPNUM_token: "<SEPNUM>", SEPTEP_token: "<SEPTEP>", SEPCAT_token: "<SEPCAT>" }
        self.num_words = 7  # Count SOS, EOS, PAD, UNK, SEP

        # copy voc
        self.copyword2index = {}
        self.index2copyword = {}
        self.num_copywords = 0

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)
            
    def addInputSentence(self, sentence):
        for word in sentence.split(' '):
            self.word_is_in_input[word] = True
            self.addWord(word)

    def addOutputSentence(self, sentence):
        for word in sentence.split(' '):
            if word not in self.word_is_in_input:
                self.word_is_in_input[word] = False
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.word2count[word] = 1
            self.index2word[self.num_words] = word
            self.num_words += 1
        else:
            self.word2count[word] += 1

    def addCopyWord(self, word):
        if word not in self.word2index:
            self.copyword2index[word] = self.num_words
            self.copyword2index[word] = 1
            self.index2copyword[self.num_words] = word
            self.num_copywords += 1
        else:
            self.word2count[word] += 1

    # Remove words below a certain count threshold
    def trim(self, min_count):
        if self.trimmed:
            return
        self.trimmed = True

        freq_words = []
        copy_words = []

        for k, v in self.word2count.items():
            if v >= min_count:
                freq_words.append(k)
            else:
                copy_words.append(k)

        print('freq_words {} / {} = {:.4f}'.format(
            len(freq_words), len(self.word2index), len(freq_words) / len(self.word2index)
        ))

        # Reinitialize dictionaries
        self.word2index = {"<PAD>": PAD_token, "<SOS>": SOS_token, "<EOS>": EOS_token, "<UNK>": UNK_token, "<SEPNUM>": SEPNUM_token, "<SEPTEP>":SEPTEP_token, "<SEPCAT>":SEPCAT_token }
        self.word2count = {"<PAD>": 0, "<SOS>": 0, "<EOS>": 0, "<UNK>": 0, "<SEPNUM>": 0, "<SEPTEP>":0, "<SEPCAT>":0 }
        self.index2word = {PAD_token: "<PAD>", SOS_token: "<SOS>", EOS_token: "<EOS>", UNK_token: "<UNK>", SEPNUM_token: "<SEPNUM>", SEPTEP_token: "<SEPTEP>", SEPCAT_token: "<SEPCAT>" }
        self.num_words = 7  # Count SOS, EOS, PAD, UNK, SEP

        for word in freq_words:
            self.addWord(word)

        for word in copy_words:
            if self.word_is_in_input[word]:
               self.addCopyWord(word)
