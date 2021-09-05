from Utilities.utilities import build_dbn
import topologia
import dataframe
import argparse
from pprint import pprint
import sys
from validacao import separa_arquivo_json, cria_json_final
import json
import pandas as pd
from datetime import datetime
import traceback

usuario='user'

def callScript(dataset_name, json_doc, n_bins, type_discretize, nome_saida, conc, alvo): 
    #print(json_doc)
    #print('rede_dinamica.n_bins = ' + str(n_bins))
    #print('rede_dinamica.type_discretize = ' + str(type_discretize))
    
    dataframe.setupBase(dataset_name, "Legenda-"+str(conc), conc)
    
    validacao,producao=separa_arquivo_json(json_doc, alvo, nome_saida)
        
    data=dataframe.base.iloc[0:len(dataframe.base)-24]
    datas=data['DATA']
    datas=pd.DatetimeIndex(datas)
    ano_valida=(datas[len(datas)-1].year)+1
    
    print("\n############################# VALIDAÇÃO #############################\n")
    ajuste = 1
    n_bins_valida = min(n_bins, 3) #no maximo 3 bins na validacao    
    valida=build_dbn(ano_valida,topologia.topology, topologia.top, topologia.nodes, data, n_bins_valida, type_discretize, validacao, 'RESULT_VALIDAÇÃO', ajuste)
    
    datas=dataframe.base['DATA']
    datas=pd.DatetimeIndex(datas)
    ano_atual=datetime.now().year
    ano_produto=(datas[len(datas)-1].year)+1
    if ano_produto!=ano_atual:
        ano_produto=ano_atual
    
    print("\n############################# PRODUTO #############################\n")
    ajuste = 1        
    produto=build_dbn(ano_produto,topologia.topology, topologia.top, topologia.nodes, dataframe.base, n_bins, type_discretize, producao, nome_saida, ajuste)
    
    dict_total=cria_json_final(valida,produto,alvo)
    nome_result='SAIDA_'+nome_saida
    path_result='../Data/JSON_files/SAIDA_'+nome_saida+'.json'
    with open(path_result, 'w') as json_file:
        json.dump(dict_total, json_file, indent=4)
    
    print("Resultado salvo em %s com o nome: %s"%(path_result,nome_result))
    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ap = argparse.ArgumentParser()
        ap.add_argument("-n", "--nbins", required=False, help="Número de bins", type=int)
        ap.add_argument("-m", "--method", required=False, help="Método de discretização", type=str)
        ap.add_argument("-u", "--user", required=False, help="Nome do usuário", type=str)
        ap.add_argument("-o", "--modelo", required=False, help="Nome do modelo", type=str)
        ap.add_argument("-d", "--datasetname", required=False, help="Nome do Dataset sem extensão .csv. Exemplo: Dados Brutos-PA-CFCT-semCNR", type=str)
        ap.add_argument("-c", "--conc", required=False, help="Concessionária", type=str)
        ap.add_argument("-t", "--target", required=False, help="Alvo", type=str)
        #ap.add_argument("-a", "--ajuste", required=False, help="Ajuste para seleção da próxima faixa, caso a probabilidade seja 50 por cento", type=int)
        args = vars(ap.parse_args())

        usuario = args['user']
        modelo = args['modelo']
        n_bins = args['nbins']
        type_discretize=args['method']
        json_doc='../Data/JSON_files/EVIDENCIAS_'+usuario+'_' + modelo+'.json'
        topologia.setup(args['conc'])
        conc = topologia.concessionaria
        dataset_name = args['datasetname']
        alvo = args['target']
        #ajuste = args['ajuste']
    else:
        usuario = 'user'
        modelo = 'mod-generico'
        n_bins=2
        type_discretize='kmeans'
        json_doc='../Data/JSON_files/EVIDENCIAS.json'
        topologia.setup('PA')
        conc=topologia.concessionaria
        dataset_name = "Dados Brutos-PA-CFCT-semCNR"
        alvo = "CFCT"
        #ajuste = 0
    nome_saida = usuario + '_' + modelo
    try:
        callScript(dataset_name, json_doc, n_bins, type_discretize, nome_saida, conc, alvo)
        print("Fim rede_dinamica " + str(modelo) + ' ' + str(conc))
    except:
        print('Erro rede_dinamica ' + str(modelo) + ' ' + str(conc))
        traceback.print_exc()