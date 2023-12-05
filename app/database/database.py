# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:02:47 2023

@author: AntonioBinanti
"""
#%% Import librerie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import SingletonThreadPool

#%%
SQLALCHEMY_DATABASE_URL = "postgresql://utente1:va2dgjlCFUwVNL5IXnhwCfifKs1xRxXi@dpg-clng7b1ll56s73fhb8v0-a/db_citrace_demo" #DATABASE DI RENDER.COM
#SQLALCHEMY_DATABASE_URL = "sqlite:///./ciTrace.db" #PER DB LOCALE

engine = create_engine(
    SQLALCHEMY_DATABASE_URL#, poolclass = SingletonThreadPool#, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()