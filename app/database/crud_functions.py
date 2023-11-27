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

def get_device(db: Session, identifier: str):
    return db.query(models.Device_info).filter(models.Device_info.identifier == identifier).first()

def get_devices(db: Session):
    return db.query(models.Device_info).all()

#SISTEMARE DA QUI
def create_device_to_user(db: Session, device: schemas.Device, user_id: int):
    device_model = models.Device_info(**device.dict(), owner_id=user_id)
    db.add(device_model)
    db.commit()
    db.refresh(device_model)
    return device_model

