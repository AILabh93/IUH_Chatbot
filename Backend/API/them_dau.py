import re
import numpy as np
from nltk import ngrams
import string
from collections import Counter
import unidecode

MAXLEN = 30
NGRAM = 5
BATCH_SIZE = 1024


accented_chars_vietnamese = [
    'á', 'à', 'ả', 'ã', 'ạ', 'â', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ', 'ă', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ',
    'ó', 'ò', 'ỏ', 'õ', 'ọ', 'ô', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ', 'ơ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ',
    'é', 'è', 'ẻ', 'ẽ', 'ẹ', 'ê', 'ế', 'ề', 'ể', 'ễ', 'ệ',
    'ú', 'ù', 'ủ', 'ũ', 'ụ', 'ư', 'ứ', 'ừ', 'ử', 'ữ', 'ự',
    'í', 'ì', 'ỉ', 'ĩ', 'ị',
    'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ',
    'đ',
]
accented_chars_vietnamese.extend([c.upper()
                                  for c in accented_chars_vietnamese])
alphabet = list(('\x00 _' + string.ascii_letters
                 + string.digits + ''.join(accented_chars_vietnamese)))


def remove_accent(text):
    return unidecode.unidecode(text)


def gen_ngrams(words, n=5):
    return ngrams(words.split(), n)


def encode(text, maxlen=MAXLEN):

    text = "\x00" + text
    x = np.zeros((maxlen, len(alphabet)))
    for i, c in enumerate(text[:maxlen]):
        x[i, alphabet.index(c)] = 1
    if i < maxlen - 1:
        for j in range(i + 1, maxlen):
            x[j, 0] = 1
    return x


def decode(x, calc_argmax=True):
    if calc_argmax:
        x = x.argmax(axis=-1)
    return ''.join(alphabet[i] for i in x)


def extract_phrases(text):
    pattern = r'\w[\w ]*|\s\W+|\W+'
    return re.findall(pattern, text)


def guess(ngram, model):
    text = ' '.join(ngram)

    preds = model.predict(np.array([encode(text)]), verbose=0)
    return decode(preds[0], calc_argmax=True).strip('\x00')


def add_accent(text, model):
    ngrams = list(gen_ngrams(text.lower(), n=NGRAM))
    guessed_ngrams = list(guess(ngram, model) for ngram in ngrams)

    candidates = [Counter() for _ in range(len(guessed_ngrams) + NGRAM - 1)]
    for nid, ngram in enumerate(guessed_ngrams):
        for wid, word in enumerate(re.split(' +', ngram)):
            candidates[nid + wid].update([word])
    output = ' '.join(c.most_common(1)[0][0] for c in candidates)
    return output


def accent_sentence(sentence, model):
    list_phrases = extract_phrases(sentence)
    output = ""
    for phrases in list_phrases:
        if len(phrases.split()) < 2 or not re.match("\w[\w ]+", phrases):
            output += phrases
        else:
            output += add_accent(phrases, model)
            if phrases[-1] == " ":
                output += " "
    return output
