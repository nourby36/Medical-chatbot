import json

def get_informations_desease(intention, nom_maladie):
    with open('medical.json', encoding='utf-8') as f:
        data = f.read()
    json_data = json.loads(data)

    informations = {}
    
    for document in json_data:
        if document['name'] == nom_maladie:
            informations['name'] = document['name']
            informations['desc'] = document['desc']
            informations['category'] = document['category']  
            informations['prevent'] = document['prevent']
            informations['cause'] = document['cause']
            informations['symptom'] = document['symptom']
            informations['yibao_status'] = document['yibao_status']
            informations['get_prob'] = document['get_prob']
            informations['easy_get'] = document['easy_get']
            informations['get_way'] = document['get_way']
            informations['acompany'] = document['acompany']
            informations['cure_department'] = document['cure_department']
            informations['cure_way'] = document['cure_way']
            informations['cure_lasttime'] = document['cure_lasttime']
            informations['cured_prob'] = document['cured_prob']
            informations['cost_money'] = document['cost_money']
            informations['check'] = document['check']
            informations['recommand_drug'] = document['recommand_drug']
            informations['drug_detail'] = document['drug_detail']
            if 'recommand_eat' in document and 'do_eat' in document and 'not_eat'in document:
              informations['recommand_eat'] = document['recommand_eat']
              informations['do_eat'] = document['do_eat']
              informations['not_eat'] = document['not_eat']
            else:
              informations['recommand_eat'] = "No specific dietary recommendations available."
            break
    
    informations['intention_utilisateur'] = intention
    return informations



def generer_reponse(intention, nom_maladie):

    informations = get_informations_desease(intention, nom_maladie)

    if intention == 'information':
        reponse = informations["desc"]
    if intention == 'symptoms':
        reponse = informations["symptom"]
    if intention == 'susceptibility':
        reponse = informations["easy_get"]
    if intention == 'treatment':
        reponse = informations["cure_way"]
    if intention == 'prevention':
        reponse = informations["prevent"]
    if intention == 'causes':
        reponse = informations["cause"]
    if intention == 'dietary':
        if informations["recommand_eat"] == "No specific dietary recommendations available.":
            reponse=informations["recommand_eat"]
        else:
            reponse = "你可以吃"+ str(informations["do_eat"]) +"\n"+"建议食用" +str(informations["recommand_eat"])+ "\n"+"不能吃 " +str(informations["not_eat"])
    if intention == 'usage':
        reponse = 'dd'
    if intention == 'precautions':
        reponse = informations[""]
    if intention == 'other information':
        reponse = str(informations['get_way'])+"得这种病的概率是"+str(informations['get_prob'])+"\n"+"属于"+str(informations['cure_department'])+"\n"+"类别"+str(informations['category'])+"\n"+"可伴有"+str(informations['acompany'])+"\n"+"多久能治愈"+str(informations['cure_lasttime'])+"\n"+"治愈概率"+str(informations['cured_prob'])+"\n"+"需要检查"+str(informations['check'])+"\n"+"推荐药物"+str(informations['recommand_drug'])+"\n"+"药物详情"+str(informations['drug_detail'])+"\n"+"成本"+str(informations['cost_money'])
    return reponse 

# nom_maladie ="肺曲菌病"
# intention ="other information"
# print(generer_reponse(intention, nom_maladie))