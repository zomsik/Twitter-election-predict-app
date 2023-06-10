
# Save Model Using Pickle
import pickle
import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from data.get_tweets import get_tweets
folder = 'model/'



def vectorizeModel(X_train, X_test):

    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    return X_train_vec, X_test_vec


def classifyModel(X_train_vec, y_train):
    classifier = RandomForestClassifier()
    classifier.fit(X_train_vec, y_train)

    return classifier

def predictModel(classifier, X_test_vec):
    
    y_pred = classifier.predict(X_test_vec)
    return y_pred



def saveModel(learningModel):
    pickle.dump(learningModel, open('model.sav', 'wb'))
    
def loadModel():
    
    #path = os.path.join(folder, filename)
    if os.path.exists('model.sav'):
        learningModel = pickle.load(open('model.sav', 'rb'))
    else:
        learningModel = makeNewModel()
        
    return learningModel
        
        
def makeNewModel():
    with open('data/data_training.csv', 'r', encoding='latin-1') as file:
        loadData = file.readlines()

    data = pd.DataFrame([row.strip('"').split('","') for row in loadData], columns=["sentiment", "id", "data", "query", "user", "text"])

    x = data['text'].values
    y = data['sentiment'].values
    
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(x)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    
    
    
    model = LogisticRegression()

    # Trenowanie modelu
    model.fit(X_train, y_train)

    # Ocena modelu na zbiorze testowym
    accuracy = model.score(X_test, y_test)
    print(f"Dokładność modelu: {accuracy}")
    return
    
    X_train_vec, X_test_vec = vectorizeModel(X_train, X_test)
    
    classifier = classifyModel(X_train_vec, y_train)
    
    y_pred = predictModel(classifier, X_test_vec)
    
    accuracy = (y_pred == y_test).mean()
    print("Accuracy:", accuracy)
    learningModel = None
    saveModel(learningModel)
    return classifier
    
def check():
    a = loadModel()
    return

makeNewModel()

