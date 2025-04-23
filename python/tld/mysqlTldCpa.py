from sqlmodel import Session, Field, SQLModel, create_engine, select, inspect # type: ignore
from sqlalchemy import Table, Column, Integer, ForeignKey # type: ignore
from sqlalchemy.schema import MetaData  # type: ignore
from sqlalchemy.exc import SQLAlchemyError   # type: ignore
from fastapi import FastAPI, Depends, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import Union 
from typing import Optional
import pandas as pd   # type: ignore
from datetime import time
app = FastAPI()

class CPA(SQLModel, table=True):

    user_id: int  = Field(ForeignKey('user.id'), primary_key = True)
    name: str  = Field(default="Unknown")
    
    conversions: int  = Field(default=None)

    total_calls: int  = Field(default=None)
    new_inbound_leads: int = Field(default=None)
    inbound_calls: int  = Field(default=None)
    outbound_calls: int  = Field(default=None)

    conversion_calls: float = Field(default=None)

    # NEED DEFAULT VALUES
    active_time: time = Field(default=None)
    work_length: time  = Field(default=None)
    dispo_length: time = Field(default=None)
    pause_length: time = Field(default=None)
    wait_length: time = Field(default=None)

# MySQL database connection parameters, and create mysql engine
mysql_url = "mysql+pymysql://root:hello@localhost:3306/mysqlDB"
engine = create_engine(mysql_url, echo=True)
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
    print("Session Yielded")

# Get/Read all data in CPA
@app.get("/get-allcpa/", response_model = list[CPA])

def get_cpa(session: Session = Depends(get_session)):

    statement = select(CPA)
    cpa = session.exec(statement).all()

    return cpa

# Get/Read employees' CPA by ID
@app.get("/get-cpa/{user}", response_model = CPA)

def get_employees(user_id: int, session: Session = Depends(get_session)):
    
    cpa_user = session.get(CPA, user_id )

    if cpa_user is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    return cpa_user


# Delete an employees' cpa
@app.delete("/delete-cpa/{user}")

def delete_user(user_id: int, session: Session = Depends(get_session)):
    existing_cpa = session.get(CPA, user_id)
    
    if existing_cpa is None:
        raise HTTPException(status_code = 404, detail="User not found")
    
    session.delete(existing_cpa)
    session.commit()

    return {"detail": "User deleted successfully"}