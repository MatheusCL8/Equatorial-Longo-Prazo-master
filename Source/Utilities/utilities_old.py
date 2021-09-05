import pandas as pd
from itertools import chain
from pgmpy.models import BayesianModel
from pgmpy.models import DynamicBayesianNetwork as DBN
from pgmpy.inference import DBNInference
from pgmpy.estimators import ParameterEstimator
from pgmpy.factors.discrete import TabularCPD
from sklearn.preprocessing import KBinsDiscretizer
import numpy as np
import json
# ------------------------------------------------------------------------------------------------------
# File Handling


def load_model(model_name, path='../../Models/'):
    '''
    Inputs:
        model_name: model name (string).
        path: path to model (optional).
    1 - Load model from path.
    2 - Check if model is valid.
    Returns: PGMPY model object.
    '''

    import pickle
    pickle_in = open(f"{path}{model_name}.pickle", "rb")
    model = pickle.load(pickle_in)

    if model.check_model():
        print("Model Loaded and Checked!")

    return model


def build_porcentagem(data):
    date=data['DATA']
    date=date.iloc[12:len(date)]
    date = date.reset_index(drop=True)
    data=data.drop(['DATA'],axis=1)
    dados=[]
    for linha in range(0,len(data)-12):
        valores=[]
        for coluna in data:
            #x = dataframe.loc[linha][coluna]
            x = ((data.iloc[linha + 12][coluna] * 100) / data.iloc[linha][coluna])-100
            valores.append('%.2f'%float(x))
        dados.append(valores)
    dataset=pd.DataFrame(dados,columns=data.columns)
    dataset=pd.concat([date,dataset],axis=1)
    return dataset

#--- Cria as bases por mês no formato VARIAVEL_0, VARIAVEL_1
def criar_base_mes(mes,Data):
    month=['January','February','March','April','May','June','July','August','September','October','November','December']
    #0 - Janeiro | 1 - Fevereiro ... | 11 - Dezembro
    Data=pd.DataFrame(Data)
    date=Data['DATA']
    date=pd.DatetimeIndex(date)
        
    mat = []
    for i in range(len(Data)):
        if date[i].month_name()==month[mes]:
            mat.append(i)
        elif date[i].month_name()!=month[mes]:
            continue
    Data_t = Data.iloc[mat]
    Data_t = Data_t.reset_index(drop=True)
    Data_t=Data_t.drop(['DATA'],axis=1)
    
    if len(Data_t)%2!=0:
        Data_t = Data_t.iloc[1:len(mat)]
        Data_t = Data_t.reset_index(drop=True)
        t0 = []
        for i in range(0,len(Data_t),2):
            t0.append(i)
        matrix_t0 = Data_t.iloc[t0]
        
        t1 = []
        for i in range(1,len(Data_t),2):
            t1.append(i)
    
        
        matrix_t1 = Data_t.iloc[t1]
    
        matrix_t0=matrix_t0.rename(columns=lambda x: x+'_0')
        matrix_t1=matrix_t1.rename(columns=lambda x: x+'_1')
    
        matrix_t0=pd.concat([matrix_t0.reset_index(drop=True), matrix_t1.reset_index(drop=True)], axis=1)
        
    else:
        t0 = []
        for i in range(0,len(mat),2):
            t0.append(i)
        matrix_t0 = Data_t.iloc[t0]
        
        t1 = []
        for i in range(1,len(mat),2):
            t1.append(i)
    
        
        matrix_t1 = Data_t.iloc[t1]
    
        matrix_t0=matrix_t0.rename(columns=lambda x: x+'_0')
        matrix_t1=matrix_t1.rename(columns=lambda x: x+'_1')
    
        matrix_t0=pd.concat([matrix_t0.reset_index(drop=True), matrix_t1.reset_index(drop=True)], axis=1)
    return matrix_t0

