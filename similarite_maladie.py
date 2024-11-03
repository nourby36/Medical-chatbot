import json
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba  # Chinese text segmentation library
from sklearn.metrics.pairwise import cosine_similarity

from traduire import traduire_en_ch, traduire_zh_en


# Assuming you have the knowledge base as a JSON file
with open('medical.json', encoding='utf-8') as f:
    # Read the contents of the file
    data = f.read()


# Parse the JSON data (check for errors)
try:
    json_data = json.loads(data)
except json.JSONDecodeError as e:
    print("Error parsing JSON:", e)
    exit(1)
# Parse the JSON data
json_data = json.loads(data)
names = [obj['name'] for obj in json_data]

# Extract names from each JSON object and store them in a list

# print(names)
def preprocess_disease_name(name):
    # Tokenization using jieba library for Chinese text
    tokens = jieba.cut(name)
    # Filter out empty tokens and join the remaining tokens
    processed_name = " ".join(token for token in tokens if token.strip())
    return processed_name

def calculate_cosine_similarity(name1, name2):
    # Preprocess both disease names
    name1 = preprocess_disease_name(name1)
    name2 = preprocess_disease_name(name2)

    
    if not name1 or not name2:
          return 0.0  # Return 0.0 for empty vocabulary

    # Convert to TF-IDF vectors
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([name1, name2])

    # Calculate cosine similarity
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    return similarity


def find_similar_diseases(user_input, disease_list, threshold=0.5):

  print(len(disease_list))
  # similar_diseases = []
  # for disease in disease_list:
  #   similarity = calculate_cosine_similarity(user_input, disease)
  #   if similarity >= threshold:
  #     similar_diseases.append(disease)
  # user_input = preprocess_disease_name(user_input)
  print(user_input)
  nom_ang = traduire_zh_en(user_input)
  print("desease")
  nom_ang = nom_ang[:-1]
  nom_maladie  = nom_ang + " desease"
  print(nom_maladie)
  user_input =traduire_en_ch(nom_maladie)
  print(user_input)
  similar_diseases = []
  for disease in disease_list:
        similarity = calculate_cosine_similarity(user_input, disease)
        similar_diseases.append((disease, similarity))

  similar_diseases.sort(key=lambda x: x[1], reverse=True)

  return similar_diseases
# il faut verifier apres la longueur de la liste , si le premier element (son score inferieri a 0.5 alors le chatbot va repondre par: si vous voulez savoir sur d'autres maladies comme ....)

def lire_mots_de_fichier(chemin_fichier):
    mots = []  # Initialiser une liste vide pour stocker les mots
    
    # Ouvrir le fichier en mode lecture avec l'encodage 'utf-8'
    with open(chemin_fichier, 'r', encoding='utf-8') as file:
        # Lire chaque ligne du fichier
        for ligne in file:
            # Nettoyer la ligne en supprimant les espaces vides et les caractères de nouvelle ligne
            mot_nettoye = ligne.strip()
            # Ajouter le mot à la liste des mots
            mots.append(mot_nettoye)
    
    return mots
# disease_list = lire_mots_de_fichier("dict\disease.txt")


# Exemple d'utilisation
# user_input = "网膜囊肿" ##paralysis

# similar_diseases = find_similar_diseases(user_input)

# print("Maladies similaires : ", similar_diseases[:3])















