#LINK RIFERIMENTO: https://www.fullstackpython.com/blog/export-pandas-dataframes-sqlite-sqlalchemy.html
#%% Import librerie 
import numpy as np
import pandas as pd
import ast
from pathlib import Path
from app.database.database import engine
from app.database import models, schemas, crud_functions
from sqlalchemy.orm import Session

BASE_DIR = Path(__file__).resolve(strict=True).parent

#%% Import daset
def importa(db: Session):
    request = pd.read_csv(f"{BASE_DIR}/Request.csv")
    actualUser = pd.read_csv(f"{BASE_DIR}/ActualUser.csv")
    device_info = pd.read_csv(f"{BASE_DIR}/Device_info.csv")

#%% Modellazione DataFrames
    request = request.rename(columns = {"Unnamed: 0": "request_id"})
    actualUser = actualUser.rename(columns = {"Unnamed: 0": "user_id", "user_id": "username", "device_info_identifier": "device_info"})
    list = actualUser["device_info"].apply(ast.literal_eval).tolist()
    actualUser["device_info"] = np.NaN
    actualUser.logged_in.fillna(value = True, inplace = True)
    actualUser.logged_in_time.fillna(value = "Unknow", inplace = True)
    actualUser = actualUser.drop(columns = ["device_info"])
    device_info = device_info.drop(columns = ["identifier"])
    device_info = device_info.rename(columns = {"Unnamed: 0": "identifier"})
    device_info["owner_id"] = np.NaN

#%% Connessione al database
    postgresql_connection = engine.connect()

#%% Creazione tabelle
    db_all_Users = actualUser.to_sql("allUsers", postgresql_connection, if_exists = "append", index = False)
    #db_device_info = device_info.to_sql("device_info", postgresql_connection, if_exists = "append", index = False)
    db_request = request.to_sql("request", postgresql_connection, if_exists = "replace")

#%% Chiusura connessione
    postgresql_connection.close()

#%% Creazione relazioni
    num_devices = 0
    user_index = 0
    for user in list:
        for device in user:
            #db_user = crud_functions.get_user(db, username = user)
            #if db_user is None:
            #    raise HTTPException(status_code=404, detail="User not found")
            device_schemas = schemas.Device(
                device_type = f"device-{device}"
                )
            
            crud_functions.create_device_to_user(db, device = device_schemas, user_id = user_index)   
            num_devices = num_devices + 1
        user_index = user_index + 1

#%% Ritorno valori
    return {
        "num users imported": db_all_Users, 
        "num devices imported": num_devices, 
        "num request imported": db_request
        }

"""
#%%
import numpy as np
import pandas as pd
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

request = pd.read_csv(f"{BASE_DIR}/Request.csv")
actualUser = pd.read_csv(f"{BASE_DIR}/ActualUser.csv")
device_info = pd.read_csv(f"{BASE_DIR}/Device_info.csv")

request = request.rename(columns = {"Unnamed: 0": "request_id"})
actualUser = actualUser.rename(columns = {"Unnamed: 0": "user_id", "user_id": "username", "device_info_identifier": "device_info"})
list = actualUser["device_info"].apply(ast.literal_eval).tolist()
actualUser["device_info"] = np.NaN
actualUser.logged_in.fillna(value = True, inplace = True)
actualUser.logged_in_time.fillna(value = "Unknow", inplace = True)
actualUser = actualUser.drop(columns = ["device_info"])
device_info = device_info.drop(columns = ["identifier"])
device_info = device_info.rename(columns = {"Unnamed: 0": "identifier"})
device_info["owner_id"] = np.NaN

for user in list:
    for device in user:
        #db_user = crud_functions.get_user(db, username = user)
        #if db_user is None:
        #    raise HTTPException(status_code=404, detail="User not found")
        device_schemas = {
            "device_type": device
            }
        crud_functions.create_device_to_user(db, device = device_schemas, user_id = user)
"""
