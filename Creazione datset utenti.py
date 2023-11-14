#%%
import matplotlib.pyplot as plt
import pandas as pd
import random
from datetime import datetime
from enum import Enum
#%% Variabili globali
num_users = 50
num_device_infos = 10

#%% Creazione Enums
class Role(Enum):
    Agricoltore = 0
    Raccolta = 1
    Logistica_raccolta = 2
    Confezionatore = 3
    Amministratore_logistica_di_distribuzione = 4
    Impiegato_logistica_di_distribuzione = 5
    Amministratore_distribuzione = 6
    Impiegato_distribuzione = 7
    Amministratore_vendita_al_dettaglio = 8
    Impiegato_vendita_al_dettaglio = 9
    Consumatore = 10
    
class Interest(Enum):
    Prezzi_di_mercato = 0
    Metereologia = 1
    Gestione_magazzino = 2
    Gestione_attività = 3
    Gestione_contatti = 4
    Risorse_didattiche = 5
    
class City(Enum):
    Catania = 0
    Palermo = 1
    Siracusa = 2
    Messina = 3
    Ragusa = 4
    
class Language(Enum):
    Italian = 0
    English = 1
    Spanish = 2
    French = 3
    
class Event(Enum):
    Register = 0
    Click = 1
    View = 2
    
class Component(Enum):
    Prezzi = 0
    Previsionimeteo = 1
    Magazzino = 2
    Quaderno = 3
    Rubrica = 4
    Education = 5
    
#%% Creazione ActualUser
actualUser = pd.DataFrame(columns = ["user_id", "role", "interests", "user_ip_address", "city", "main_language_used", "logged_in", "logged_in_time", "device_info_identifier"])

random.seed(32)
for i in range(0, num_users): #da inserire interests
    new_user_list = [(i, random.choice(list(Role)).name, random.randint(10000, 99999), random.choice(list(City)).name, Language.Italian.name, [random.randint(0, 5), random.randint(5, 10)])]
    new_row = pd.DataFrame(new_user_list, columns = ["user_id", "role", "user_ip_address", "city", "main_language_used", "device_info_identifier"])
    actualUser = pd.concat([actualUser, new_row], ignore_index = True)
   
#%% Creazione Device_info
device_info = pd.DataFrame(columns = ["identifier", "browser", "browser_version", "device_type", "operative_system", "platform", "resolution", "zoom", "dark_mode"])

for i in range(0, num_device_infos):
    new_device_list = [(i)]
    new_row = pd.DataFrame(new_device_list, columns = ["device_type"])
    device_info = pd.concat([device_info, new_row], ignore_index = True)
    
#%% Creazione Context
context = pd.DataFrame(columns = ["page_value", "selected_filter", "selected_value_min", "selected_value_max", "chart_type", "chart_data", "chart_options", "zoom_page", "comparison_type", "comparison_years", "component", "location", "referrer", "article_owner", "target", "tags"])
 
#%% Creazione Request
request = pd.DataFrame(columns = ["event", "selector", "timestamp", "page_url_current", "actualUser", "device_info", "component"])
for i in range(0,100):  #Ogni utente clicca sullo stesso component per 100 volte
    for j in range (0, num_users):
        anno = random.randint(2020, 2023)
        mese = random.randint(1, 12)
        giorno = random.randint(1, 27)
        ora = random.randint(0, 23)
        minuti = random.randint(0, 59)
        date  = datetime(anno, mese, giorno, ora, minuti)
        user = actualUser.loc[actualUser["user_id"] == j].copy()
        device = user["device_info_identifier"].iloc[0][0]
        #device = user["device_info_identifier"].values.tolist()[0][0]
        new_request_list = [(
            Event.Click.name,
            date,
            j,
            device,
            Component(j % 6).name
        )]
        new_row = pd.DataFrame(new_request_list, columns = ["event", "timestamp", "actualUser", "device_info", "component"])
        request = pd.concat([request, new_row], ignore_index = True)
        
for i in range(0,80):  #Ogni utente clicca sullo stesso component per 80 volte
    for j in range (0, num_users):
        anno = random.randint(2020, 2023)
        mese = random.randint(1, 12)
        giorno = random.randint(1, 27)
        ora = random.randint(0, 23)
        minuti = random.randint(0, 59)
        date  = datetime(anno, mese, giorno, ora, minuti)
        user = actualUser.loc[actualUser["user_id"] == j].copy()
        device = user["device_info_identifier"].iloc[0][1]
        new_request_list = [(
            Event.Click.name,
            date,
            j,
            device,
            Component((j + 2) % 6).name
        )]
        new_row = pd.DataFrame(new_request_list, columns = ["event", "timestamp", "actualUser", "device_info", "component"])
        request = pd.concat([request, new_row], ignore_index = True) 
        
