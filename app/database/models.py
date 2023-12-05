# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:08:52 2023

@author: AntonioBinanti
"""
#%% import librerie
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database.database import Base
from typing import Dict, List

#%% Creazione tabelle
#association_users_device_info = Table(
#    "association_users_device_info",
#    Base.metadata,
#    Column("user_id", ForeignKey("allUsers.user_id")),
#    Column("device_info_id", ForeignKey("device_info.identifier"))
#    )

class AllUsers(Base):
    __tablename__ = "allUsers"
    
    user_id = Column(Integer, primary_key = True, index = True)
    username = Column(String)
    user_IP_address = Column(Integer)
    role = Column(String)
    city = Column(String)
    interests = Column(String)#List[String]) #DA ATTENZIONARE
    logged_in = Column(Boolean)
    logged_in_time = Column(String)
    main_language_used = Column(String)
    
    device_info = relationship("Device_info") #, back_populates = "owners")
    requests = relationship("Request")
    
class Device_info(Base):
    __tablename__ = "device_info"
    
    identifier = Column(Integer, primary_key = True, index = True)
    browser = Column(String)
    browser_version = Column(String)
    device_type = Column(String)
    operative_system = Column(String)
    platform = Column(String)
    resolution = Column(String)
    zoom = Column(String)
    dark_mode = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("allUsers.user_id"))
    
    #owners = relationship("AllUsers", back_populates = "device_info")
    #VEDERE SE NEESSARIA LA RELATIONSHIP CON REQUEST
    #users = relationship("AllUsers", secondary = "association_users_device_info")
    
class Request(Base):
    __tablename__ = "request"
    
    request_id = Column(Integer, primary_key = True, index = True)
    event = Column(String)
    selector = Column(String)
    timestamp = Column(String)
    page_url_current = Column(String)
    actualUser = Column(Integer, ForeignKey("allUsers.user_id"))#relationship("AllUsers")
    device_info = Column(Integer) #, ForeignKey("device_info.identifier")) #relationship("Device_info")
    component = Column(String)
                    
    