#--- Cria um doc JSON com o nome completo das variaveis e suas faixas de discretização
def build_doc_variavel_discretizacao(dados_brutos,legendas,bins=3,type_disc='kmeans',usuario='user'):
    data = dados_brutos.drop(['DATA'],axis=1)
    df=pd.DataFrame(data)
    lista=list(df.columns)
    meses=['JANEIRO','FEVEREIRO','MARCO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']
    dict_meses=dict()
    for m in range(len(meses)):
        mat = []
        for i in range(m,len(df),12):
            mat.append(i)
        Data_t = df.iloc[mat]
        Data_t = Data_t.reset_index(drop=True)
        est = KBinsDiscretizer(n_bins=bins,encode='ordinal', strategy=type_disc.lower())
        r = est.fit(Data_t)
        x=r.bin_edges_
        faixas=dict()
        for j,i in zip(lista,x):
            faixas[j]=list(i)
        df_legenda = legendas
        dict_legenda=dict()
        for i in range(len(df_legenda)):
            legenda=list(df_legenda[i])
            dict_legenda[legenda[1]]=legenda[0]

        var_discretize=dict()
        for var,value in zip(lista,faixas.values()):
            if var in dict_legenda:
                var_discretize[dict_legenda[var]]=value
        dict_meses[meses[m]]=var_discretize

    with open('../Data/JSON_files/FAIXAS_'+usuario+'.json', 'w') as json_fl:
        json.dump(dict_meses, json_fl, indent=4)

#--- Disrcetiza as bases para a Rede Dinâmica

def discretize_data_quantile(dataframe,bins=3,type_discr='kmeans'):
    # kmeans      |       quantile        |       uniform
    #n_bins=3 (Default)
    # dataframe: Base que foi passada pela função "criar_base_mes"
    lista=list(dataframe.columns)
    est = KBinsDiscretizer(n_bins=bins,encode='ordinal', strategy=type_discr.lower())
    r = est.fit(dataframe)
    disc = est.transform(dataframe)
    discretized_dataframe=pd.DataFrame(disc,columns=lista)
    #####################################
    x=r.bin_edges_
    faixas=dict()
    for j,i in zip(lista,x):
        faixas[j]=i            
    #####################################

    return discretized_dataframe, faixas


#--- Cria as arestas no formato pedido pela Rede Bayesiana Dinâmica

def build_edges(ed):
    edges=list(ed)
    edges_0=[]
    for i in range(len(edges)):
        x=(tuple(edges[i][0].split('_')),tuple(edges[i][1].split('_')))
        edges_0.append(x)
    edge=[]
    for j in range(len(edges_0)):
        y=((edges_0[j][0][0],int(edges_0[j][0][1])),(edges_0[j][1][0],int(edges_0[j][1][1])))
        edge.append(y)
    return edge

#--- Constroi as Tabelas de Probabilidades Condicionais (CPDs) para a Rede Dinâmica

def build_dbn_cpds(edges,dbn_model,nodes_dbn, discretized_data):
    nodes=list(nodes_dbn)
    model = BayesianModel(edges)
    estimator = BayesianEstimator_V2(model, discretized_data)
    cpds=[]    
    for no in nodes:
        node=(no[0]+'_'+str(no[1]))
        valor,card,cardi=estimator.estimate_cpd(node, prior_type="BDeu")
        if len(dbn_model.get_parents(no))==0:
            cpd=TabularCPD(no,
                           card,
                           valor)
            cpds.append(cpd)
        else:
            cpd=TabularCPD(no,
                           card,
                           valor,
                           evidence=dbn_model.get_parents(no),
                           evidence_card=cardi[1:]
            )
            cpds.append(cpd)
    return cpds

#--- Classe que cria os valores de probabilidades para estimação bayesiana (Alterada para se adequar à Rede Dinâmica)

