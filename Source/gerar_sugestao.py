import pandas as pd
from fbprophet import Prophet
import json
import dataframe
import sys
import argparse
import topologia
from Utilities.utilities import discretize_data_quantile
import traceback


# MANDAR A BASE, O N_BINS, A VARIAVEL ALVO, QUATIDADE DE ANOS, TIPO DE DISCRETIZAÇÃO

def discretizacao_BDCompleta(n_bins,type_discretize, mes, base, alvo, ano_projecao):
    dicano = dict()
    base=pd.DataFrame(base).drop(['DATA'], axis=1)
    topologia.node_list=base.columns
    nodes=list(topologia.node_list)
    nodes.remove(alvo)
    Data,faixas = discretize_data_quantile(base,n_bins,type_discretize)

    #print("faixas = ", faixas)
    #print('Data = ', Data)

    #--------------------------------------
    #virá como parametro alvo e anos de projecao (lembrando que deverar
    #                                        ter os anos de validacao)

    dicano[alvo] = str(ano_projecao)
    #------------------------------------------------
    k=0
    for ano in range(0,len(Data),12):
        dicio=dict()
        m=0
        for mes in range(ano,(ano+12)):
            dict_local=dict()
            for i in range(len(nodes)):
                dict_local[nodes[i]] = int(Data[nodes[i]][mes])
            dicio['MES_'+str(m)]=dict_local
            m=m+1
        dicano['ANO_'+str(k)]=dicio
        k = k+1

    return dicano

def new_data(ano,data):
    meses=ano*12

    data['DATA'] = pd.DatetimeIndex(data['DATA'])
    nomes=list(data.columns)

    dfs=[]
    for column in range(1,len(nomes)):
        col=data[['DATA',data.columns[column]]]
        dfs.append(col)


    new_dfs=[]
    for data in dfs:
        cols=data.columns
        data=data.rename(columns={cols[0]: 'ds', cols[1]:'y'})
        new_dfs.append(data)

    #FAZ A PREVISÃO DE DATA A PARTIR DA PRIMEIRA VARIAVEL
    my_model=Prophet(interval_width=0.95)
    my_model.fit(new_dfs[0])
    future_dates0 = my_model.make_future_dataframe(periods=meses, freq='MS')
    forecast0 = my_model.predict(future_dates0)
    forecast0=forecast0[['ds']]
    forecast0=forecast0.rename(columns={'ds':'DATA'})
    dt=pd.DataFrame(forecast0['DATA'])


    for data in range(len(new_dfs)):
        my_model10 = Prophet(interval_width=0.95)
        col=my_model10.fit(new_dfs[data])
        future_dates = my_model10.make_future_dataframe(periods=meses, freq='MS')
        forecast = my_model10.predict(future_dates)
        forecast=forecast[['yhat']]
        forecast=forecast.rename(columns={'yhat':nomes[data+1]})
        dt[nomes[data+1]]=forecast

    return dt


def retorna_sugestao_evidencia(base, n_bins,type_discretize,variavel_alvo,quant_ano,concessionaria, modelo, FBprophet_cond='n'):

    if FBprophet_cond=='y':
        df=new_data(quant_ano, base)
        df=df[len(base):len(df)]
        base=pd.concat([base, df], axis=0)

    anosValidacao = 2
    meses=['JANEIRO','FEVEREIRO','MARCO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']

    dicio=discretizacao_BDCompleta(n_bins, type_discretize, meses, base,variavel_alvo,quant_ano+anosValidacao)
    intervalo=len(dicio)-(quant_ano+anosValidacao)
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

    if FBprophet_cond=='n':
        outPath = '../Data/JSON_files/EVIDENCIAS_TENDENCIA_'+str(modelo)+'.json'
    else:
        outPath = '../Data/JSON_files/EVIDENCIAS_SUGERIDAS_'+str(modelo)+'.json'
    print('Gravando saida em: ', outPath)
    with open(outPath, 'w') as json_file:
        json.dump(new_evi, json_file, indent=4)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ap = argparse.ArgumentParser()
        ap.add_argument("-n", "--nbins", required=False, help="Número de bins", type=int)
        ap.add_argument("-m", "--method", required=False, help="Método de discretização", type=str)
        ap.add_argument("-c", "--conc", required=False, help="Concessionária", type=str)
        ap.add_argument("-z", "--horizon", required=False, help="Horizonte de projeção em anos", type=int)
        ap.add_argument("-t", "--target", required=False, help="Variável Alvo", type=str)
        ap.add_argument("-d", "--datasetname", required=False, help="Nome do Dataset sem extensão .csv. Exemplo: Dados Brutos-PA-CFCT-semCNR ou Tendencias-PA-semCNR", type=str)
        ap.add_argument("-u", "--name", required=False, help="Nome do arquivo de saida", type=str)
        ap.add_argument("-p", "--prophet", required=False, help="Usar ou não o Prophet (pode ser 'y' ou 'n')", type=str)
        args = vars(ap.parse_args())

        n_bins = args['nbins']
        type_discretize=args['method']
        concessionaria = args['conc']
        quant_ano = args['horizon']
        variavel_alvo = args['target']
        dataset_name = args['datasetname']
        modelo = args['name']
        prophet = args['prophet']
    else:
        type_discretize='kmeans'
        n_bins=2
        quant_ano=10
        variavel_alvo='CFCT'
        concessionaria = 'PA'
        dataset_name = "Tendencias-PA-semCNR"
        modelo = 'm_PA_1'
        prophet = 'n'

    try:
        topologia.setup(concessionaria)

        if prophet == 'n':
            print('Usando ../Data/raw/'+dataset_name+'.xlsx')
            data=pd.read_excel('../Data/raw/'+dataset_name+'.xlsx')
        else:
            print('Usando ' + dataset_name)
            dataframe.setupBase(dataset_name, "Legenda-"+str(concessionaria), concessionaria)
            data = dataframe.base

        new_evidencia=retorna_sugestao_evidencia(data, n_bins,type_discretize,variavel_alvo,quant_ano,concessionaria, modelo, prophet)
        print('Fim sugestoes. prophet = ', prophet, ', modelo = ', modelo)
    except:
        print('Erro sugestoes. prophet = ', prophet, ', modelo = ', modelo)
        traceback.print_exc()
