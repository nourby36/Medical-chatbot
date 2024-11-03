# Importer les données depuis le fichier data.py
from data import data_list
from sklearn.model_selection import train_test_split


# Afficher le nombre total de données
print("Nombre total de données :", len(data_list))

# Afficher un exemple de données
print("Exemple de données :", data_list[0])
questions_en = [item[0] for item in data_list]
questions_zh = [item[1] for item in data_list]
intentions = [item[2] for item in data_list]

# Afficher le nombre total de questions et d'intentions uniques
unique_questions_en = set(questions_en)
unique_questions_zh = set(questions_zh)
unique_intentions = set(intentions)


# Échantillonnage stratifié de 10% des données
train_questions_en, test_questions_en, train_questions_zh, test_questions_zh, train_intentions, test_intentions = train_test_split(
    questions_en, questions_zh, intentions,  train_size=0.1, stratify=intentions)


print(len(train_questions_en))

data_ner_annotation = []

# Pour chaque question en anglais dans l'ensemble d'entraînement
for question_en in train_questions_en:
    # Ajouter la question avec une entité nommée vide à la liste data_ner_annotation
    data_ner_annotation.append((question_en, {"entities": []}))

# Enregistrez les données dans un fichier data_ner.py
with open("data_ner_annotation.py", "w") as file:
    file.write("data_ner_annotation = [\n")
    for question, entities in data_ner_annotation:
        file.write(f'    ("{question}", {entities}),\n')
    file.write("]\n")