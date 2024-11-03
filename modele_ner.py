import spacy
from spacy.training import Example
from spacy.training.iob_utils import offsets_to_biluo_tags
from data_ner_annotation import data_ner_annotation

# Charger le modèle vide SpaCy
nlp = spacy.load("en_core_web_sm")
# Ajouter le composant NER au pipeline SpaCy
ner = nlp.get_pipe("ner")
ner.add_label("nom_maladie")
# Vérifier et corriger les annotations
corrected_examples = []
for text, annotation in data_ner_annotation:
    entities = annotation.get('entities', [])
    corrected_examples.append(Example.from_dict(nlp.make_doc(text), annotation))

# Entraîner le modèle avec les exemples corrigés
optimizer = nlp.begin_training()
for i in range(10):  # Nombre d'itérations d'entraînement
    for example in corrected_examples:
        nlp.update([example], sgd=optimizer)

# Sauvegarder le modèle entraîné
output_dir = "C:\\Users\\MSI\\Desktop\\IDS4\\sem2\\NLP\\PROJET\\modeles\\modele_ner"

nlp.to_disk(output_dir)
