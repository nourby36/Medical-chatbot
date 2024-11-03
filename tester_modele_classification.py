from transformers import BertForSequenceClassification, BertTokenizer
import torch
import torch.nn.functional as F  
from tester_modele_classification_generales import find_word_from_index
from traduire import traduire_en_ch



# print("Probabilités de chaque classe:", probs)
# print("Classe prédite:", predicted_class.item())


def predict_intention(text):
    # Définir le chemin vers le répertoire contenant votre modèle enregistré
    model_dir = "C:\\Users\\MSI\\Desktop\\IDS4\\sem2\\NLP\\PROJET\\modele_classification1"

    # Charger le tokenizer
    tokenizer =BertTokenizer.from_pretrained('hfl/chinese-bert-wwm')

    # Charger le modèle
    model = BertForSequenceClassification.from_pretrained(model_dir)
    # Exemple de texte à classer
    # text = "what is the desease called Paralysis"
    text = traduire_en_ch(text)

    # Prétraitement du texte
    inputs = tokenizer(text, padding=True, truncation=True, max_length=128, return_tensors="pt")

    # Prédiction
    with torch.no_grad():
        outputs = model(**inputs)

    # Récupération des prédictions
    logits = outputs.logits

    # Application de la fonction softmax pour obtenir des probabilités
    probs = F.softmax(logits, dim=1)

    # Récupération de l'indice de la classe prédite
    predicted_class = torch.argmax(probs, dim=1)
    word = find_word_from_index(predicted_class.item(), "labels_to_ids.txt")
    return(word)


# print(predict_intention("what is the desease called Paralysis"))

