import tensorflow as tf
import re
import numpy as np
import string
import nltk
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
import time
import itertools
from collections import Counter
from tensorflow.keras.models import load_model
from . import themDau


class Vocab():
    def __init__(self, chars):
        self.pad = 0
        self.go = 1
        self.eos = 2

        self.chars = chars
        self.c2i = {c: i + 3 for i, c in enumerate(chars)}
        self.i2c = {i + 3: c for i, c in enumerate(chars)}

        self.i2c[0] = '<pad>'
        self.i2c[1] = '<sos>'
        self.i2c[2] = '<eos>'

    def encode(self, chars):
        return [self.go] + [self.c2i[c] for c in chars] + [self.eos]

    def decode(self, ids):
        ids = [i for i in ids]
        first = 1 if self.go in ids else 0
        last = ids.index(self.eos) if self.eos in ids else None
        sent = ''.join([self.i2c[i] for i in ids[first:last]])
        return sent

    def __len__(self):
        return len(self.c2i) + 3

    def decode_split(self, ids):
        ids = [i for i in ids]
        first = 1 if self.go in ids else 0
        last = ids.index(self.eos) if self.eos in ids else None
        return [self.i2c[i] for i in ids[first:last]]


alphabets = 'aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0123456789 '
vocab = Vocab(alphabets)
ENC_EMB_DIM = 256
DEC_EMB_DIM = 256
ENC_HID_DIM = 512
DEC_HID_DIM = 512
vocab_size = vocab.__len__()
BATCH_SIZE = 64
MAXLEN = 40


def preprocessing_data(row):
    row = row.lower()
    processed = re.sub(
        r'[^aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0123456789 ]',
        "", row)
    return ''.join([i for i in row if i in alphabets])


class Encoder(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, enc_units, batch_sz):
        super(Encoder, self).__init__()
        self.batch_sz = batch_sz
        self.enc_units = enc_units
        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.lstm = tf.keras.layers.LSTM(self.enc_units,
                                         return_sequences=True,
                                         return_state=True)
        self.bi = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(self.enc_units,
                                                                     return_sequences=True,
                                                                     return_state=True))

    def call(self, x, hidden):

        x = self.embedding(x)
        output, state_h, state_c = self.lstm(x, initial_state=[hidden, hidden])
        # print(state_h.shape)
        return output, state_h, state_c
    # khởi tạo first state để  trả về last state

    def initialize_hidden_state(self):
        return tf.zeros((self.batch_sz, self.enc_units))


class BahdanauAttention(tf.keras.layers.Layer):
    def __init__(self, units):
        super(BahdanauAttention, self).__init__()
        self.W1 = tf.keras.layers.Dense(units)
        self.W2 = tf.keras.layers.Dense(units)
        self.V = tf.keras.layers.Dense(1)

    def call(self, query, values):
        query_with_time_axis = tf.expand_dims(query, 1)

        score = self.V(tf.nn.tanh(
            self.W1(query_with_time_axis) + self.W2(values)))

        # attention_weights shape == (batch_size, max_length, 1)
        attention_weights = tf.nn.softmax(score, axis=1)

        # context_vector shape after sum == (batch_size, hidden_size)
        context_vector = attention_weights * values
        context_vector = tf.reduce_sum(context_vector, axis=1)

        return context_vector, attention_weights


class Decoder(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, dec_units, batch_sz):
        super(Decoder, self).__init__()
        self.batch_sz = batch_sz
        self.dec_units = dec_units
        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.lstm = tf.keras.layers.LSTM(self.dec_units,
                                         return_sequences=True,
                                         return_state=True)
        self.fc = tf.keras.layers.Dense(vocab_size)

        # used for attention
        self.attention = BahdanauAttention(self.dec_units)

    def call(self, x, hidden, enc_output):
        # enc_output shape == (batch_size, max_length, hidden_size)
        context_vector, attention_weights = self.attention(
            hidden[0], enc_output)

        # x shape after passing through embedding == (batch_size, 1, embedding_dim)
        x = self.embedding(x)

        # x shape after concatenation == (batch_size, 1, embedding_dim + hidden_size)
        x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=-1)

        output, state_h, state_c = self.lstm(x, initial_state=hidden)

        # output shape == (batch_size * 1, hidden_size)
        output = tf.reshape(output, (-1, output.shape[2]))

        # output shape == (batch_size, vocab)
        x = self.fc(output)

        # trả về last state của decode cho lần train từ kế tiếp
        return x, state_h, state_c, attention_weights


