#%% Import librerie 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import ast
from pathlib import Path

#%% Variabili globali
__version__ = "0.1.1"
BASE_DIR = Path(__file__).resolve(strict=True).parent

#%% Import datasets
request = pd.read_csv("C:\\Users\\AntonioBinanti\\Documents\\CiTrace\\Datasets\\Requests CiTrace\\Request.csv")
actualUser = pd.read_csv("C:\\Users\\AntonioBinanti\\Documents\\CiTrace\\Datasets\\Requests CiTrace\\ActualUser.csv")
device_info = pd.read_csv("C:\\Users\\AntonioBinanti\\Documents\\CiTrace\\Datasets\\Requests CiTrace\\device_info.csv")

#%% Conversione dati categorici
request["timestamp"] = pd.to_datetime(request["timestamp"])
request["year"] = request.timestamp.dt.year
request["month"] = request.timestamp.dt.month
request["day"] = request.timestamp.dt.day
request["day_week"] = request.timestamp.dt.day_of_week
request["hour"] = request.timestamp.dt.hour
request["minute"] = request.timestamp.dt.minute
request["event"] = request["event"].astype("category")#.cat.codes
request["component"] = request["component"].astype("category")#.cat.codes

actualUser["role"] = actualUser["role"].astype("category")#.cat.codes
actualUser["city"] = actualUser["city"].astype("category")#.cat.codes
actualUser["main_language_used"] = actualUser["main_language_used"].astype("category")#.cat.codes
actualUser.dtypes

#%% Join tra colonne request e actualUser (Magari da inserire nel modello a kluster, non qui)
X_r = request[["actualUser", "device_info"]]
list = actualUser["interests"].apply(ast.literal_eval).tolist()
X_u = pd.DataFrame(list, columns = ["i1", "i2"])
X_m = X_r.merge(X_u, left_on = "actualUser", right_index = True)
X_m["i1"] = X_m["i1"].astype("category").cat.codes
X_m["i2"] = X_m["i2"].astype("category").cat.codes
X_m.dtypes
#%% Inserimento valori in X e y
X = X_r[["actualUser", "device_info"]]
y = request["component"]

#%% Creazione plot del modello DecisionTree
dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)

tree.plot_tree(dtree)

#%% Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 100)

dtree = DecisionTreeClassifier(random_state = 100)
dtree.fit(X_train, y_train)

y_pred = dtree.predict(X_test)
print("Train data accuracy:",accuracy_score(y_true = y_train, y_pred = dtree.predict(X_train)))
print("Test data accuracy:",accuracy_score(y_true = y_test, y_pred = y_pred))

y_proba = dtree.predict_proba(X_test)

#%% Riconversione in valori categorici di y_proba
#codes = request.component.cat.codes
categories = request["component"].cat.categories
y_proba = pd.DataFrame(y_proba, columns = categories)

#%% Esportazione modello 
import pickle
pickle.dump(dtree,open(f"{BASE_DIR}/decisionTree_model-{__version__}.pkl",'wb'))

#%% Esempio log utente registrato
logged_users = [[3, 4],
                [0, 10],
                [0, 2],
                [0, 0]
                ] #[user_id, device_info_identifier]

out = dtree.predict_proba(logged_users)
out = pd.DataFrame(out, columns = categories)

for u in range(0, len(out)):
    comp = out.iloc[u].sort_values(ascending = False).index
    print(f"User {u}:")
    for u1 in range(0, len(comp)):
        print(f"{u1 + 1}: {comp[u1]}")