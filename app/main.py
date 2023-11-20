# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 11:00:06 2023

@author: AntonioBinanti
"""

#%% Import librerie
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from app.ML_models.model_functions import predict_cluster
from app.ML_models.model_functions import __version__ as model_version

#%% Definizione app e classi
app = FastAPI()

class UserIn(BaseModel):
    new_user_preferences: List[str]
    
class PredictionOut(BaseModel):
    cluster: List[int]

#%% Definizione API app

@app.get("/")
def home():
    return {"health_check": "OK", "model_version": model_version}

@app.post("/predict")#, response_model = PredictionOut)
def predict(payload: UserIn):
    cluster = predict_cluster(payload.new_user_preferences)
    return {"cluster": cluster}
    
#%% Test API