class CustomSchedule(tf.keras.optimizers.schedules.LearningRateSchedule):
    def __init__(self, d_model, warmup_steps=4000):
        super(CustomSchedule, self).__init__()

        self.d_model = d_model
        self.d_model = tf.cast(self.d_model, tf.float32)

        self.warmup_steps = warmup_steps

    def __call__(self, step):
        arg1 = tf.math.rsqrt(step)
        arg2 = step * (self.warmup_steps ** -1.5)

        return tf.math.rsqrt(self.d_model) * tf.math.minimum(arg1, arg2)


optimizer = tf.keras.optimizers.Adam(CustomSchedule(256), beta_1=0.9, beta_2=0.98,
                                     epsilon=1e-9)
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(
    from_logits=True, reduction='none')


def loss_function(real, pred):
    mask = tf.math.logical_not(tf.math.equal(real, 0))
    loss_ = loss_object(real, pred)
    mask = tf.cast(mask, dtype=loss_.dtype)
    loss_ *= mask
    return tf.reduce_mean(loss_)


def evaluate(inputs, encoder, decoder, model):
    inputs = [vocab.encode(' '.join(inputs))]
    inputs = tf.keras.preprocessing.sequence.pad_sequences(
        inputs, maxlen=MAXLEN, padding='post')
    inputs = tf.convert_to_tensor(inputs)
    result = []
    hidden = tf.zeros((1, ENC_HID_DIM))
    enc_out, state_h, state_c = encoder(inputs, hidden)
    dec_input = tf.expand_dims([vocab.go], 0)
    for t in range(MAXLEN):
        dec_hidden = [state_h, state_c]
        predictions, state_h, state_c, attention_weights = decoder(dec_input,
                                                                   dec_hidden,
                                                                   enc_out)

        attention_weights = tf.reshape(attention_weights, (-1, ))
        predicted_id = tf.argmax(predictions[0]).numpy()
        result.append(predicted_id)
        if predicted_id == vocab.eos:
            return themDau.add_accent(vocab.decode(result), model)
        dec_input = tf.expand_dims([predicted_id], 0)

    return themDau.add_accent(vocab.decode(result), model)


def gen_ngrams(text, n=5):
    tokens = text.split()
    if len(tokens) < n:
        return [tokens]

    return nltk.ngrams(text.split(), n)


def change_error(text, encoder, decoder, model):
    text = preprocessing_data(text)
    list_ngrams = gen_ngrams(text)
    guessed_ngrams = list(evaluate(ngram, encoder, decoder, model)
                          for ngram in list_ngrams)
    candidates = [Counter() for _ in range(len(guessed_ngrams) + 4)]
    for nid, ngram in enumerate(guessed_ngrams):
        for wid, word in enumerate(re.split(' +', ngram)):
            candidates[nid + wid].update([word])
    result = []
    for c in candidates:
        try:
            result.append(c.most_common(1)[0][0])
        except:
            break
    output = ' '.join(result)
    return output


# if __name__ == "__main__":
# encoder = Encoder(vocab_size, ENC_EMB_DIM, ENC_HID_DIM, BATCH_SIZE)
# decoder = Decoder(vocab_size, DEC_EMB_DIM, DEC_HID_DIM, BATCH_SIZE)
# checkpoint_dir = 'checkpoint'
# checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
# checkpoint = tf.train.Checkpoint(optimizer=optimizer,
#                                  encoder=encoder,
#                                  decoder=decoder)
# checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))
