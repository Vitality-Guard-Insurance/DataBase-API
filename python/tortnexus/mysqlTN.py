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

# MySQL database connection parameters  
mysql_user = "root"
mysql_password = "hello"
mysql_host = "localhost"
mysql_port = "3306"
mysql_database = "mysqlDB" # database name 

# MySQL connection URL
# Public Retrival is to allow to get the password
# mysql_url = "mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}" # ?allowPublicKeyRetrieval=True"
mysql_url = "mysql+pymysql://root:hello@localhost:3306/mysqlDB"
engine = create_engine(mysql_url, echo=True) # MySQL engine/instance

# Read the CSV file (PATH) and strip the excess spaces
csv_file_path = 'employees.csv' 
df = pd.read_csv(csv_file_path)