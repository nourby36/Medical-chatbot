import spacy



def detecter_entites_nommées(texte, chemin_modele="C:\\Users\\MSI\\Desktop\\IDS4\\sem2\\NLP\\PROJET\\modele_ner"
):
    # Charger le modèle entraîné
    nlp = spacy.load(chemin_modele)

    # Appliquer le modèle au texte
    doc = nlp(texte)

    # Stocker les entités nommées détectées dans une liste de tuples (entité, étiquette)
    entites = [(ent.text, ent.label_) for ent in doc.ents]

    return entites

# Exemple d'utilisation de la fonction
texte = "What is (are) Paralysis ?"
chemin_modele = "C:\\Users\\MSI\\Desktop\\IDS4\\sem2\\NLP\\PROJET\\modele_ner"

# entites_detectees = detecter_entites_nommées(texte, chemin_modele)
# print(entites_detectees)