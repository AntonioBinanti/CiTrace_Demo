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

#%% Variabili globali
interest_value = 0.5
n_clusters = 6

#%% Import dataset
request = pd.read_csv("C:\\Users\\AntonioBinanti\\Documents\\CiTrace\\Datasets\\Requests CiTrace\\Request.csv")
actualUser = pd.read_csv("C:\\Users\\AntonioBinanti\\Documents\\CiTrace\\Datasets\\Requests CiTrace\\ActualUser.csv")
device_info = pd.read_csv("C:\\Users\\AntonioBinanti\\Documents\\CiTrace\\Datasets\\Requests CiTrace\\device_info.csv")

#%% Conversione valori categorici (FATTA DOPO)
"""request["timestamp"] = pd.to_datetime(request["timestamp"])
request["year"] = request.timestamp.dt.year
request["month"] = request.timestamp.dt.month
request["day"] = request.timestamp.dt.day
request["day_week"] = request.timestamp.dt.day_of_week
request["hour"] = request.timestamp.dt.hour
request["minute"] = request.timestamp.dt.minute
request["event"] = request["event"].astype("category")#.cat.codes
request["component"] = request["component"].astype("category").cat.codes

actualUser["role"] = actualUser["role"].astype("category")#.cat.codes
actualUser["city"] = actualUser["city"].astype("category")#.cat.codes
actualUser["main_language_used"] = actualUser["main_language_used"].astype("category")#.cat.codes

list_user = actualUser["interests"].apply(ast.literal_eval).tolist()
actualUser[["interest1", "interest2"]] = list_user
list_dev = actualUser["device_info_identifier"].apply(ast.literal_eval).tolist()
actualUser[["dev_info1", "dev_info2"]] = list_dev
actualUser["role"] = actualUser["role"].astype("category").cat.codes
actualUser["city"] = actualUser["city"].astype("category").cat.codes
actualUser["interest1"] = actualUser["interest1"].astype("category").cat.codes
actualUser["interest2"] = actualUser["interest2"].astype("category").cat.codes
actualUser["dev_info1"] = actualUser["dev_info1"].astype("category")
actualUser["dev_info2"] = actualUser["dev_info2"].astype("category")"""

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
        

#%% Separazione interests e devices in più clonne
"""list_user = table["interests"].apply(ast.literal_eval).tolist()
table[["interest1", "interest2"]] = list_user
list_dev = table["device_info_identifier"].apply(ast.literal_eval).tolist()
table[["dev_info1", "dev_info2"]] = list_dev
#x = x.drop(["interests", "device_info_identifier"], axis = 1)"""

#%% Filtraggio valori utili per clusterizzazione
components = request["component"].unique().tolist()

x = pd.DataFrame()
#x[["role", "city"]] = table[["role", "city"]]
for c in components: #importiamo i click per componente da "table"
    x[c] = table[c]

x = x.drop_duplicates()
x = x.fillna(0)

#%% Conversione valori categorici
"""x["role"] = x["role"].astype("category").cat.codes
x["city"] = x["city"].astype("category").cat.codes
x["interest1"] = x["interest1"].astype("category").cat.codes
x["interest2"] = x["interest2"].astype("category").cat.codes"""

#Per convertire da cat.codes a cat.category
#a = x["role"].cat.categories[x["role"].cat.codes]
#%% Normalizzazione valori
#x_stand = ((x - x.min()) / (x.max() - x.min())) * 10
scaler = MinMaxScaler() 
x_stand = pd.DataFrame(scaler.fit_transform(x) * 10, columns = [components])
x.describe()
#%% Scelta numero cluster k utilizzando elbow method
max_iteraction_elbow = 10
res = []

for i in range(1, max_iteraction_elbow):
    kmeans = KMeans(n_clusters = i)
    kmeans.fit(x_stand)
    res.append(kmeans.inertia_)

plt.plot(range(1, max_iteraction_elbow), res, marker = "o")
plt.title("Elbow Method")
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.show()
#n_cluser sarà 6

#%% Scelta n_components per l'utilizzo del PCA
nums = np.arange(len(x.columns))
var_ratio = []
for num in nums:
  pca = PCA(n_components=num)
  pca.fit(x_stand)
  var_ratio.append(np.sum(pca.explained_variance_ratio_))

plt.figure(figsize=(4,2),dpi=150)
plt.grid()
plt.plot(nums,var_ratio,marker='o')
plt.xlabel('n_components')
plt.ylabel('Explained variance ratio')
plt.title('n_components vs. Explained Variance Ratio')
plt.show()
#%% Plot 2D del cluster

pca = PCA(n_components = 2) #Comprimiamo in 2 dimensioni, dal grafico precedente avremo un "mantenimento dell'informazione" del 70%"
data_2d = pca.fit_transform(x_stand)
#clear_output(wait=True)

hierarchical_cluster = AgglomerativeClustering(n_clusters= n_clusters, affinity='euclidean', linkage='ward')
labels = hierarchical_cluster.fit_predict(data_2d)

pal = sns.color_palette("hls", n_clusters)

colors = dict({})
for i in range(0, n_clusters):
    colors[i] = pal[i]
sns.scatterplot(x = data_2d[:,0], y = data_2d[:,1], hue = labels, palette = colors)    
plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
plt.title("Cluster utenti")

#%% Prova inserimento nuovi utenti
"""
new_users = [[0, 1, 0, 1, 0, 0],
             [0, 0, 1, 0, 1, 0],
             [0, 0, 1, 0, 0, 0],
             [1, 0, 0, 1, 0, 0],
             [1, 0, 1, 0, 0, 0],
             [0, 0, 1, 0, 0, 1],
             [1, 0, 0, 0, 1, 0],
             [1, 1, 0, 0, 1, 1]
            ]"""

new_users = [[1, 1, 0, 0, 0, 0],
             [0, 1, 0, 1, 0, 1],
             [0, 0, 1, 0, 0, 0],
             [0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 1]
            ]
new_users_stand = pd.DataFrame(scaler.fit_transform(new_users) * 10, columns = components)

new_users_2D = pca.transform(new_users_stand)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(data_2d, labels)
prediction = knn.predict(new_users_2D)

plt.figure(figsize = (6, 4))
sns.scatterplot(x = data_2d[:,0], y = data_2d[:,1], hue = labels, palette = colors)
ax = sns.scatterplot(x = new_users_2D[:,0], y = new_users_2D[:,1], hue = prediction, palette = colors, marker = "X", legend = False)
for i in range(0, len(new_users)):
    ax.text(new_users_2D[i, 0]-1.7, new_users_2D[i, 1]-0.6, new_users[i], size = 7)
plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
plt.title("Cluster nuovi utenti (x)")

plt.show()

#%% PROVA ESPORTAZIONE MODELLO
import pickle
pickle.dump(knn,open('KNN_model.pkl','wb'))
pickled_model=pickle.load(open('KNN_model.pkl','rb'))
## Prediction
pickled_model.predict(new_users_2D)