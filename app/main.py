# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 11:00:06 2023

@author: AntonioBinanti
"""

#%% Import librerie
from fastapi import FastAPI, Depends, HTTPException
#from typing import Dict, List
#from pydantic import BaseModel
from app.ML_models.model_functions import predict_cluster
from app.ML_models.model_functions import predict_components
from app.ML_models.model_functions import __version__ as model_version
from app.database import models, schemas, crud_functions
from app.database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from app.dataset import test_import_database

#%% Definizione app e database 
app = FastAPI()

models.Base.metadata.drop_all(bind = engine, checkfirst=True)
models.Base.metadata.create_all(bind = engine, checkfirst=True)

#%% Per aprire e chiudere le sessioni di utilizzo del database
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#%% Definizione API ML models

@app.get("/")
def home():
    return {"health_check": "OK", "model_version": model_version}
    
@app.post("/predict_cluster", response_model = schemas.PredictionCluster)
def predict_clust(payload: schemas.UserReg):
    cluster = predict_cluster(payload.new_user_preferences)
    return {"cluster": cluster} 

@app.post("/predict_components")
def predict_comp(payload: schemas.UserPref):
    components_dict = predict_components(payload.user_id, payload.device_info_id)
    return {"Scorciatoie": components_dict}

#%% API CRUD per il database

@app.get("/users", response_model = list[schemas.UserExt])
def get_users(db: Session = Depends(get_db)):
    db_users = crud_functions.get_users(db)
    return db_users

@app.get("/user_username/{username}", response_model=schemas.UserExt)
def get_user(username: str, db: Session = Depends(get_db)):
    db_user = crud_functions.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/user_id/{user_id}", response_model=schemas.UserExt)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_functions.get_user_id(db, user_id = user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/user_requests/{user_id}", response_model=schemas.UserRequests)
def get_user_requests(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_functions.get_user_id(db, user_id = user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/devices", response_model = list[schemas.DeviceExt])
def get_devices(db: Session = Depends(get_db)):
    db_devices = crud_functions.get_devices(db)
    return db_devices

@app.get("/device_type{device_type}", response_model = list[schemas.DeviceExt])
def get_device_type(device_type: str, db: Session = Depends(get_db)):
    db_devices = crud_functions.get_device_type(db, device_type = device_type)
    if db_devices is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return db_devices
    
@app.get("/device_id/{identifier}", response_model = schemas.DeviceExt)
def get_device_id(identifier: int, db: Session = Depends(get_db)):
    db_devices = crud_functions.get_device_identifier(db, identifier = identifier)
    if db_devices is None:
        raise HTTPException(status_code=404, detail="Identifier not found")
    return db_devices

@app.get("/requests", response_model = list[schemas.Request])
def get_devices(db: Session = Depends(get_db)):
    db_requests = crud_functions.get_requests(db)
    return db_requests

@app.get("/request_id/{request_id}", response_model = schemas.Request)
def get_request_id(request_id: int, db: Session = Depends(get_db)):
    db_request = crud_functions.get_request_id(db, request_id = request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

@app.post("/add_user", response_model = schemas.UserExt)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud_functions.get_user(db, username = user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User_id already registered")
    return crud_functions.create_user(db=db, user=user)

@app.post("/add_device_to_user/{username}", response_model=schemas.DeviceExt)
def create_device_to_user(username: str, device: schemas.Device, db: Session = Depends(get_db)):
    #db_device = crud_functions.get_device(db, identifier = device.identifier)
    db_user = crud_functions.get_user(db, username = username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.device_info is not None:
        for dev in db_user.device_info:
            if device.device_type == dev.device_type:
                raise HTTPException(status_code=400, detail="Device already registered")
    return crud_functions.create_device_to_user(db=db, device=device, user_id=db_user.user_id)

@app.put("/update_user/{username}") 
def update_user(username: str, user_updated: schemas.User, db: Session = Depends(get_db)):
    db_user = crud_functions.get_user(db, username = username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_functions.update_user(db=db, user_updated=user_updated, db_user=db_user)

@app.put("/update_device_user/{device_type}/{username}") 
def update_device(device_type: str, username: str, device_updated: schemas.Device, db: Session = Depends(get_db)):
    db_user = crud_functions.get_user(db, username = username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_device = crud_functions.get_device_model_user(db, device_type = device_type, user_id = db_user.user_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return crud_functions.update_device(db=db, device_updated=device_updated, db_device = db_device)

@app.delete("/user/{username}")
def delete_user(username: str, db: Session = Depends(get_db)): 
    db_user = crud_functions.get_user(db, username = username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    #Fare prima delete di tutte le requests e i devices associati
    for req in db_user.requests:
        db.delete(req)
    for dev in db_user.device_info:
        db.delete(dev)
    db.delete(db_user)
    db.commit()
    return {"ok": True}

@app.delete("/device/{model}/{username}")
def delete_device(device_type: str, username: str, db: Session = Depends(get_db)):
    db_user = crud_functions.get_user(db, username = username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_device = crud_functions.get_device_model_user(db, device_type = device_type, user_id = db_user.user_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(db_device)
    db.commit()
    return {"ok": True}

@app.delete("/request/{request_id}")
def delete_device(request_id: int, db: Session = Depends(get_db)):
    db_request = crud_functions.get_request_id(db, request_id = request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    db.delete(db_request)
    db.commit()
    return {"ok": True}
#%% Test API

@app.get("/importa")
def importa(db: Session = Depends(get_db)):
    import_list = test_import_database.importa(db)
    
    return {
        "Import": "Ok",
        "Details": import_list
        }