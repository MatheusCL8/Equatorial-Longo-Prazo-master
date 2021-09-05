from Utilities.utilities import build_edges
from pgmpy.models import BayesianModel

concessionaria=""
topology=""
node_list=""
top=""
nodes=""
def setup(string):
    global concessionaria
    global topology
    global node_list
    global top
    global nodes
    concessionaria=string

    '''top=[('PNT-TOT_0', 'CFCT_0'), ('NC-C_0', 'CFCT_0'), ('I-AEC_0', 'PNT-TOT_0'), ('I-AEC_0', 'NC-C_0'), ('IPAGRO_0', 'I-AEC_0'), ('IV-CVA_0', 'CFCT_0'), ('IV-CVA_0', 'NC-C_0'), ('IV-CVA_0', 'IPAGRO_0'), ('PT-TOT_0', 'PNT-TOT_0'), ('PT-TOT_0', 'I-AEC_0'), ('PT-TOT_0', 'IV-CVA_0'), ('NC-R_0', 'NC-C_0'), ('NC-R_0', 'PT-TOT_0'), ('NC-PPU_0', 'NC-C_0'), ('NC-PPU_0', 'NC-R_0'), ('PFI-IG_0', 'NC-PPU_0'),
    ('PNT-TOT_1', 'CFCT_1'), ('NC-C_1', 'CFCT_1'), ('I-AEC_1', 'PNT-TOT_1'), ('I-AEC_1', 'NC-C_1'), ('IPAGRO_1', 'I-AEC_1'), ('IV-CVA_1', 'CFCT_1'), ('IV-CVA_1', 'NC-C_1'), ('IV-CVA_1', 'IPAGRO_1'), ('PT-TOT_1', 'PNT-TOT_1'), ('PT-TOT_1', 'I-AEC_1'), ('PT-TOT_1', 'IV-CVA_1'), ('NC-R_1', 'NC-C_1'), ('NC-R_1', 'PT-TOT_1'), ('NC-PPU_1', 'NC-C_1'), ('NC-PPU_1', 'NC-R_1'), ('PFI-IG_1', 'NC-PPU_1'), 
    ('NC-C_0', 'PT-TOT_1'), ('PT-TOT_0', 'CFCT_1'), ('I-AEC_0', 'IV-CVA_1'), ('IV-CVA_0', 'IV-CVA_1'), ('PFI-IG_0', 'IV-CVA_1')]
    '''
    
    top_MA=[('IV-CVA_0', 'CFCT_0'), ('IPAGRO_0', 'CFCT_0'),
         ('Q-BF_0', 'IMR-TOT_0'), ('MR-PS_0', 'IMR-TOT_0'), ('IMR-TOT_0', 'PNT-TOT_0'), 
         ('IMR-TOT_0', 'CFCT_0'), ('NC-C_0', 'PNT-TOT_0'), ('NC-C_0', 'PT-TOT_0'),('NC-R_0', 'PT-TOT_0'),
         ('NC-R_0', 'PNT-TOT_0'), ('NC-I_0', 'PT-TOT_0'), ('PNT-TOT_0', 'PT-TOT_0'),('PT-TOT_0', 'CFCT_0'), 
         ('PNT-TOT_0', 'CFCT_0'), ('TEMP-MAX_0', 'CFCT_0'), ('I-PLUV_0', 'CFCT_0'),
         
         ('IV-CVA_1', 'CFCT_1'), ('IPAGRO_1', 'CFCT_1'), 
         ('Q-BF_1', 'IMR-TOT_1'), ('MR-PS_1', 'IMR-TOT_1'), ('IMR-TOT_1', 'PNT-TOT_1'), 
         ('IMR-TOT_1', 'CFCT_1'), ('NC-C_1', 'PNT-TOT_1'), ('NC-C_1', 'PT-TOT_1'),('NC-R_1', 'PT-TOT_1'),
         ('NC-R_1', 'PNT-TOT_1'), ('NC-I_1', 'PT-TOT_1'), ('PNT-TOT_1', 'PT-TOT_1'),('PT-TOT_1', 'CFCT_1'), 
         ('PNT-TOT_1', 'CFCT_1'), ('TEMP-MAX_1', 'CFCT_1'), ('I-PLUV_1', 'CFCT_1'),('CFCT_0','PNT-TOT_1')]
    
    
    top_PA=[('IV-CVA_0', 'I-AEC_0'), ('IPAGRO_0', 'I-AEC_0'), ('PFI-IG_0', 'I-AEC_0'),('PFI-IG_0', 'PNT-TOT_0'),
         ('I-AEC_0', 'CFCT_0'), ('Q-BF_0', 'IMR-TOT_0'), ('MR-PS_0', 'IMR-TOT_0'), ('IMR-TOT_0', 'PNT-TOT_0'), 
         ('IMR-TOT_0', 'CFCT_0'), ('NC-C_0', 'PNT-TOT_0'), ('NC-C_0', 'PT-TOT_0'),('NC-R_0', 'PT-TOT_0'),
         ('NC-R_0', 'PNT-TOT_0'), ('NC-I_0', 'PT-TOT_0'), ('PNT-TOT_0', 'PT-TOT_0'),('PT-TOT_0', 'CFCT_0'), 
         ('PNT-TOT_0', 'CFCT_0'), ('TEMP-MAX_0', 'CFCT_0'), ('I-PLUV_0', 'CFCT_0'),
         ('IV-CVA_1', 'I-AEC_1'), ('IPAGRO_1', 'I-AEC_1'), ('PFI-IG_1', 'I-AEC_1'),('PFI-IG_1', 'PNT-TOT_1'),
         ('I-AEC_1', 'CFCT_1'), ('Q-BF_1', 'IMR-TOT_1'), ('MR-PS_1', 'IMR-TOT_1'), ('IMR-TOT_1', 'PNT-TOT_1'), 
         ('IMR-TOT_1', 'CFCT_1'), ('NC-C_1', 'PNT-TOT_1'), ('NC-C_1', 'PT-TOT_1'),('NC-R_1', 'PT-TOT_1'),
         ('NC-R_1', 'PNT-TOT_1'), ('NC-I_1', 'PT-TOT_1'), ('PNT-TOT_1', 'PT-TOT_1'),('PT-TOT_1', 'CFCT_1'), 
         ('PNT-TOT_1', 'CFCT_1'), ('TEMP-MAX_1', 'CFCT_1'), ('I-PLUV_1', 'CFCT_1'),('CFCT_0','PNT-TOT_1')]
    
    top=[]
    
    if concessionaria=='PA':
         top=top_PA
         print('PA')
    elif concessionaria=='MA':
         top=top_MA
         print('MA')
    
    topology=build_edges(top)
    
    model = BayesianModel(top)
    nodes=list(model.nodes())
    
    tam=int(len(nodes)/2)
    names_t=nodes[0:tam]
    names=[]
    for name in names_t:
        names.append(name[0:-2])
    
    node_list=list(names)

