import re
import unicodedata
from .vocab import Voc

def loadQuestions(filename, fields):
    questions = []
    with open(filename, 'r', encoding='iso-8859-1') as f:
        for line in f:
            try:
                line = line.replace('\n', ' ')
                line = line.replace('"', '')
                values = line.split("\t")
                # Extract fields
                questionObj = {}
                for i, field in enumerate(fields):
                    questionObj[field] = values[i]
                questions.append(questionObj)
            except:
                continue
    return questions

def extractQuestionPairs(questions):
    qd_pairs = []
    for q_obj in questions:
        originQ = q_obj["question"] + " <SEPNUM> " + q_obj["numerical"] + " <SEPTEP> " + q_obj["temporal"] + " <SEPCAT> " + q_obj["categorical"]
        subQ1 = q_obj["subquestion1"]
        subQ2 = q_obj["subquestion2"]
        questiontype = q_obj["type"]
        qd_pairs.append([originQ, subQ1, subQ2, questiontype])
    return qd_pairs

# Turn a Unicode string to plain ASCII, thanks to
# https://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# Lowercase, trim, and remove non-letter characters
def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    s = s.replace("sepnum","<SEPNUM>")
    s = s.replace("septep","<SEPTEP>")
    s = s.replace("sepcat","<SEPCAT>")
    return s

# Read query/response pairs and return a voc object
def readVocs(datafile, corpus_name):
    print("Reading lines...")
    # Read the file and split into lines
    lines = open(datafile, encoding='utf-8').\
        read().strip().split('\n')
    # Split every line into pairs and normalize
    pairs = [[normalizeString(s) for s in l.split('\t')] for l in lines]
    voc = Voc(corpus_name)
    return voc, pairs

# Returns True iff both sentences in a pair 'p' are under the MAX_LENGTH threshold
def filterPair(p, max_length):
    # Input sequences need to preserve the last word for EOS token
    return len(p[0].split(' ')) < max_length and len(p[1].split(' ')) < max_length

# Filter pairs using filterPair condition
def filterPairs(pairs, max_length):
    return [pair for pair in pairs if filterPair(pair, max_length)]

# Using the functions defined above, return a populated voc object and pairs list
def loadPrepareData(corpus, corpus_name, datafile, save_dir, max_length):
    print("Start preparing training data ...")
    voc, pairs = readVocs(datafile, corpus_name)
    print("Read {!s} sentence pairs".format(len(pairs)))
    pairs = filterPairs(pairs, max_length)
    print("Trimmed to {!s} sentence pairs".format(len(pairs)))
    print("Counting words...")
    for pair in pairs:
        voc.addInputSentence(pair[0])
        voc.addOutputSentence(pair[1])
        voc.addOutputSentence(pair[2])
    print("Counted words:", voc.num_words)
    return voc, pairs

def trimRareWords(voc, pairs, MIN_COUNT):
    # Trim words used under the MIN_COUNT from the voc
    voc.trim(MIN_COUNT)
    # Filter out pairs with trimmed words
    keep_pairs = []
    for pair in pairs:
        input_sentence = pair[0]
        output_sentence_1 = pair[1]
        output_sentence_2 = pair[2]
        keep_input = True
        keep_output = True
        # Check input sentence
        for word in input_sentence.split(' '):
            if word not in voc.word2index and word not in voc.copyword2index:
                keep_input = False
                break
        # Check output sentence
        for word in output_sentence_1.split(' '):
            if word not in voc.word2index and word not in voc.copyword2index:
                keep_output = False
                break
        for word in output_sentence_2.split(' '):
            if word not in voc.word2index and word not in voc.copyword2index:
                keep_output = False
                break

        # Only keep pairs that do not contain trimmed word(s) in their input or output sentence
        if keep_input and keep_output:
            keep_pairs.append(pair)

    print("Trimmed from {} pairs to {}, {:.4f} of total".format(len(pairs), len(keep_pairs), len(keep_pairs) / len(pairs)))
    return keep_pairs

def replaceRareWords(voc, pairs, MIN_COUNT):
    # Replace words used under the MIN_COUNT from the voc
    voc.trim(MIN_COUNT)
    # Filter out pairs with trimmed words
    keep_pairs = []
    for pair in pairs:
        input_sentence = pair[0]
        output_sentence_1 = pair[1]
        output_sentence_2 = pair[2]
        keep_input = True
        keep_output = True
        # Check input sentence
        replaced_input_sentence = ''
        for word in input_sentence.split(' '):
            if word not in voc.word2index and word not in voc.copyword2index:
                replaced_input_sentence += "<UNK>"
            else:
                replaced_input_sentence += word
            replaced_input_sentence += " "
        pair[0] = replaced_input_sentence[:-1] # remove lask blank
        # Check output sentence
        replaced_output_sentence_1 = ''
        for word in output_sentence_1.split(' '):
            if word not in voc.word2index and word not in voc.copyword2index:
                replaced_output_sentence_1 += "<UNK>"
            else:
                replaced_output_sentence_1 += word
            replaced_output_sentence_1 += " "
        pair[1] = replaced_output_sentence_1[:-1]

        replaced_output_sentence_2 = ''
        for word in output_sentence_2.split(' '):
            if word not in voc.word2index and word not in voc.copyword2index:
                replaced_output_sentence_2 += "<UNK>"
            else:
                replaced_output_sentence_2 += word
            replaced_output_sentence_2 += " "
        pair[2] = replaced_output_sentence_2[:-1]

        keep_pairs.append(pair)

    print("Replaced from {} pairs to {}, {:.4f} of total".format(len(pairs), len(keep_pairs), len(keep_pairs) / len(pairs)))
    return keep_pairs