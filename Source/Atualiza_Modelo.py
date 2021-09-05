# Código para atualização de dados e modelos

# ----- Importa Bibliotecas

from Source.Utilities.utilities import load_csv, save_csv, load_model, variation_generator, variation_perc_generator, time_shifter, build_doc_variavel_discretizacao, build_edges, build_dbn
import pandas as pd



# ----- Configurações (#TODO Passar configurações para arquivo e ler diretamente do txt)


path_raw_data = '../Data/raw/Dataset_Injetada_Socioecon.csv'
path_output = '../Data/processed/'

df = load_csv(path_raw_data)

variation_perc_columns = df.columns                     # Colunas de variação em porcentagem
variation_columns = []                                  # Colunas de variação bruta
time_delta = 1                                          # Variação em meses


time_shifts = [1]                                       # Deslocamento no tempo em meses (variável alvo)
shifted_columns = ['INJETADA_var']                      # Variável a ser deslocada no tempo (variável alvo)


# ----- Dados brutos referente a Topologia de longo prazo

# VERIFICAR, POIS JÁ SE ESTÁ LENDO A BASE NO INÍCIO
data = pd.read_excel('../Data/raw/Dados Dinamica.xlsx', sheet_name = "Dados Brutos")
df=pd.DataFrame(data)

# ---- Gerar o arquivo de descritização  com os nomes das variáveis e o valor min e max.

num_bins = 3
method_discretization = 'kmeans'
build_doc_variavel_discretizacao(num_bins,method_discretization)


# ----- Cria colunas de variação

df_var = variation_perc_generator(df, variation_perc_columns, time_delta, inplace=True)
#df_var = variation_generator(df, variation_columns, time_delta, inplace=True)

# ----- Desloca a variável alvo no tempo

df_processed = time_shifter(df_var, shifted_columns, time_shifts, path_output, inplace=False)


# ------ TOPOLOGIA DA REDE BAYESIANA NORMAL
# ------ Inserção da topologia de uma rede bayesiana simples
top=[('IPAGRO_0', 'IBCR_0'),('IMR-TOT_0', 'CFCT_0'),('CFCT_0', 'IBCR_0'),('MR-BF_0', 'Q-BF_0'),('Q-BF_0', 'MR-PS_0'),('MR-PS_0', 'IBCR_0'),('IBCR_0', 'PMC_0'),('MR-PS_0', 'PMC_0'),
         ('IPAGRO_1', 'IBCR_1'),('IMR-TOT_1', 'CFCT_1'),('CFCT_1', 'IBCR_1'),('MR-BF_1', 'Q-BF_1'),('Q-BF_1', 'MR-PS_1'),('MR-PS_1', 'IBCR_1'),('IBCR_1', 'PMC_1'),('MR-PS_1', 'PMC_1'),
        ('PMC_0','CFCT_1')]

topology=build_edges(top)
       
# ----- Criação da Rede Dinâmica

build_dbn(topology, top, df, num_bins,method_discretization)
