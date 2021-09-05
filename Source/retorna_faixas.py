import json

with open('../Data/JSON_files/FAIXAS.json', 'r') as js_file:
    faixas = json.load(js_file)


with open('../Data/JSON_files/EVIDENCIAS_SUGERIDAS.json', 'r') as json_file:
    evi_sugeridas= json.load(json_file)
