import pickle
import pandas as pd
import numpy as np
import re
import gensim
import nltk
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from  nltk.stem import SnowballStemmer
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from sklearn.preprocessing import LabelEncoder
from keras.layers import Dense, Dropout, Embedding, LSTM
from keras.models import Sequential
from keras.callbacks import ReduceLROnPlateau, EarlyStopping

decode_map = {0: "negative", 2: "neutral", 4: "positive"}
stop_words = stopwords.words("english")
stemmer = SnowballStemmer("english")

def loadData():
    with open('data/data_training.csv', 'r', encoding='ISO-8859-1') as file:
        loadData = file.readlines()
        
    data = pd.DataFrame([row.strip('"').split('","') for row in loadData], columns=["sentiment", "id", "data", "query", "user", "text"])
    return data


def preprocess(text, stem=False):
    # Remove link,user and special characters
    text = re.sub("@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+", ' ', str(text).lower()).strip()
    tokens = []
    
    for token in text.split():
        if token not in stop_words:
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                tokens.append(token)
    return " ".join(tokens)


def decode_sentiment(label):
    return decode_map[int(label)]


def getSequentialModel(embedding_layer):
    model = Sequential()
    model.add(embedding_layer)
    model.add(Dropout(0.5))
    model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(1, activation='sigmoid'))
    
    model.summary()
    
    model.compile(loss='binary_crossentropy',
              optimizer="adam",
              metrics=['accuracy'])
    return model

        
def createNewModel():
    nltk.download('stopwords')
    
    data = loadData()
    data.sentiment = data.sentiment.apply(lambda x: decode_sentiment(x))
    data.text = data.text.apply(lambda x: preprocess(x))
    data_train, data_test = train_test_split(data, test_size=0.2, random_state=42)

    documents = [_text.split() for _text in data_train.text] 
    w2v_model = gensim.models.word2vec.Word2Vec(vector_size=300, window=7, min_count=10, workers=8)
    w2v_model.build_vocab(documents)
    
    words = w2v_model.wv.index_to_key
    vocab_size = len(words)
    
    w2v_model.train(documents, total_examples=len(documents), epochs=32)
    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(data_train.text)
    
    x_train = pad_sequences(tokenizer.texts_to_sequences(data_train.text), maxlen=300)
    x_test = pad_sequences(tokenizer.texts_to_sequences(data_test.text), maxlen=300)
    
    labels = data_train.sentiment.unique().tolist()
    labels.append("neutral")
    
    encoder = LabelEncoder()
    encoder.fit(data_train.sentiment.tolist())
    
    y_train = encoder.transform(data_train.sentiment.tolist())
    y_test = encoder.transform(data_test.sentiment.tolist())
    
    y_train = y_train.reshape(-1,1)
    y_test = y_test.reshape(-1,1)
    
    embedding_matrix = np.zeros((vocab_size, 300))
    for word, i in tokenizer.word_index.items():
        if word in w2v_model.wv:
            embedding_matrix[i] = w2v_model.wv[word]

    embedding_layer = Embedding(vocab_size, 300, weights=[embedding_matrix], input_length=300, trainable=False)

    model = getSequentialModel(embedding_layer)
    
    callbacks = [ ReduceLROnPlateau(monitor='val_loss', patience=5, cooldown=0),
              EarlyStopping(monitor='val_acc', min_delta=1e-4, patience=5)]
    
    
    model.fit(x_train, y_train,
                    batch_size=1024,
                    epochs=8,
                    validation_split=0.1,
                    verbose=1,
                    callbacks=callbacks)
    
    
    model.save("data/model.h5")
    w2v_model.save("data/model.w2v")
    pickle.dump(tokenizer, open("data/tokenizer.pkl", "wb"), protocol=0)
    pickle.dump(encoder, open("data/encoder.pkl", "wb"), protocol=0)
    
    return model, w2v_model, tokenizer, encoder
    
