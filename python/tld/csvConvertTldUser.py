from sqlmodel import Session, Field, SQLModel, create_engine, select, inspect # type: ignore
from sqlalchemy import Table, Column, Integer # type: ignore
from sqlalchemy.schema import MetaData  # type: ignore
from sqlalchemy.exc import SQLAlchemyError   # type: ignore
from fastapi import FastAPI, Depends, HTTPException # type: ignore
from typing import Union 
from typing import Optional, List
from datetime import datetime, time
import pandas as pd # type: ignore

class Employees(SQLModel, table=True):

    # A unique identifier for each employee.
    # The employee's current status (e.g., Active).
    # The employee's name.
    # The employee's login credentials.
    # The employee's role and agency.
    # States where the employee is licensed (if applicable).
    # Key dates in the employee's record.
    # Additional group affiliations for the employee.
    user_id: int = Field(default=None, primary_key=True)

    status: str = Field(default=None)

    full_name: str = Field(default=None)
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)

    username: str = Field(default=None)
    email: str = Field(default=None)

    role_descriptions: str = Field(default='Unknown')
    agency_description: str = Field(default='Unknown')
    group_descriptions: str = Field(default='Unknown')

    licensed_states: str = Field(default='Unknown')

    date_created: datetime = Field(default=None)
    date_activated: datetime = Field(default=None)
    date_modified: datetime = Field(default=None)
    date_deactivated: datetime = Field(default=None)

# MySQL database connection parameters, and create mysql engine
mysql_url = "mysql+pymysql://root:hello@localhost:3306/mysqlDB"
engine = create_engine(mysql_url, echo=True)
SQLModel.metadata.create_all(engine)

# Read the CSV file (PATH) and strip the excess spaces
csv_file_path = 'users.csv'
df = pd.read_csv(csv_file_path)

# Replace NaN values with None  
df = df.where(pd.notnull(df), None)

with Session(engine) as session:
    try:
        for index, row in df.iterrows():
            # Clean datetime fields  
            date_activated = row.get('date_activated')  
            date_created = row.get('date_created')  
            date_modified = row.get('date_modified')  
            date_deactivated = row.get('date_deactivated')  

            # Replace '0000-00-00 00:00:00' with None  
            date_activated = None if date_activated == '0000-00-00 00:00:00' else date_activated  
            date_created = None if date_created == '0000-00-00 00:00:00' else date_created  
            date_modified = None if date_modified == '0000-00-00 00:00:00' else date_modified  
            date_deactivated = None if date_deactivated == '0000-00-00 00:00:00' else date_deactivated  

            employee = Employees(
                user_id=row.get('user_id', 'Unknown'),
                
                status=row.get('status', 'Unknown'),
                
                full_name=row.get('full_name', 'Unknown'),
                first_name=row.get('first_name', 'Unknown'),
                last_name=row.get('last_name', 'Unknown'),
                
                username=row.get('username', 'Unknown'),
                email=row.get('email', 'Unknown'),

                role_descriptions=row.get('role_descriptions', 'Unknown'),
                agency_description=row.get('agency_description', 'Unknown'),
                group_descriptions=row.get('group_descriptions', 'Unknown'),

                licensed_states=row.get('licensed_states', 'Unknown'),

                date_created=date_created,  
                date_activated=date_activated,  
                date_modified=date_modified,  
                date_deactivated=date_deactivated
            )

            session.add(employee)
            # print("Employee {employee} added")

        session.commit()
        # print("Committed")
        # print(f"Inserted {len(df)} employees.")

    # In case of error, roll back the session
    except Exception as e:
        print(f"Error occurred: {e}")
        session.rollback()