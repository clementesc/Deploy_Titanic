import pandas as pd
import numpy as np
import json
import pickle
import os

def  load_data():
    dados = pd.read_csv('./data/titanic.csv')

    return dados

# retorna todos os dados já armazenados das predições realizadas e validadas pelo usuário
# TODO: verificar se o arquivo existe antes de abrir
def get_all_predictions():
    data = None
    with open('predictions.json', 'r') as f:
        data = json.load(f)
        
    return data

# salva as predições em um arquivo JSON
# TODO: verificar se já não está salvo no arquivo antes de salvar de novo
def save_prediction(passageiro):
    # le todos as predições
    data = get_all_predictions()
    # adiciona a nova predição nos dados já armazenados
    data.append(passageiro)
    # salva todas as predições no arquivo json
    with open('predictions.json', 'w') as f:
        json.dump(data, f)

def survival_predictor(passageiro):
    # Mapeia o 'Sexo' e 'Embarcado' para valores numéricos.
    # dados['Sex'] = dados['Sex'].map({'male':0, 'female':1})
    # dados['Embarked'] = dados['Embarked'].map({'C':0, 'Q':1, 'S':2}

    P_CLASS_MAP = {
        '1st': 1, 
        '2nd': 2, 
        '3rd': 3
    }
    SEX_MAP = {
        'Male': 0,
        'Female': 1,
    }
    EMBARKED_MAP = {
        'Cherbourg': 0, 
        'Queenstown': 1, 
        'Southampton': 2
    }
    
    # Realiza o mapeamento
    passageiro['Pclass'] = P_CLASS_MAP[passageiro['Pclass']]
    passageiro['Sex'] = SEX_MAP[passageiro['Sex']]
    passageiro['Embarked'] = EMBARKED_MAP[passageiro['Embarked']]
    
    # carrega o modelo de predição já treinado e validado
    model = pickle.load(open(os.path.join('models', 'model.pkl'), 'rb'))

    values = pd.DataFrame([passageiro])

    # Realiza a predição
    results = model.predict(values)

    result = None

    if len(results) == 1:
        result = int(results[0])

    return result             
    
