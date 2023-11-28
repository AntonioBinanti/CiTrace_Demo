# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:02:47 2023

@author: AntonioBinanti
"""
#%% Import librerie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#%%
SQLALCHEMY_DATABASE_URL = "postgresql://utente1:gBudzRyqR1ebZVOY2TobUyJINDB3Sqac@dpg-cleu9jbl00ks739tvo20-a/prova_urov" #PER RENDER.COM
#SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db" #PER DB LOCALE

engine = create_engine(
    SQLALCHEMY_DATABASE_URL#, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()