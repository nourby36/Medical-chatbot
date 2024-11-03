# Chatbot Médical Bilingue (Anglais-Chinois)

## Description
Ce projet propose un chatbot médical capable de traiter les questions en chinois, d'extraire des entités médicales et de fournir des réponses pertinentes basées sur une base de connaissances. Il utilise des modèles de classification et de reconnaissance d'entités nommées (NER).

## Table des matières
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure des fichiers](#structure-des-fichiers)
- [Contribution](#contribution)
- [Licence](#licence)

## Fonctionnalités
1. **Traduction** : Script `traduire.py` permettant la traduction entre l'anglais et le chinois.
2. **Extraction des données** : Script `charger_data.py` permet l'extraction des questions et intentions à partir des fichiers XML et enregistrement dans `data.py`sous la forme (question_anglais,question_chinois,intention).
3. **Équilibrage des données** : Équilibrage des intentions dans `data_balanced.py` à l'aide de `imbalanced_data.py`.
4. **Modèle de classification des intentions** : Script modele_classification.py entraîne un modèle (`modele_classification1`) pour classifier les intentions médicales.
5. **Test du modèle de classification** : Vérification des performances du modèle via `tester_modele_classification.py`.
6. **Préparation des données pour le modèle NER** : Script selection_data_ner.py permet extraction des questions en anglais pour l'entraînement du modèle NER et enregistrement dans `data_ner_annotation.py`
7. exemple: ("What special dietary instructions should I follow with Fluticasone and Vilanterol Oral Inhalation ?", {'entities': [(55,66,"nom_maladie"),(71,97,"nom_maladie")]})
8. **Annotation manuelle des entités** : Annotation avec SpaCy pour identifier les maladies.
9. **Modèle NER** : Script modele_ner.py entraîne et sauvegarde le modèle dans `modele_ner`.
10. **Test du modèle NER** : Test des performances avec `tester_modele_ner.py`.
11. **Extraction des maladies similaires** : Utilisation de `similarite_maladie.py` pour extraire les maladies à partir de la base des conaissances et calculer la similarité cosinus entre la maladie en entrée et les maladies extraites et choisir la plus probable (si aucune n'a plus de 50% de coresspondance il ne retourne pad d'information) .
12. **Génération de réponse** : Script `generation_reponse.py` pour générer des réponses basées sur les intentions et maladies (selon l'intention et la maladie détéctés) .
13. **Modèle pour intentions générales** : Entraînement d'un modèle avec `modele_classification_generales.py` pour traiter des intentions telles que salutations, remerciements, medical...
14. **Génération de réponses finales** : `generation_reponse_chatbot.py` pour extraire l'intention de l'utilisateur et générer des réponses appropriées.

## Installation
1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/utilisateur/projet-chatbot-medical.git
   cd projet-chatbot-medical
2.Script Bash pour télécharger le fichier depuis Google Drive (contenant les modeles deja entrainé)
https://drive.google.com/file/d/15J6XgUH4IcLx990RCOSQxrxuRHMVo-qN/view?usp=sharing

