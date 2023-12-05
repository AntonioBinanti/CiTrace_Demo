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
    device_type: str
    class Config:
        orm_mode = True
    
class DeviceExt(Device):
    identifier: int
    owner_id: Optional[int] 
    #owners: Optional[List[str]] = [] #DA CONTROLLARE
    
class Request(BaseModel):
    request_id: int
    event: str
    selector: Optional[str]
    timestamp: str
    page_url_current: Optional[str]
    actualUser: int #UserExt 
    device_info: int #DeviceExt
    component: str
    class Config:
        orm_mode = True
    
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
    user_id: int
    device_info: Optional[List[Device]] = []
    
class UserRequests(User):
    user_id: int
    requests: Optional[List[Request]] = []