class BayesianEstimator_V2(ParameterEstimator):
    def __init__(self, model, data, **kwargs):
        
        self.model=model
        self.data=data

        super(BayesianEstimator_V2, self).__init__(model, data, **kwargs)

    def estimate_cpd(
        self, node, prior_type="BDeu", pseudo_counts=[], equivalent_sample_size=5
    ):

        node_cardinality = len(self.state_names[node])
        parents = sorted(self.model.get_parents(node))
        parents_cardinalities = [len(self.state_names[parent]) for parent in parents]
        cpd_shape = (node_cardinality, np.prod(parents_cardinalities, dtype=int))

        if prior_type == "K2":
            pseudo_counts = np.ones(cpd_shape, dtype=int)
        elif prior_type == "BDeu":
            alpha = float(equivalent_sample_size) / (
                node_cardinality * np.prod(parents_cardinalities)
            )
            pseudo_counts = np.ones(cpd_shape, dtype=float) * alpha
        elif prior_type == "dirichlet":
            pseudo_counts = np.array(pseudo_counts)
            if pseudo_counts.shape != cpd_shape:
                raise ValueError(
                    "The shape of pseudo_counts for the node: {node} must be of shape: {shape}".format(
                        node=node, shape=str(cpd_shape)
                    )
                )
        else:
            raise ValueError("'prior_type' not specified")

        state_counts = self.state_counts(node)
        bayesian_counts = state_counts + pseudo_counts

        cpd = TabularCPD(
            node,
            node_cardinality,
            np.array(bayesian_counts),
            evidence=parents,
            evidence_card=parents_cardinalities,
            state_names={var: self.state_names[var] for var in chain([node], parents)},
        )
        cpd.normalize()
        values=cpd.get_values()
        card=cpd.variable_card
        cardi=cpd.cardinality
        valor=[]
        for value in values:
            v=[]
            for value_1 in value:
                v.append(round(value_1, 8))
            valor.append(v)
        return valor,card,cardi

#--- Função que cria as inferencias das Redes Dinâmicas Criadas
  
