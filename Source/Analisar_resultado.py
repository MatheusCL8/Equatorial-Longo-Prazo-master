# -*- coding: utf-8 -*-


import json
import pandas as pd

json_doc='../Data/JSON_files/SAIDA_Josivan.json'
meses=['JANEIRO','FEVEREIRO','MARCO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']

with open(json_doc, 'r') as js_file:
    inferencia = json.load(js_file)

data=pd.DataFrame({'ANO':[],'MES':[],'MIN':[],'MEDIO':[],'MAX':[]})

for i in range(len(meses)):
    sup=inferencia[meses[i]]['CFCT']
    temp=[]
    for j in range(len(sup)):
        valores=[]
        value=sup[j]
        MIN=value['MIN']
        MEDIO=value['MEDIO']
        MAX=value['MAX']
        ANO = value['ANO']
        
        data=data.append(pd.DataFrame({'ANO':[ANO],'MES':[' MES DE '+meses[i]],'MIN':[MIN],'MEDIO':[MEDIO],'MAX':[MAX]}))
        

        

print('Executado com sucesso')

data.to_excel('../Data/raw/resultado2.xlsx',index=False) 




'''

data=pd.DataFrame({'CLASSE':['MIN','MEDIO','MAX']})

for i in range(len(meses)):
    sup=inferencia[meses[i]]['CFCT']
    temp=[]
    for j in range(len(sup)):
        valores=[]
        value=sup[j]
        MIN=value['MIN']
        MEDIO=value['MEDIO']
        MAX=value['MAX']
        data['TEMPO '+str(j)+' MES DE '+meses[i]]=[MIN,MEDIO,MAX]
        

print(data)

data.to_excel('../Data/raw/result.xlsx',index=False) 
'''