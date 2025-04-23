from datetime import time
import math 
import pandas as pd   # type: ignore
from sqlmodel import Session, Field, SQLModel, create_engine, select # type: ignore
from sqlalchemy import MetaData  # type: ignore
from sqlalchemy.schema import MetaData  # type: ignore
from sqlalchemy import Table, Column, Integer # type: ignore
from fastapi import FastAPI, Depends, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import Union 
from typing import Optional
import uvicorn # type: ignore
import pydantic # type: ignore
import numpy as np # type: ignore

class RollingRichies(SQLModel, table=True):
    firstname: str = Field(default=None)
    lastname: str = Field(default=None)
    username: str = Field(default=None)
    password: str = Field(default=None)
    extension: int = Field(default=None)
    email: str = Field(default=None)
    department: str = Field(default=None)
    account: str = Field(default=None)
    macAddress: str = Field(default=None) # mac has to be converted to string

# MySQL database connection parameters  
mysql_user = "root"
mysql_password = "hello"
mysql_host = "localhost"
mysql_port = "3306"
mysql_database = "mysqlDB" # database name 

# Public Retrival is to allow to get the password
# mysql_url = "mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}" # ?allowPublicKeyRetrieval=True"
# MySQL database connection parameters, and create mysql engine
mysql_url = "mysql+pymysql://root:hello@localhost:3306/mysqlDB"
engine = create_engine(mysql_url, echo=True)
SQLModel.metadata.create_all(engine)

# Read the CSV file (PATH) and strip the excess spaces
csv_file_path = 'employees.csv'
df = pd.read_csv(csv_file_path)
