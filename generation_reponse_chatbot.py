from generation_reponse import generer_reponse
from similarite_maladie import find_similar_diseases
from tester_modele_classification import predict_intention
from tester_modele_classification_generales import predict_intention_generalisee
import json
import random
from tester_modele_ner import detecter_entites_nommées
from traduire import traduire_en_ch, traduire_zh_en
from similarite_maladie import names


def charger_intents(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['intents']

def obtenir_reponse(intent_list, tag):
    for intent in intent_list:
        if intent['tag'] == tag:
            responses = intent['responses']
            return random.choice(responses)
    return "Désolé, je n'ai pas de réponse pour ce tag."

def reponse_aleatoire(file_path, tag):
    intents = charger_intents(file_path)
    return obtenir_reponse(intents, tag)


def extract_second_part(phrase):
    parts = phrase.split(": ", 1)  
    if len(parts) == 2: 
        return parts[1]  
    else:
        return None  

def gerer_traduction(text):
    text =extract_second_part(text)
    text =traduire_zh_en(text)
    return(text)



def generation_reponse(text):
    text1 = text
    print(text)
    text = traduire_zh_en(text)
    classe_generale =predict_intention_generalisee(text)
    print(text)
    print(classe_generale)
    if classe_generale=="traduction" :
        reponse = gerer_traduction(text1)
        print(reponse)
    elif classe_generale=="medical":
        classe_medicale =predict_intention(text)
        entite_detectee = detecter_entites_nommées(text)
        print(entite_detectee)
        print(entite_detectee[0][0])

        nom_maladie = traduire_en_ch(entite_detectee[0][0])
        print(nom_maladie)
        similar_disease = find_similar_diseases(nom_maladie,names)
        disease = similar_disease[0][0] 
        reponse = generer_reponse(classe_medicale,disease)  
        print(disease,"   ff  ", classe_medicale)
        print(reponse)
    else:
        reponse = reponse_aleatoire("intentions_generales.json", classe_generale)
        reponse= traduire_en_ch
        (reponse)
        print(reponse)
    
    return(reponse)


# # generation_reponse("您好") ##hello
# generation_reponse("您能将这句中文翻译成英文吗 : 治疗糖尿病的最佳方法是什么？") ##Can you translate this Chinese into English: What is the best way to treat diabetes?
# generation_reponse("您有关于肾病的信息吗？") ##do you have information about kidney disease?
