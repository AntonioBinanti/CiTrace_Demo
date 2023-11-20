# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 10:36:42 2023

@author: AntonioBinanti
"""
#%% Import librerie
import pickle
from pathlib import Path
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

#%% Variabili globali
__version__ = "0.1.0"

BASE_DIR = Path(__file__).resolve(strict=True).parent

#%% Import dati   
model_knn = pickle.load(open(f"{BASE_DIR}/KNN_model-{__version__}.pkl", "rb"))
components = pickle.load(open(f"{BASE_DIR}/components.pkl", "rb"))
pca = pickle.load(open(f"{BASE_DIR}/pca.pkl", "rb"))
scaler = pickle.load(open(f"{BASE_DIR}/scaler_components.pkl", "rb"))
model_dtree = pickle.load(open(f"{BASE_DIR}/decisionTree_model-{__version__}.pkl",'rb'))

#%% Predizioni
def predict_cluster(preferences): 
    preference_int = [1 if pref in preferences else 0 for pref in components]
    preferences_agg = [preference_int] * scaler.data_max_ * 0.75
    new_users_stand = pd.DataFrame(scaler.transform(preferences_agg) * 10, columns = components)
    new_users_2D = pca.transform(new_users_stand)
    prediction = model_knn.predict(new_users_2D)
    return prediction.tolist()

def predict_components(user_id, device_info_id):
    out = model_dtree.predict_proba([[user_id, device_info_id]])
    out = pd.DataFrame(out, columns = components)
    
    components_dict = {}
    for u in range(0, len(out)):
        comp = out.iloc[u].sort_values(ascending = False).index
        for u1 in range(0, len(comp)):
            components_dict[int(u1 + 1)] = comp[u1]
    return components_dict  #comp.tolist()
    
#%%Test
#a = predict_components(3, 4)
#print(a)


