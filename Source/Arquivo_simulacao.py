# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 14:49:35 2020

@author: josiv
"""
#Arquivo teste
from Utilities.utilities import  discretize_data_quantile
from dataframe import dados_brutos, base
import pandas as pd
import topologia
import json

n_bins=3
type_discretize='kmeans'
# kmeans      |       quantile        |       uniform

def base_Mes(mes,Data): 
    #Data=pd.DataFrame(Data) 
    mat = []
    for i in range(mes,len(Data),12):
        mat.append(i)
    Data_t = Data.iloc[mat]
    return Data_t

meses=['JANEIRO','FEVEREIRO','MARCO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']

dicano = dict()

base=pd.DataFrame(base).drop(['CFCT'],axis=1)
topologia.setup('PA')
topologia.node_list.remove('CFCT')
for m in range(len(meses)): 
    mes=m
    bases = base_Mes(mes,base)
    bases = bases.reset_index(drop=True)
    
    discretized_data,faixas = discretize_data_quantile(bases, n_bins, type_discretize)
        
    for ano in range(len(discretized_data)):
        dict_local=dict()
        dicio=dict()
        aux=[]
        for i in range(len(topologia.node_list)):
            dict_local[topologia.node_list[i]]=int(discretized_data[topologia.node_list[i]][ano])
         
        if(meses[m] == 'JANEIRO'):
            dicio['MES_'+str(m)]=dict_local
            dicano['ANO_'+str(ano)] = dicio
        else:
            dicano['ANO_'+str(ano)]['MES_'+str(m)] = dict_local
     
with open('../Data/JSON_files/EVIDENCIA_AUTOMATICA.json', 'w') as json_file:
    json.dump(dicano, json_file, indent=4)
