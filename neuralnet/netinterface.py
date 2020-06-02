import os

from tensorflow.keras.models import load_model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
from neuralnet.newnettrain import NetTrain

pd.set_option('display.max_colwidth', 200)

model = load_model('en-de-model.h5')
NN = NetTrain()


def get_word(n, tokenizer):
    if n == 0:
        return ""
    for word, index in tokenizer.word_index.items():
        if index == n:
            return word
    return ""


def encode_sequences(tokenizer, length, lines):
    seq = tokenizer.texts_to_sequences(lines)
    seq = pad_sequences(seq, maxlen=length, padding='post')
    return seq


eng_tokenizer = NN.get_eng_tokenizer()
ru_tokenizer = NN.get_ru_tokenizer()

eng_length = NN.get_eng_length()

text = "A feedback message is then  written to the browser. The names and values of these cookies are then written to the HTTP response. " \
       "Then, perform these steps to test this example. Submit the web page. " \
       "After completing these steps, you will observe that a feedback message is displayed by the  browser."

text = text.split(".")


def pass_to_encoder(text):
    # refactor text
    # phrs_enc = encode_sequences(eng_tokenizer, eng_length,)
    phrs_enc = encode_sequences(eng_tokenizer, eng_length,
                                ["the weather is nice today", "my name is tom",
                                 "how old are you", "where is the nearest shop"])

    print("phrs_enc:", phrs_enc.shape)

    preds = model.predict_classes(phrs_enc)
    print("Preds:", preds.shape)
    print(preds[0])
    print(get_word(preds[0][0], ru_tokenizer), get_word(preds[0][1], ru_tokenizer),
          get_word(preds[0][2], ru_tokenizer), get_word(preds[0][3], ru_tokenizer))
    print(preds[1])
    print(get_word(preds[1][0], ru_tokenizer), get_word(preds[1][1], ru_tokenizer),
          get_word(preds[1][2], ru_tokenizer), get_word(preds[1][3], ru_tokenizer))
    print(preds[2])
    print(get_word(preds[2][0], ru_tokenizer), get_word(preds[2][1], ru_tokenizer),
          get_word(preds[2][2], ru_tokenizer), get_word(preds[2][3], ru_tokenizer))
    print(preds[3])
    print(get_word(preds[3][0], ru_tokenizer), get_word(preds[3][1], ru_tokenizer),
          get_word(preds[3][2], ru_tokenizer), get_word(preds[3][3], ru_tokenizer))
    print()