for i in range(0,60):  #Ogni utente clicca sullo stesso component per 60 volte
    for j in range (0, num_users):
        anno = random.randint(2020, 2023)
        mese = random.randint(1, 12)
        giorno = random.randint(1, 27)
        ora = random.randint(0, 23)
        minuti = random.randint(0, 59)
        date  = datetime(anno, mese, giorno, ora, minuti)
        user = actualUser.loc[actualUser["user_id"] == j].copy()
        device = user["device_info_identifier"].iloc[0][0]
        new_request_list = [(
            Event.Click.name,
            date,
            j,
            device,
            Component((j + 3) % 6).name
        )]
        new_row = pd.DataFrame(new_request_list, columns = ["event", "timestamp", "actualUser", "device_info", "component"])
        request = pd.concat([request, new_row], ignore_index = True) 
        
for i in range(0,40):  #Ogni utente clicca sullo stesso component per 40 volte
    for j in range (0, num_users):
        anno = random.randint(2020, 2023)
        mese = random.randint(1, 12)
        giorno = random.randint(1, 27)
        ora = random.randint(0, 23)
        minuti = random.randint(0, 59)
        date  = datetime(anno, mese, giorno, ora, minuti)
        user = actualUser.loc[actualUser["user_id"] == j].copy()
        device = user["device_info_identifier"].iloc[0][1]
        new_request_list = [(
            Event.Click.name,
            date,
            j,
            device,
            Component((j + 4) % 6).name
        )]
        new_row = pd.DataFrame(new_request_list, columns = ["event", "timestamp", "actualUser", "device_info", "component"])
        request = pd.concat([request, new_row], ignore_index = True) 
        
for i in range(0,20):  #Ogni utente clicca sullo stesso component per 20 volte
    for j in range (0, num_users):
        anno = random.randint(2020, 2023)
        mese = random.randint(1, 12)
        giorno = random.randint(1, 27)
        ora = random.randint(0, 23)
        minuti = random.randint(0, 59)
        date  = datetime(anno, mese, giorno, ora, minuti)
        user = actualUser.loc[actualUser["user_id"] == j].copy()
        device = user["device_info_identifier"].iloc[0][1]
        new_request_list = [(
            Event.Click.name,
            date,
            j,
            device,
            Component((j + 1) % 6).name
        )]
        new_row = pd.DataFrame(new_request_list, columns = ["event", "timestamp", "actualUser", "device_info", "component"])
        request = pd.concat([request, new_row], ignore_index = True)    
        
for i in range(0,20):  #Ogni utente clicca su component casuali per 20 volte
    for j in range (0, num_users):
        anno = random.randint(2020, 2023)
        mese = random.randint(1, 12)
        giorno = random.randint(1, 27)
        ora = random.randint(0, 23)
        minuti = random.randint(0, 59)
        date  = datetime(anno, mese, giorno, ora, minuti)
        user = actualUser.loc[actualUser["user_id"] == j].copy()
        device = user["device_info_identifier"].iloc[0][0]
        new_request_list = [(
            Event.Click.name,
            date,
            j,
            device,
            random.choice(list(Component)).name
        )]
        new_row = pd.DataFrame(new_request_list, columns = ["event", "timestamp", "actualUser", "device_info", "component"])
        request = pd.concat([request, new_row], ignore_index = True)
#%% Numero clic su component
for i in range(0, len(actualUser)): 
    row = request[request['actualUser'] == i]['component'].value_counts()
    print(f"User {i}:\n{row}")
    
#%% Aggiunta campo "interests" (In base al numero di click effettuato dagli utenti nei cicli for precedenti)
for i in range(0, len(actualUser)): 
    row = request[request['actualUser'] == i]['component'].value_counts()
    interests_list = [[row.index[0]],
                      [row.index[1]]
                      ]
    actualUser.loc[i, "interests"] = interests_list

#%% Test
series = actualUser["interests"].tolist()[0][0]

#%% Esportazione Dataset
request.to_csv("C:\\Users\\AntonioBinanti\\Documents\\CiTrace\\Datasets\\Requests CiTrace\\Request.csv")
actualUser.to_csv("C:\\Users\\AntonioBinanti\\Documents\\CiTrace\\Datasets\\Requests CiTrace\\ActualUser.csv")
device_info.to_csv("C:\\Users\\AntonioBinanti\\Documents\\CiTrace\\Datasets\\Requests CiTrace\\Device_info.csv")