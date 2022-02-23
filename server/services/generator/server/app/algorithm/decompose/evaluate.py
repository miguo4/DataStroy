import torch
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.meteor_score import meteor_score
from .process import normalizeString
from .utils import indexesFromSentence
import traceback

def token2sentence(tokens, voc, sentence_voc):
    decoded_words = []
    for token in tokens:
        if token.item() < voc.num_words:
            decoded_words.append(voc.index2word[token.item()])
        elif token.item() >= voc.num_words and token.item() < (voc.num_words + len(sentence_voc.keys())):
            decoded_words.append(sentence_voc[token.item()-voc.num_words])
        else:
            decoded_words.append('<UNK>')
    return decoded_words

def evaluate(searcher, voc, sentence, questiontype, max_length, device):
    ### Format input sentence as a batch
    # words -> indexes
    indexes_batch = [indexesFromSentence(voc, sentence)]
    # Create lengths tensor
    lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
    # Transpose dimensions of batch to match models' expectations
    input_batch = torch.LongTensor(indexes_batch).transpose(0, 1)
    # Use appropriate device
    input_batch = input_batch.to(device)
    # lengths = lengths.to(device)
    lengths = torch.as_tensor(lengths, dtype=torch.int64, device=device)
    # Decode sentence with searcher
    tokens_1, scores_1, tokens_2, scores_2 = searcher(input_batch, lengths, max_length, questiontype)
    # indexes -> words
    sentence_voc = {}
    for index, word in enumerate(sentence.split(' ')):
        sentence_voc[index] = word
    decoded_words_1 = token2sentence(tokens_1, voc, sentence_voc)
    decoded_words_2 = token2sentence(tokens_2, voc, sentence_voc)
    return decoded_words_1, decoded_words_2

def BLEU_score(reference, candidate):
    reference = reference.split(' ')
    references = [reference]
    candidate = candidate.split(' ')
    BLEU_1 = sentence_bleu(references, candidate, weights=(1, 0, 0, 0))
    BLEU_2 = sentence_bleu(references, candidate, weights=(0.5, 0.5, 0, 0))
    BLEU_3 = sentence_bleu(references, candidate, weights=(0.33, 0.33, 0.33, 0))
    BLEU_4 = sentence_bleu(references, candidate, weights=(0.25, 0.25, 0.25, 0.25))

    return BLEU_1, BLEU_2, BLEU_3, BLEU_4

def evaluateBLEU(test_pairs, searcher, voc, max_length, device):
    BLEU_1 = 0
    BLEU_2 = 0
    BLEU_3 = 0
    BLEU_4 = 0

    for test_pair in test_pairs:
        input_sentence = normalizeString(test_pair[0])
        # Replace unknown words
        replaced_input_sentence = ''
        for word in input_sentence.split(' '):
            if word not in voc.word2index and word not in voc.copyword2index:
                replaced_input_sentence += "<UNK>"
            else:
                replaced_input_sentence += word
            replaced_input_sentence += " "
        input_sentence = replaced_input_sentence[:-1]
        input_type = test_pair[3]
        # Evaluate sentence
        output_words_1, output_words_2 = evaluate(searcher, voc, input_sentence, input_type, max_length, device)
        # Format and print response sentence
        output_words_1[:] = [x for x in output_words_1 if not (x == '<EOS>' or x == '<PAD>')]
        output_words_2[:] = [x for x in output_words_2 if not (x == '<EOS>' or x == '<PAD>')]
        text1 = ' '.join(output_words_1)
        text1 = text1.partition("?")[0]
        text1 = text1.partition(".")[0]
        text2 = ' '.join(output_words_2)
        text2 = text2.partition("?")[0]
        text2 = text2.partition(".")[0]

        b1_1, b2_1, b3_1, b4_1 = BLEU_score(text1, test_pair[1])
        b1_2, b2_2, b3_2, b4_2 = BLEU_score(text2, test_pair[2])
        BLEU_1 += (b1_1+b1_2) / 2
        BLEU_2 += (b2_1+b2_2) / 2
        BLEU_3 += (b3_1+b3_2) / 2
        BLEU_4 += (b4_1+b4_2) / 2

    BLEU_1 = BLEU_1 / len(test_pairs)
    BLEU_2 = BLEU_2 / len(test_pairs)
    BLEU_3 = BLEU_3 / len(test_pairs)
    BLEU_4 = BLEU_4 / len(test_pairs)

    print('BLEU_1: %s'%(BLEU_1))
    print('BLEU_2: %s'%(BLEU_2))
    print('BLEU_3: %s'%(BLEU_3))
    print('BLEU_4: %s'%(BLEU_4))

    # return BLEU_1, BLEU_2, BLEU_3, BLEU_4

def METEOR_score(reference, candidate):
    references = [reference]
    METEOR = meteor_score(references, candidate)

    return METEOR

def evaluateMETEOR(test_pairs, searcher, voc, max_length, device):
    METEOR = 0

    for test_pair in test_pairs:
        input_sentence = normalizeString(test_pair[0])
        # Replace unknown words
        replaced_input_sentence = ''
        for word in input_sentence.split(' '):
            if word not in voc.word2index and word not in voc.copyword2index:
                replaced_input_sentence += "<UNK>"
            else:
                replaced_input_sentence += word
            replaced_input_sentence += " "
        input_sentence = replaced_input_sentence[:-1]
        input_type = test_pair[3]
        # Evaluate sentence
        output_words_1, output_words_2 = evaluate(searcher, voc, input_sentence, input_type, max_length, device)
        # Format and print response sentence
        output_words_1[:] = [x for x in output_words_1 if not (x == '<EOS>' or x == '<PAD>')]
        output_words_2[:] = [x for x in output_words_2 if not (x == '<EOS>' or x == '<PAD>')]
        text1 = ' '.join(output_words_1)
        text1 = text1.partition("?")[0]
        text1 = text1.partition(".")[0]
        text2 = ' '.join(output_words_2)
        text2 = text2.partition("?")[0]
        text2 = text2.partition(".")[0]

        m_1 = METEOR_score(text1, test_pair[1])
        m_2 = METEOR_score(text2, test_pair[2])
        METEOR += (m_1+m_2) / 2

    METEOR = METEOR / len(test_pairs)

    print('METEOR: %s'%(METEOR))


def evaluateInput(input_sentence, input_type, searcher, voc, max_length, device):
    try:
        input_sentence = normalizeString(input_sentence)
        # Replace unknown words    
        # replaced_input_sentence = ''
        # for word in input_sentence.split(' '):
        #     if word not in voc.word2index and word not in voc.copyword2index:
        #         replaced_input_sentence += "<UNK>"
        #     else:
        #         replaced_input_sentence += word
        #     replaced_input_sentence += " "
        # input_sentence = replaced_input_sentence[:-1]
        # print("final sentence: %s"%(input_sentence))
        # Evaluate sentence
        output_words_1, output_words_2 = evaluate(searcher, voc, input_sentence, input_type, max_length, device)
        # Format and print response sentence
        output_words_1[:] = [x for x in output_words_1 if not (x == '<EOS>' or x == '<PAD>')]
        output_words_2[:] = [x for x in output_words_2 if not (x == '<EOS>' or x == '<PAD>')]
        text1 = ' '.join(output_words_1)
        text1 = text1.partition("?")[0]
        text1 = text1.partition(".")[0]
        text2 = ' '.join(output_words_2)
        text2 = text2.partition("?")[0]
        text2 = text2.partition(".")[0]
        return text1, text2

    except Exception as e:
        print('********************************')
        print(traceback.format_exc())
        print("question cannot be decomposed")