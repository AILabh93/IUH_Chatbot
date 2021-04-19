import itertools
from tensorflow.keras.models import load_model
import re
import unidecode
import nltk
import string
import numpy as np
from collections import Counter

MAXLEN = 30

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
alphabet = list(('\x00 _' + string.ascii_letters +
                string.digits + ''.join(accented_chars_vietnamese)))


def remove_accent(text):
    return unidecode.unidecode(text)


def encode(text, maxlen=MAXLEN):
    text = "\x00" + text
    x = np.zeros((maxlen, len(alphabet)))
    for i, c in enumerate(text[:maxlen]):
        x[i, alphabet.index(c)] = 1
    if i < maxlen - 1:
        for j in range(i+1, maxlen):
            x[j, 0] = 1
    return x


def decode(x, calc_argmax=True):
    if calc_argmax:
        x = x.argmax(axis=-1)
    return ''.join(alphabet[i] for i in x)


def guess(ngram, model):
    text = ' '.join(ngram)
    preds = model.predict(np.array([encode(text)]), verbose=0)
    return decode(preds[0], calc_argmax=True).strip('\x00')


def add_accent(text, model):
    text = remove_accent(text)
    guessed_ngrams = list(guess(text.split(), model))
    return ''.join(guessed_ngrams)


if __name__ == "__main__":
    model = load_model('checkpoint/model.h5')
    print(add_accent('xin chao', model))
