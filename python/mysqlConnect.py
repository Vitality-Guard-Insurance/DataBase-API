from sqlmodel import Session, Field, SQLModel, create_engine, select, inspect # type: ignore
from sqlalchemy import Table, Column, Integer # type: ignore
from sqlalchemy.schema import MetaData  # type: ignore
from sqlalchemy.exc import SQLAlchemyError   # type: ignore
from fastapi import FastAPI, Depends, HTTPException # type: ignore
from typing import Union 
from typing import Optional, List
from datetime import datetime, time
import pandas as pd # type: ignore

# MySQL database connection parameters, and create mysql engine
mysql_url = "mysql+pymysql://root:hello@localhost:3306/mysqlDB"
engine = create_engine(mysql_url, echo=True)
SQLModel.metadata.create_all(engine)