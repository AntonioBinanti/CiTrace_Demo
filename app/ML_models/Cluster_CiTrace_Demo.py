#%% Import librerie
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn import preprocessing
import ast
from sklearn.decomposition import PCA
from IPython.display import clear_output
from sklearn.neighbors import KNeighborsClassifier
import seaborn as sns
from pathlib import Path
from sqlalchemy.orm import Session
from app.database.database import engine

#%% Variabili globali
__version__ = "0.1.0"
BASE_DIR = Path(__file__).resolve(strict=True).parent
interest_value = 0.5
n_clusters = 6

#%% Funzione modello

def retrain_cluster_model(db: Session):
#%% Connessione al database

    postgresql_connection = engine.connect()
    
    request = pd.read_sql("request", postgresql_connection)
    actualUser = pd.read_sql("allUsers", postgresql_connection)
    device_info = pd.read_sql("device_info", postgresql_connection)
    
    postgresql_connection.close()
    
#%% Merge tabelle
    table = request.merge(actualUser, left_on = "actualUser", right_on = "user_id")
    
#%% Inserimento numero click per componente
    num_users = table["actualUser"].nunique()
    num_click = table.groupby("actualUser")["component"].value_counts()

    click_table = pd.DataFrame()
    for u in range(0, len(num_click)):
        a = num_click.index[u][1]
        click_table.loc[num_click.index[u][0], "user_id"] = num_click.index[u][0]
        click_table.loc[num_click.index[u][0], num_click.index[u][1]] = num_click.values[u]
    
    table = table.merge(click_table, left_on = "actualUser", right_on = "user_id")
    
#%% Aumento punteggio components in base alle preferenze dell'utente
    interests_list = table["interests"].apply(ast.literal_eval)
    for i in range(0, len(interests_list)):
        for j in interests_list[i]:
            value = table.loc[i, j]
            table.loc[i, j] = value + value * interest_value  

#%% Filtraggio valori utili per clusterizzazione
    components = request["component"].unique().tolist()

    x = pd.DataFrame()
    for c in components: #importiamo i click per componente da "table"
        x[c] = table[c]
        
        x = x.drop_duplicates()
        x = x.fillna(0)

#%% Normalizzazione valori
    
    scaler = MinMaxScaler() 
    x_stand = pd.DataFrame(scaler.fit_transform(x) * 10, columns = [components])
    x.describe()
        
#%% Plot 2D del cluster

    pca = PCA(n_components = 2) #Comprimiamo in 2 dimensioni, dal grafico precedente avremo un "mantenimento dell'informazione" del 70%"
    data_2d = pca.fit_transform(x_stand)
    
    hierarchical_cluster = AgglomerativeClustering(n_clusters= n_clusters, affinity='euclidean', linkage='ward')
    labels = hierarchical_cluster.fit_predict(data_2d)

#%% Creazione modello KNN
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(data_2d, labels)

#%% PROVA ESPORTAZIONE MODELLO, SCALER, COMPONENTS E PCA
    import pickle

    pickle.dump(knn,open(f"{BASE_DIR}/KNN_model-{__version__}.pkl",'wb'))
    pickle.dump(scaler, open(f"{BASE_DIR}/scaler_components.pkl", "wb"))
    pickle.dump(components, open(f"{BASE_DIR}/components.pkl", "wb"))
    pickle.dump(pca, open(f"{BASE_DIR}/pca.pkl", "wb"))

    return {
        "Ok": True,
        "num_users_imported": f"{len(actualUser)}",
        "num_requests_imported": f"{len(request)}",
        "num_devices_imported": f"{len(device_info)}",
        "num_users_used_for_training": f"{len(x)}"
        }

