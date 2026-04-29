import json
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import os

class IntentClassifier:
    def __init__(self, intents_file='intents.json'):
        self.intents_file = intents_file
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        self.classifier = LogisticRegression(max_iter=200)
        self.label_encoder = LabelEncoder()
        self.intents = []
        
    def load_data(self):
        with open(self.intents_file, 'r') as file:
            data = json.load(file)
            
        self.intents = data['intents']
        
        X = []
        y = []
        
        for intent in self.intents:
            for pattern in intent['patterns']:
                X.append(pattern)
                y.append(intent['tag'])
                
        return X, y
        
    def train(self):
        print("Loading data...")
        X, y = self.load_data()
        
        print("Training model...")
        X_vec = self.vectorizer.fit_transform(X)
        y_encoded = self.label_encoder.fit_transform(y)
        
        self.classifier.fit(X_vec, y_encoded)
        
        # Save the models
        with open('model.pkl', 'wb') as f:
            pickle.dump((self.vectorizer, self.label_encoder, self.classifier), f)
            
        print("Model trained and saved successfully!")
        
    def load_model(self):
        if not os.path.exists('model.pkl'):
            self.train()
        else:
            with open('model.pkl', 'rb') as f:
                self.vectorizer, self.label_encoder, self.classifier = pickle.load(f)
                
        # Also load intents for responses
        with open(self.intents_file, 'r') as file:
            data = json.load(file)
            self.intents = data['intents']
                
    def predict_intent(self, text):
        X_vec = self.vectorizer.transform([text])
        prediction = self.classifier.predict(X_vec)
        prob = np.max(self.classifier.predict_proba(X_vec))
        
        # If probability is too low, return fallback
        if prob < 0.25:
            return "fallback"
            
        tag = self.label_encoder.inverse_transform(prediction)[0]
        return tag
        
    def get_response(self, text):
        tag = self.predict_intent(text)
        
        import random
        for intent in self.intents:
            if intent['tag'] == tag:
                return {"tag": tag, "response": random.choice(intent['responses'])}
                
        return {"tag": "fallback", "response": "I'm sorry, I couldn't process that."}

if __name__ == "__main__":
    # Test training and prediction
    model = IntentClassifier()
    model.train()
    print("Testing 'What is my balance?':", model.predict_intent("What is my balance?"))
