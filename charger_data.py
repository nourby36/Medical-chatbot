from googletrans import Translator
import os
import xml.etree.ElementTree as ET
import time
from traduire import traduire_en_ch
import re

def est_chinois(phrase):
    # Utilisation d'une expression régulière pour filtrer les caractères chinois
     return bool(re.match('^[\u4e00-\u9fa50-9\s\W]+$', phrase))

types_questions_a_extraire = {'treatment', 'symptoms', 'susceptibility', 'usage', 'prevention', 'information', 'causes', 'dietary', 'precautions', 'other information'}


dossier_racine = 'data_test'

data = []

translator = Translator()

for sous_dossier in os.listdir(dossier_racine):
    chemin_sous_dossier = os.path.join(dossier_racine, sous_dossier)
    if os.path.isdir(chemin_sous_dossier):
        for fichier in os.listdir(chemin_sous_dossier):
            chemin_fichier = os.path.join(chemin_sous_dossier, fichier)
            print(chemin_fichier)
            if fichier.endswith('.xml'):
                tree = ET.parse(chemin_fichier)
                root = tree.getroot()

                for qa_pair in root.findall('.//QAPair'):
                    question_element = qa_pair.find('Question')
                    if question_element is not None:
                        qtype_attribut = question_element.get('qtype')

                        if qtype_attribut in types_questions_a_extraire:
                            question_text = question_element.text.strip()
                            translation = traduire_en_ch(question_text)

                            if est_chinois(translation):
                                print(question_text)
                                print(translation)
                                print(qtype_attribut)
                                data.append((question_text, translation, qtype_attribut))



with open('data.py', 'a', encoding='utf-8') as file:
    # Écrire chaque nouvelle question dans le fichier
    for question_text, question, qtype in data:
        file.write(f"    ('{question_text}', '{question}', '{qtype}'),\n")