import pandas as pd
import topologia
from datetime import datetime


data=['DATA']
#path = '../Data/raw/Nova BD_Dados_OUT_NOV_DEZ_COM_CNR.xlsx'
#sheet1="Dados Brutos"
#sheet2="Legenda"
base=""
legendas=""

#brutos = pd.read_excel(path,sheet_name = sheet1)

#legenda = pd.read_excel(path,sheet_name = sheet2)
#df_legenda=legenda.iloc[0:len(legenda),0:2]

# CSV DADOS BRUTOS SERÁ ATUALIZADO EXTERNAMENTE

#brutos.to_csv('../Data/raw/'+sheet1+'.csv',index=False)
#df_legenda.to_csv('../Data/raw/'+sheet2+'.csv',index=False)

def setupBase(sheet1, sheet2, concessionaria):
    global data
    global base
    global legenda
    global legendas
    dados_brutos=pd.read_csv('../Data/raw/'+sheet1+'.csv')
    
    topologia.setup(concessionaria)
    names=data+topologia.node_list
    base=dados_brutos[names]
    
    datas=base['DATA']
    datas=pd.DatetimeIndex(datas)
    ano_atual=datetime.now().year

    drop=[]

    for data in range(len(base['DATA'])):
        if datas[data].year==ano_atual:
            drop.append(data)
               
    base=base.drop(drop,axis=0)
    
    legendas=pd.read_csv('../Data/raw/'+sheet2+'.csv')    


'''
#data=['DATA']
path = '../Data/raw/Nova BD_Dados.xlsx'
sheet1="Dados Brutos"
sheet2="Legenda"


brutos = pd.read_excel(path,sheet_name = sheet1)

legenda = pd.read_excel(path,sheet_name = sheet2)
df_legenda=legenda.iloc[0:len(legenda),0:2]

brutos.to_csv('../Data/raw/'+sheet1+'.csv',index=False)
df_legenda.to_csv('../Data/raw/'+sheet2+'.csv',index=False)



dados_brutos=pd.read_csv('../Data/raw/'+sheet1+'.csv')
#names=data+node_list
#base=dados_brutos[names]
base=dados_brutos[node_list]
legendas=pd.read_csv('../Data/raw/'+sheet2+'.csv')





'''
