import json

#json_doc='../Data/JSON_files/EVIDENCIAS.json'

#data=base.iloc[0:len(base)-24]

def separa_arquivo_json(json_doc, alvo, nome):
    ##### ARQUIVO JSON PARA VALIDAÇÃO #####
    
    with open(json_doc, 'r') as js_validacao:
        teste_valida = json.load(js_validacao)
    
    for key in range(2,len(teste_valida.keys())-1):
        teste_valida.pop('ANO_'+str(key))
    
    teste_valida[alvo]=len(teste_valida.keys())-1
    
    validacao='../Data/JSON_files/VALIDACAO_' + str(nome) + '.json'
    
    with open(validacao, 'w') as json_v:
            json.dump(teste_valida, json_v, indent=4)
    
    
    ##### ARQUIVO JSON COM 10 ANOS #####
    
    with open(json_doc, 'r') as js_file:
        inferencia = json.load(js_file)
    del inferencia['ANO_0']
    del inferencia['ANO_1']
    
    
    inferencia[alvo]=len(inferencia.keys())-1
    
    novo=0
    antigo=2
    for k in range(1,len(inferencia.keys())):
        inferencia['ANO_'+str(novo)]=inferencia.pop('ANO_'+str(antigo), None)
        novo+=1
        antigo+=1
        
    producao='../Data/JSON_files/PRODUCAO_' + str(nome) + '.json'
    
    with open(producao, 'w') as json_file:
            json.dump(inferencia, json_file, indent=4)
    
    
    return validacao, producao


#def return_json_file(json_doc_valida,json_doc_produ):
'''json_doc_valida='../Data/JSON_files/SAIDA_RESULT_VALIDAÇÃO.json'
json_doc_produ='../Data/JSON_files/SAIDA_user.json'
with open(json_doc_valida, 'r') as js_validacao:
    json_valida = json.load(js_validacao)
        
with open(json_doc_produ, 'r') as js_producao:
    json_produ = json.load(js_producao)'''

def cria_json_final(json_valida,json_produ,alvo):
    meses=['JANEIRO','FEVEREIRO','MARCO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']
    final_dict=dict()
    cont=0
    for valida,produ in zip(json_valida.keys(),json_produ.keys()):
        month_dict=dict()
        a=json_valida[valida][alvo]
        b=json_produ[produ][alvo]
        total=a+b
        month_dict[alvo]=total
        final_dict[meses[cont]]=dict(month_dict)
        cont+=1
    return final_dict




