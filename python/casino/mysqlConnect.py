from datetime import time
import math 
import pandas as pd   # type: ignore
from sqlmodel import Session, Field, SQLModel, create_engine, select # type: ignore
from sqlalchemy import MetaData  # type: ignore
from sqlalchemy.schema import MetaData  # type: ignore
from sqlalchemy import Table, Column, Integer # type: ignore
from sqlalchemy.exc import SQLAlchemyError   # type: ignore
from fastapi import FastAPI, Depends, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import Union 
from typing import Optional
# import uvicorn # type: ignore
import pydantic # type: ignore
import numpy as np # type: ignore

# Read the CSV file (PATH) and strip the excess spaces
csv_file_path = 'employees.csv'
df = pd.read_csv(csv_file_path)

#### Do I need this in here?????
# Have to add employeeID == id
class Employee(SQLModel, table=True):   
    id: int = Field(default=None, primary_key=True)
    fullname: str = Field(default=None) 
    firstname: str = Field(default=None) 
    lastname: str = Field(default=None) 
    tldEmail: str = Field(default=None) 
    employment: str = Field(default=None)
    department: str = Field(default=None) 
    manager: str = Field(default=None)


# MySQL database connection parameters  
mysql_url = "mysql+pymysql://root:hello@localhost:3306/mysqlDB"

# Create MySQL engine  
engine = create_engine(mysql_url, echo=True)

# Create the tables in the engine
SQLModel.metadata.create_all(engine)  