import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np
import string
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, RepeatVector, Dropout
from tensorflow.keras import optimizers

pd.set_option('display.max_colwidth', 200)
# file = "C:/Users/Екатерина/PycharmProjects/app/neuralnet/deutch.txt"
# file_en = "C:/Users/Екатерина/PycharmProjects/app/neuralnet/shildt-en-prepared.txt"
# file_ru = "C:/Users/Екатерина/PycharmProjects/app/neuralnet/shildt-ru-prepared.txt"

# Массивы параллельных текстов
file_en = "./neuralnet/shildt-en-prepared.txt"
file_ru = "./neuralnet/shildt-ru-prepared.txt"

# Класс обучения нейронной сети
class NetTrain:
    def __init__(self):
        # data = self.read_text(file_en, file_ru)
        data = self.read_text(file_en, file_ru)
        ru_eng = np.array(data)
        ru_eng = ru_eng[:30000, :]
        # print("Dictionary size:", ru_eng.shape)

        # Исключение знаков пунктуации
        ru_eng[:, 0] = [s.translate(str.maketrans('', '', string.punctuation)) for s in ru_eng[:, 0]]
        ru_eng[:, 1] = [s.translate(str.maketrans('', '', string.punctuation)) for s in ru_eng[:, 1]]

        # Приведение букв к нижнему регистру
        for i in range(len(ru_eng)):
            ru_eng[i, 0] = ru_eng[i, 0].lower()
            ru_eng[i, 1] = ru_eng[i, 1].lower()

        # Представление слов векторами
        self.eng_tokenizer = Tokenizer()
        self.eng_tokenizer.fit_on_texts(ru_eng[:, 0])
        eng_vocab_size = len(self.eng_tokenizer.word_index) + 1
        self.eng_length = 8

        self.ru_tokenizer = Tokenizer()
        self.ru_tokenizer.fit_on_texts(ru_eng[:, 1])
        ru_vocab_size = len(self.ru_tokenizer.word_index) + 1
        ru_length = 8

        # Разделение выборки на обучающую и тестовую
        # (соотношение 80/20)
        train, test = train_test_split(ru_eng, test_size=0.2, random_state=12)
        # encode sentences for training
        trainX = self.encode_sequences(self.eng_tokenizer, self.eng_length, train[:, 0])
        trainY = self.encode_sequences(self.ru_tokenizer, ru_length, train[:, 1])

        # Шифрование тестовой выборки
        testX = self.encode_sequences(self.eng_tokenizer, self.eng_length, test[:, 0])
        testY = self.encode_sequences(self.ru_tokenizer, ru_length, test[:, 1])

        print("ru_vocab_size: ", ru_vocab_size, ru_length)
        print("eng_vocab_size: ", eng_vocab_size, self.eng_length)

        # Создание модели
        model = self.make_model(eng_vocab_size, ru_vocab_size, self.eng_length, ru_length, 512)
        num_epochs = 1
        history = model.fit(trainX, trainY.reshape(trainY.shape[0], trainY.shape[1], 1),
                            epochs=num_epochs, batch_size=512, validation_split=0.2, callbacks=None, verbose=1)

        # Сохранение модели в файл
        model.save('example1.h5')
        print(model.summary())

    # lstm_param = 512/256/128
    def create_model(self, eng_vocab_size, ru_vocab_size, eng_length, ru_length, lstm_param, name_model):
        model = self.make_model(eng_vocab_size, ru_vocab_size, eng_length, ru_length, lstm_param)
        model.save(name_model)
        return model

    # was history = ...
    def fit_model(self, model, trainX, trainY, num_epochs):
        return model.fit(trainX, trainY.reshape(trainY.shape[0], trainY.shape[1], 1),
                         epochs=num_epochs, batch_size=512, validation_split=0.2, callbacks=None, verbose=1)

    # --------MY FILE READING (USING 2 FILES)-------- #
    def read_text(self, file_init, file_targ):

        with open(file_init, mode='rt', encoding="utf8") as file:
            text = file.read()
            sents_init = text.strip().split('\n')
            file.close()
            # returns list [[E, G], [E2, G2], ...]
            # return [i.split('\t') for i in sents]
            # return sents

        with open(file_targ, mode='rt', encoding="utf8") as file:
            text = file.read()
            sents_targ = text.strip().split('\n')
            file.close()

        length = len(sents_init)

        list_all = []
        for i in range(length):
            list_all.append([sents_init[i]]+[sents_targ[i]])
            # list_all.append([sents_init[i]+"\t"+sents_targ[i]])

        return list_all

    # --------INITIAL FILE READING (USING 1 FILE)-------- #
    # def read_text(self, filename):
    #     with open(filename, mode='rt', encoding='utf-8') as file:
    #         # returns a string
    #         text = file.read()
    #         # split() returns list of words
    #         # strip() removes spaces from the ends
    #         sents = text.strip().split('\n')
    #         # returns list [['E', 'G'], ['E2', 'G2'], ...]
    #     return [i.split('\t') for i in sents]

    def encode_sequences(self, tokenizer, length, lines):
        seq = tokenizer.texts_to_sequences(lines)
        seq = pad_sequences(seq, maxlen=length, padding='post')
        return seq

    def make_model(self, in_vocab, out_vocab, in_timesteps, out_timesteps, n):

        model = Sequential()
        model.add(Embedding(in_vocab, n, input_length=in_timesteps, mask_zero=True))
        model.add(LSTM(n))
        model.add(Dropout(0.3))
        model.add(RepeatVector(out_timesteps))
        model.add(LSTM(n, return_sequences=True))
        model.add(Dropout(0.3))
        model.add(Dense(out_vocab, activation='softmax'))
        model.compile(optimizer=optimizers.RMSprop(lr=0.001), loss='sparse_categorical_crossentropy')
        return model

    def get_ru_tokenizer(self):
        return self.ru_tokenizer

    def get_eng_tokenizer(self):
        return self.eng_tokenizer

    def get_eng_length(self):
        return self.eng_length