def Dynamic_Bayesian_Inference(topologia, top, discretized_df,data,data_sup,mes,faixas,json_doc):
    
    #REDE BAYESIANA DINÂMICA
    dbn = DBN()
    dbn.add_edges_from(topologia)
    CPDs=build_dbn_cpds(top,dbn,dbn.nodes(),discretized_df)
    for cpds in CPDs:
        dbn.add_cpds(cpds)
    dbn.initialize_initial_state()
    
    dbn_inf = DBNInference(dbn)
    meses_=['JANEIRO','FEVEREIRO','MARCO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']
    with open(json_doc, 'r') as js_file:
            inferencia = json.load(js_file)
    key=list(inferencia.keys())
    value=list(inferencia.values())
    target=(key[0],value[0])
    
    flag=float(data_sup[target[0]+'_1'][len(data)-1])

    dicio=dict()
    dicio_target=[]
    print(meses_[mes],'-------------------------------------------------------------------------------|')
    for i in range(int(target[1])):
        g_key=list(inferencia['ANO_'+str(i)].keys())
        # SE O ANO TIVER EVIDENCIA, SERÁ FEITO INFERENCIA COM EVIDENCIA REFERENTE AO TEMPO E MÊS CORRENTE
        if len(inferencia['ANO_'+str(i)])!=0 and 'MES_'+str(mes) in g_key and len(inferencia['ANO_'+str(i)]['MES_'+str(mes)])!=0:
            dict_local=dict()
            # SEÁ PEGO AS EVIDENCIAS DO MÊS REFERENTE A BASE USADA
            evidencias=inferencia['ANO_'+str(i)].get('MES_'+str(mes))
            l_key=list(evidencias.keys())
            l_value=list(evidencias.values())
            # SERÁ CRIADO UM DICIONARIO PARA A FUNÇÃO DE INFERENCIA REFERENTE AO TEMPO E MÊS ESPECIFICO
            d=dict()
            for k in range(len(l_key)):
                evi=(l_key[k],i)
                d[evi]=int(l_value[k])
        
            inf=list(dbn_inf.backward_inference([(target[0],i)],d)[(target[0],i)].values)
        
            prob=max(inf)
            index_prob=inf.index(prob)
            f=list(faixas[target[0]+'_'+'0'])
            print('faixas ',f)
            pormed = ((float(f[int(index_prob)])+float(f[int(index_prob)+1]))/2)/100
            medflag = flag*pormed+flag
            maxflag =(flag*(f[int(index_prob)+1]/100))+flag  
            flag=    (flag*(f[int(index_prob)]/100))+flag
                
            nivel=['Baixo', 'Medio', 'Alto']
            print(target[0],'--- Tempo'+'_'+str(i),'--- Probabilidade: ',prob,'--- Nivel: ',nivel[index_prob])
            print('Min: ',flag)
            print("Media",medflag)
            print('Max: ',maxflag,'\n')
            dict_local['VALOR TOTAL']=flag
            dict_local['PROBABILIDADE']=prob
            dict_local['NIVEL']=nivel[index_prob]
            dict_local['MEDIO']= medflag#(float(f[int(index_prob)])+float(f[int(index_prob)+1]))/2
            dict_local['MAX']=maxflag#f[int(index_prob)+1]
            dict_local['MIN']=flag#f[int(index_prob)]
            dicio_target.append(dict_local)
            
        elif len(inferencia['ANO_'+str(i)])!=0 and 'MES_'+str(mes) not in g_key:
            continue
    
    
        else:
            dict_local=dict()
            inf=list(dbn_inf.backward_inference([(target[0], i)])[(target[0],i)].values)
            prob=max(inf)
            index_prob=inf.index(prob)
            f=list(faixas[target[0]+'_'+'0'])
            
            pormed = ((float(f[int(index_prob)])+float(f[int(index_prob)+1]))/2)/100
            medflag = flag*pormed+flag
            maxflag =(flag*(f[int(index_prob)+1]/100))+flag  
            
            flag=(flag*(f[int(index_prob)]/100))+flag
            nivel=['Baixo', 'Medio', 'Alto']
            print(target[0],'--- Tempo'+'_'+str(i),'--- Probabilidade: ',prob,'--- Nivel: ',nivel[index_prob])
            print('Min: ',flag)
            print("Media",medflag)
            print('Max: ',maxflag,'\n')
            
            dict_local['VALOR TOTAL']=flag
            dict_local['PROBABILIDADE']=prob
            dict_local['NIVEL']=nivel[index_prob]
            dict_local['MEDIO']= medflag#(float(f[int(index_prob)])+float(f[int(index_prob)+1]))/2
            dict_local['MAX']=maxflag#f[int(index_prob)+1]
            dict_local['MIN']=flag#f[int(index_prob)]
            dicio_target.append(dict_local)
        dicio[target[0]]=dicio_target

        
    return dicio

def build_dbn(topologia, top, nodes, dataframe, n_bins, tipo_discretizacao, json_doc, usuario):
    meses=['JANEIRO','FEVEREIRO','MARCO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']
    dic_infer=dict()
    
    dataset=build_porcentagem(dataframe)
    dataframe = dataframe.loc[12:len(dataframe)]
    dataframe = dataframe.reset_index(drop=True)
    #dataset=dt.loc[12:len(dt)]
    for m in range(len(meses)):
        mes=m
        
        data = criar_base_mes(mes,dataset)
        data_sup=criar_base_mes(mes,dataframe)
        #data_sup=data_sup.loc[1:len(data_sup)]
    
        #DISCRETIZA CADA DATASET
        # Tipos de discrcetização:     kmeans (Default)   |     quantile    |     uniform
        # def discretize_data_quantile(dataframe,lista,bins,type_discr='kmeans')

        discretized_data,faixas = discretize_data_quantile(data, n_bins, tipo_discretizacao)

        #INFERENCIA DE CADA MÊS
        infer=Dynamic_Bayesian_Inference(topologia, top,discretized_data,data,data_sup,mes, faixas, json_doc)

        dic_infer[meses[mes]]=infer

    # ----- Salva modelo (pickle) e intervalos de discretização (csv? json?)

    with open('../Data/JSON_files/SAIDA_'+usuario+'.json', 'w') as json_file:
        json.dump(dic_infer, json_file, indent=4)
    
    return dic_infer
    
