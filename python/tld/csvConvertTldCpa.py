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
import numpy as np  # type: ignore Import numpy for NaN checking

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

    active_time: time = Field(default=None)
    work_length: time  = Field(default=None)
    dispo_length: time = Field(default=None)
    pause_length: time = Field(default=None)
    wait_length: time = Field(default=None)

# MySQL database connection parameters  
mysql_url = "mysql+pymysql://root:hello@localhost:3306/mysqlDB"  
engine = create_engine(mysql_url, echo=True)  
SQLModel.metadata.create_all(engine)  

# Read the CSV file  
csv_file_path = 'cpa.csv'  
df = pd.read_csv(csv_file_path)  

# Replace NaN values with None   
df = df.where(pd.notnull, None)
df = df.where(pd.notna, None)


def seconds_to_time(seconds: Optional[int]) -> Optional[time]:  
    if seconds is None:  
        return None  
    if seconds < 0:  # Prevent negative seconds, adjust according to your logic  
        return None
    return time(hour=seconds // 3600, minute=(seconds // 60) % 60, second=seconds % 60)  

def sanitize_value(value: Optional[float]) -> float:  
    """Ensure that the value is not -inf, inf, or NaN, returning a valid number."""  
    if value in [float('-inf'), float('inf')] or (isinstance(value, float) and np.isnan(value)):  
        return 0.0  # Ensure that invalid values are replaced with a default numerical value  
    print("conversion calls",value)
    return value  

with Session(engine) as session:  
    try:  
        for index, row in df.iterrows():  
            cpa = CPA(  
                user_id=row.get('user', None),  
                name=row.get('name', 'Unknown'),  
                conversions=row.get('conversions', None),  
                total_calls=row.get('total_calls', None),  
                new_inbound_leads=row.get('new_inbound_leads', None),  
                inbound_calls=row.get('inbound_calls', None),  
                outbound_calls=row.get('outbound_calls', None),  

                conversion_calls=sanitize_value(row.get('conversion_calls', None)), 

                active_time=seconds_to_time(row.get('active_length_in_sec')),  
                work_length=seconds_to_time(row.get('work_length_in_sec')),  
                dispo_length=seconds_to_time(row.get('dispo_length_in_sec')),  
                pause_length=seconds_to_time(row.get('pause_length_in_sec')),  
                wait_length=seconds_to_time(row.get('wait_length_in_sec'))  
            )  

            session.add(cpa)  

        session.commit()  
        print("Committed")  

    except Exception as e:  
        print(f"Error occurred: {e}")  
        session.rollback()  