import pandas as pd
import json
from gerar_evidencias import discretizacao_BDCompleta
#from dataframe import base
import dataframe
import sys
import argparse
import datetime
import os.path

# MANDAR A BASE, O N_BINS, A VARIAVEL ALVO, QUATIDADE DE ANOS, TIPO DE DISCRETIZAÇÃO

def get_evd_tendencias(base, n_bins,type_discretize,variavel_alvo,quant_ano,concessionaria, modelo):
        
    meses=['JANEIRO','FEVEREIRO','MARCO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']
    
    dicio=discretizacao_BDCompleta(n_bins, type_discretize, meses, base,variavel_alvo,quant_ano+2)
    intervalo=len(dicio)-(quant_ano+2)
    list_dic=list(dicio.keys())
    list_dic=list_dic[1:intervalo]
    
    for p in list_dic:
        dicio.pop(p)
    
    novo=0
    antigo=intervalo-1
    for k in range(1,len(dicio.keys())):
        dicio['ANO_'+str(novo)]=dicio.pop('ANO_'+str(antigo))
        novo+=1
        antigo+=1
    new_evi=dict(dicio)
    with open('../Data/JSON_files/EVIDENCIAS_TENDENCIAS_'+str(modelo)+'.json', 'w') as json_file:
        json.dump(new_evi, json_file, indent=4)

def xlsx_to_csv(readFrom, saveTo, concessionaria):
    print("Adequando planilha")
    #df = pd.concat(pd.read_excel(readFrom, sheet_name=None), ignore_index=True)
    #df.to_csv(saveTo+'.csv',index=False, encoding="utf8")
    
    sheets = ['Numero Consumidores BASE', 'variáveis_explicativas BASE', 'Número de Consumidores Básico', 'variáveis_explicativas_básico']
    for sheet in sheets:
        file_name = saveTo+ "_" + str(sheet) + '.csv'
        try:
            dados = pd.read_excel(readFrom, sheet_name=sheet)
            dados.to_csv(file_name,index=False, encoding="utf8")
            
        except:
            print("Não foi encontrada a sheet " + str(sheet))
            
        if os.path.isfile(file_name):
            today = datetime.datetime.now()
            nao_consolidados = datetime.timedelta(days=90)
            ano_0 = (today - nao_consolidados).year - 2
            erase_until_key(file_name, 0, ano_0, 'Consolidado')
            saveToDataset = os.path.join(os.path.dirname(saveTo), 'Dataset Tendencias ' + str(concessionaria) + '.csv')
            drop_columns(file_name, sheet, concessionaria, saveToDataset)

def erase_until_key(file_name, field_position, key, endKey):
    print('Ajustando csv ' + os.path.basename(file_name))
    print('Key: ', key)
    print('Key position: ', field_position)

    try: 
        with open(file_name, 'r+', encoding="utf8") as fr: 
            lines = fr.readlines()[1:] #Salta a primeira linha que apenas identifica a Tendências
        with open(file_name, 'w+', encoding="utf8") as fw:
            delete = True
            head = True
            for line in lines:
                if head:
                    fw.write(line)  
                    head = False
                    continue
                field_to_look = line.split(',')[field_position]
                line_aux = line
                if str(field_to_look) == str(key):
                    delete = False
                elif str(field_to_look).startswith(str(endKey)):
                    break
                if not delete and field_to_look: 
                    fw.write(line)  
        fw.close()
    except Exception as ex:
        print(ex)
        
def drop_columns(file_name, sheet, concessionaria, saveTo):
    print('Removendo colunas de ', file_name)
    print('Salvando resultado em ', saveTo)
    columns_to_drop = { 
        'Numero Consumidores BASE': [0], 
        'variáveis_explicativas BASE': [0, 3, 4, 5], 
        'Número de Consumidores Básico': [0], 
        'variáveis_explicativas_básico': [0]
    }
    col_to_drop = columns_to_drop[sheet]
    print('col_to_drop = ', col_to_drop)
    
    dados = pd.read_csv(file_name)
    print('antes')
    print(dados.shape)
    dados.drop(dados.columns[col_to_drop], axis=1, inplace=True)
    print('depois')
    print(dados.shape)
    dados.to_csv(saveTo,index=False, encoding="utf8")
        

if __name__ == '__main__':

    #readFrom = 'D:\\EQTL_Pará_variáveis_explicativas_2020_10_23.xlsx'
    #saveTo = 'D:\\EQTL_PA_testeCSV'
    #concessionaria = 'PA'
    #xlsx_to_csv(readFrom, saveTo, concessionaria)
    #sys.exit(1)

    if len(sys.argv) > 1:
        ap = argparse.ArgumentParser()
        ap.add_argument("-n", "--nbins", required=False, help="Número de bins", type=int)
        ap.add_argument("-m", "--method", required=False, help="Método de discretização", type=str)
        ap.add_argument("-c", "--conc", required=False, help="Concessionária", type=str)
        ap.add_argument("-z", "--horizon", required=False, help="Horizonte de projeção em anos", type=int)
        ap.add_argument("-t", "--target", required=False, help="Variável Alvo", type=str)
        ap.add_argument("-d", "--datasetname", required=False, help="Nome do Dataset. Exemplo: EQTL_PA_Variaveis Explicativas.xlsx", type=str)
        ap.add_argument("-u", "--name", required=False, help="Nome do modelo", type=str)
        args = vars(ap.parse_args())

        n_bins = args['nbins']
        type_discretize=args['method']
        concessionaria = args['conc']
        quant_ano = args['horizon']
        variavel_alvo = args['target']
        dataset_name = args['datasetname']
        modelo = args['name']
    else:
        type_discretize='kmeans'
        n_bins=2
        quant_ano=10
        variavel_alvo='CFCT'
        concessionaria = 'MA'
        dataset_name = "Dataframe1"
        modelo = 'mod_MA_1'
    dataframe.setupBase(dataset_name, "Legenda-"+str(concessionaria), concessionaria)
    new_evidencia=get_evd_tendencias(dataframe.base, n_bins,type_discretize,variavel_alvo,quant_ano,concessionaria, modelo)