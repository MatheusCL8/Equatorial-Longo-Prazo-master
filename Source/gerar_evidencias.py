from Utilities.utilities import discretize_data_quantile
import pandas as pd
import topologia
import json
from dataframe import base

def discretizacao_BDCompleta(n_bins,type_discretize, mes, base, alvo, ano_projecao):
    alvo = alvo
    dicano = dict()
    base=pd.DataFrame(base).drop(['DATA',alvo], axis=1)
    topologia.node_list.remove(alvo)
    Data,faixas = discretize_data_quantile(base,n_bins,type_discretize)
    
    #--------------------------------------
    #virá como parametro alvo e anos de projecao (lembrando que deverar 
    #                                        ter os anos de validacao)

    anos_projecao = str(ano_projecao)
    
    dicano[alvo] = anos_projecao
    #------------------------------------------------
    k=0
    for ano in range(0,len(Data),12):
        dicio=dict()
        m=0
        for mes in range(ano,(ano+12)):
            dict_local=dict()
            for i in range(len(topologia.node_list)):
                dict_local[topologia.node_list[i]] = int(Data[topologia.node_list[i]][mes])
            dicio['MES_'+str(m)]=dict_local
            m=m+1
        dicano['ANO_'+str(k)]=dicio
        k = k+1
    
    return dicano

'''n_bins=2
type_discretize='kmeans'

meses=['JANEIRO','FEVEREIRO','MARCO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']

dic=discretizacao_BDCompleta(n_bins, type_discretize, meses, base,'CFCT',10)'''
