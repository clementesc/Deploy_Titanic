from fastapi import Body, FastAPI
from typing import Any
import json
import data_handler

# rodar nossa API
# $ uvicorn main:api --reload

api = FastAPI()

@api.get("/")
def root():
    return {"message": "Service OK"}

@api.get("/get-titanic-data")
def get_titanic_data():
    dados = data_handler.load_data()
    dados_json = dados.to_json(orient='records')
    return dados_json

@api.get("/get-all-predictions")
def get_all_predictions():
    dados_json = data_handler.get_all_predictions()
    return dados_json

@api.post("/save-prediction")
def save_prediction(passageiro_json: Any = Body(None)):
    passageiro = json.loads(passageiro_json)
    result = data_handler.save_prediction(passageiro)

    return result

@api.post("/predict")
def predict(passageiro_json: Any = Body(None)):
    passageiro = json.loads(passageiro_json)
    result = data_handler.survival_predictor(passageiro)
    
    return result