 
import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

# Charger les données JSON
with open("intentions_generales.json", 'r') as file:
    data = json.load(file)

    
# Extraire les patterns et les tags
patterns = []
tags = []
for intent in data['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        tags.append(intent['tag'])

# Division des données en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(patterns, tags, test_size=0.2, random_state=42,stratify=tags  )

# Créer un pipeline de traitement avec TF-IDF et SVM
model = make_pipeline(TfidfVectorizer(), SVC(kernel='linear'))

# Entraîner le modèle
model.fit(X_train, y_train)

# Évaluer le modèle
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))

# Utiliser le modèle pour prédire un nouveau texte
def predict_tag(text):
    return model.predict([text])[0]

# Exemple d'utilisation
print(predict_tag("can you say it in english"))

