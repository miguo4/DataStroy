import itertools

# Default word tokens
PAD_token = 0  # Used for padding short sentences
SOS_token = 1  # Start-of-sentence token
EOS_token = 2  # End-of-sentence token
UNK_token = 3  # Unknown token

def indexesFromSentence(voc, sentence, input_sentence=''):
    indexes = []
    input_sentence_tokens = input_sentence.split(' ')
    for word in sentence.split(' '):
        if word == '<PAD>':
            indexes += [PAD_token]
        elif word in voc.word2index:
            # Generate Mode
            indexes += [voc.word2index[word]]
        elif word in voc.copyword2index and word in input_sentence_tokens:
            # Copy Mode
            copy_index = input_sentence_tokens.index(word)
            indexes += [voc.num_words + copy_index]
        else:
            # Out of vocabulary
            indexes += [UNK_token]
            
    indexes += [EOS_token]
    return indexes


def zeroPadding(l, fillvalue=PAD_token):
    return list(itertools.zip_longest(*l, fillvalue=fillvalue))

def binaryMatrix(l, value=PAD_token):
    m = []
    for i, seq in enumerate(l):
        m.append([])
        for token in seq:
            if token == PAD_token:
                m[i].append(0)
            else:
                m[i].append(1)
    return m