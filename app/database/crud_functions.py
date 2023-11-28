# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 17:20:00 2023

@author: AntonioBinanti
"""
#%% Impor librerie
from sqlalchemy.orm import Session
from . import schemas, models

#%% Funzioni

def get_user(db: Session, username: str):
    return db.query(models.AllUsers).filter(models.AllUsers.username == username).first()

def get_user_id(db: Session, user_id: int):
    return db.query(models.AllUsers).filter(models.AllUsers.user_id == user_id).first()

def get_users(db: Session):
    return db.query(models.AllUsers).all()


def create_user(db: Session, user: schemas.User):
    user_model = models.AllUsers(
        username = user.username,
        user_IP_address = user.user_IP_address,
        role = user.role,
        city = user.city,
        logged_in = user.logged_in,
        main_language_used = user.main_language_used
        )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

#def get_devices_user(db: Session, user_id: int):
#    return db.query(model.AllUsers).filter(models.AllUsers == user_id).

def get_device_model(db: Session, model: str):
    return db.query(models.Device_info).filter(models.Device_info.model == model).all()

def get_device_model_user(db: Session, model: str, user_id: int):
    return db.query(models.Device_info).filter(models.Device_info.model == model, models.Device_info.owner_id == user_id).first()

def get_device_identifier(db: Session, identifier: int):
    return db.query(models.Device_info).filter(models.Device_info.identifier == identifier).first()

def get_devices(db: Session):
    return db.query(models.Device_info).all()

def create_device_to_user(db: Session, device: schemas.Device, user_id: int):
    device_model = models.Device_info(**device.dict(), owner_id=user_id)
    db.add(device_model)
    db.commit()
    db.refresh(device_model)
    return device_model

def update_user(db: Session, user_updated: schemas.User, db_user: schemas.UserExt):
    user_data = user_updated.dict(exclude_unset = True) #Filtraggio dei soli valori inseriti dall'utente
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_device(db: Session, device_updated: schemas.Device, db_device: schemas.DeviceExt):
    device_data = device_updated.dict(exclude_unset = True) #Filtraggio dei soli valori inseriti dall'utente
    for key, value in device_data.items():
        setattr(db_device, key, value)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device
