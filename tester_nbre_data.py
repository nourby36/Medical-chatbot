import os
import xml.etree.ElementTree as ET

# Chemin du dossier racine
dossier_racine = 'data_test'

# Liste des qtypes à compter
qtypes_a_compter = [
    "treatment",
    "symptoms",
    "susceptibility",
    "usage",
    "prevention",
    "information",
    "causes",
    "dietary",
    "precautions",
    "other information"
]

# Dictionnaire pour stocker le nombre d'occurrences de chaque qtype
occurrences_qtypes = {qtype: 0 for qtype in qtypes_a_compter}

# Parcourt tous les sous-dossiers dans le dossier racine
for sous_dossier in os.listdir(dossier_racine):
    chemin_sous_dossier = os.path.join(dossier_racine, sous_dossier)
    # Vérifie que c'est un dossier
    if os.path.isdir(chemin_sous_dossier):
        # Parcourt tous les fichiers dans ce sous-dossier
        for fichier in os.listdir(chemin_sous_dossier):
            chemin_fichier = os.path.join(chemin_sous_dossier, fichier)
            # Vérifie que c'est un fichier XML
            if fichier.endswith('.xml'):
                # Parse le fichier XML
                tree = ET.parse(chemin_fichier)
                root = tree.getroot()
                # Parcourt toutes les balises <QAPair>
                for qa_pair in root.findall('.//QAPair'):
                    question_element = qa_pair.find('Question')
                    if question_element is not None:
                        qtype_attribut = question_element.get('qtype')
                        # Vérifie si le qtype est dans la liste à compter
                        if qtype_attribut in occurrences_qtypes:
                            # Incrémente le compteur pour ce qtype
                            occurrences_qtypes[qtype_attribut] += 1

# Affiche le nombre d'occurrences de chaque qtype
for qtype, occurrences in occurrences_qtypes.items():
    print(f"{qtype}: {occurrences}")

total_questions = sum(occurrences_qtypes.values())
print(f"Total des questions pour tous les types spécifiés : {total_questions}")