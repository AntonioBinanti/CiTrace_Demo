# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 11:00:06 2023

@author: AntonioBinanti
"""

#%% Import librerie
from fastapi import FastAPI
from typing import Dict, List
from pydantic import BaseModel
from app.ML_models.model_functions import predict_cluster
from app.ML_models.model_functions import predict_components
from app.ML_models.model_functions import __version__ as model_version

#%% Definizione app e classi
app = FastAPI()

class UserReg(BaseModel):
    new_user_preferences: List[str]
    
class UserPref(BaseModel):
    user_id: int #long
    device_info_id: int #long
    
class PredictionCluster(BaseModel):
    cluster: List[int]
    
class PredictionComponents(BaseModel):
    scorciatoie: Dict[str, int]

#%% Definizione API app

@app.get("/")
def home():
    return {"health_check": "OK", "model_version": model_version}
    
@app.post("/predict_cluster", response_model = PredictionCluster)
def predict_clust(payload: UserReg):
    cluster = predict_cluster(payload.new_user_preferences)
    return {"cluster": cluster} 

@app.post("/predict_components")
def predict_comp(payload: UserPref):
    components_dict = predict_components(payload.user_id, payload.device_info_id)
    return {"Scorciatoie": components_dict}
    
#%% Test API