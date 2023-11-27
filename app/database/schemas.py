# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 17:21:00 2023

@author: AntonioBinanti
"""

#%% Import librerie
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

#%% Definizione Pydantic models di input ed output
class UserReg(BaseModel):
    new_user_preferences: List[str]
    
class UserPref(BaseModel):
    user_id: int #long
    device_info_id: int #long
    
class PredictionCluster(BaseModel):
    cluster: List[int]
    
class PredictionComponents(BaseModel):
    scorciatoie: Dict[str, int]
    
class Device(BaseModel):
    model: str
    class Config:
        orm_mode = True
    
class DeviceExt(Device):
    identifier: str
    owner_id: Optional[int] 
    #owners: Optional[List[str]] = [] #DA CONTROLLARE
    
class User(BaseModel):
    #user_id: int
    username: str
    user_IP_address: int
    role: str
    city: str
    #interests: List[str]
    logged_in: bool
    #logged_in_time: str
    main_language_used: str
    class Config:
        orm_mode = True
    
class UserExt(User):
    #dev_info: Optional[str]
    user_id: int
    device_info: Optional[List[Device]] = []
