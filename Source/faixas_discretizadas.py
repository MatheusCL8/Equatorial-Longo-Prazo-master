from Utilities.utilities import  build_doc_variavel_discretizacao
#from dataframe import base, legendas
import dataframe
import topologia
import argparse
import sys
import traceback

n_bins=3
type_discretize='kmeans'
usuario='user'

def callScript(dataset_name, n_bins, type_discretize, usuario, concessionaria):
    #print(n_bins)
    #print(type_discretize)
    dataframe.setupBase(dataset_name, "Legenda-"+str(concessionaria), concessionaria)
    matrix=[]
    topologia.setup(concessionaria)
    for i in range(len(topologia.node_list)):
        for j in range(len(dataframe.legendas)):
            if topologia.node_list[i] == dataframe.legendas['DATA'][j]:
                matrix.append(list(dataframe.legendas.iloc[j]))

    build_doc_variavel_discretizacao(dataframe.base,matrix,n_bins,type_discretize,usuario)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ap = argparse.ArgumentParser()
        ap.add_argument("-n", "--nbins", required=False, help="Número de bins", type=int)
        ap.add_argument("-m", "--method", required=False, help="Método de discretização", type=str)
        ap.add_argument("-u", "--user", required=False, help="Nome do usuario e modelo", type=str)
        ap.add_argument("-d", "--datasetname", required=False, help="Nome do Dataset sem extensão .csv. Exemplo: Dados Brutos-PA-CFCT-semCNR", type=str)
        ap.add_argument("-c", "--conc", required=False, help="Concessionária", type=str)
        args = vars(ap.parse_args())

        usuario = args['user']
        n_bins = args['nbins']
        type_discretize=args['method']
        concessionaria = args['conc']
        dataset_name = args['datasetname']
    else:
        usuario = 'user'
        n_bins=3
        type_discretize='kmeans'
        concessionaria = 'PA'
        dataset_name = "Dados Brutos-PA-CFCT-semCNR"
    try:
        callScript(dataset_name, n_bins, type_discretize, usuario, concessionaria)
        print('Fim faixas. concessionaria = ', concessionaria, ', dataset = ', dataset_name)
    except:
        print('Erro faixas. concessionaria = ', concessionaria, ', dataset = ', dataset_name)
        traceback.print_exc()
