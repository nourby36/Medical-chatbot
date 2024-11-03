from transformers import BertForSequenceClassification, BertTokenizer
import torch
import torch.nn.functional as F  
from traduire import traduire_en_ch


def predict_intention_generalisee(text):
    # Définir le chemin vers le répertoire contenant votre modèle enregistré
    model_dir = "C:\\Users\\MSI\\Desktop\\IDS4\\sem2\\NLP\\PROJET\\modele_classification2"

    # Charger le tokenizer
    tokenizer =BertTokenizer.from_pretrained('hfl/chinese-bert-wwm')

    # Charger le modèle
    model = BertForSequenceClassification.from_pretrained(model_dir)
    # Exemple de texte à classer
    # text = "Can you render this Chinese idea into English:what is Virus "
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
    word = find_word_from_index(predicted_class.item(), "generales_to_code1.txt")
    return(word)

def find_word_from_index(index, file_path):
    # Ouvrir le fichier et lire son contenu
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Parcourir chaque ligne du fichier pour trouver le mot correspondant à l'indice
    for line in lines:
        # Séparer la ligne en mot et indice
        word, idx = line.strip().split(":")
        idx = int(idx)
        # Vérifier si l'indice correspond à celui recherché
        if idx == index:
            return word

    # Si aucun mot correspondant n'est trouvé, retourner None
    return None


# print(predict_intention_generalisee("Can you render this Chinese idea into English:what is Virus "))