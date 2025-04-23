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


# MySQL database connection parameters  
mysql_user = "root"
mysql_password = "hello"
mysql_host = "localhost"
mysql_port = "3306"
mysql_database = "mysqlDB" # database name 

# # MySQL connection URL
# # Public Retrival is to allow to get the password
# # mysql_url = "mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}" # ?allowPublicKeyRetrieval=True"
# mysql_url = "mysql+pymysql://root:hello@localhost:3306/mysqlDB"
# engine = create_engine(mysql_url, echo=True) # MySQL engine/instance

# Read the CSV file (PATH) and strip the excess spaces
csv_file_path = 'employees.csv'
df = pd.read_csv(csv_file_path)

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

# Create a MySQL engine  
engine = create_engine(mysql_url, echo=True)

# Default values for required fields to avoid integrity errors
DEFAULT_EMAIL = 'unknown@example.com'
DEFAULT_MANAGER = 'Not Assigned'

with Session(engine) as session:
    try:
        for index, row in df.iterrows(): # userID == employeeID need to add this
            employee = Employee(
                fullname=row.get('Full Name', 'Unknown'),
                firstname=row.get('First', 'Unknown'),
                lastname=row.get('Last', 'Unknown'),
                tldEmail=row.get('Email TLD', DEFAULT_EMAIL),
                employment=row.get('Employment', 'Unknown'),
                department=row.get('Department', 'Unknown'),
                manager=row.get('Manager', DEFAULT_MANAGER)
            )

            # print(f'Manager Value Before Insert: {employee.manager}')
            session.add(employee)
            print("Employee {employee} added")

        session.commit()
        print("Committed")
        print(f"Inserted {len(df)} employees.")  

    # In case of error, roll back the session
    except Exception as e:
        print(f"Error occurred: {e}")
        session.rollback()

# APIs ##

app = FastAPI()
def get_session():
    with Session(engine) as session:
        yield session
    print("Session Yielded")

# Read all Employees (see if this works in order to see all of the employees)
@app.get("/allemployees/", response_model = list[Employee])

def get_allemployees(session: Session = Depends(get_session)):

    # query to select all employees
    employee = session.exec(select(Employee)).all()

    return employee

# # # Read Employees by ID
@app.get("/employees/{user}", response_model = Employee)

def get_employees(employeeID: Employee, session: Session = Depends(get_session)):
    employee_user = session.get(Employee, employeeID)

    if employee_user is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    return employee_user

# Create an Employee
@app.post("/create-employee/", response_model = Employee)

def create_employee(employeeID: Employee, session: Session = Depends(get_session)):
    session.add(employee)
    session.commit()
    session.refresh(employee)

    return employee

# Update an Employee
@app.put("/employee/{user}", response_model = Employee)

def update_employees(employeeID: int, employee = Employee, session: Session = Depends(get_session)):
    existing_employee = session.get(Employee, employeeID)

    if existing_employee is None:
        raise HTTPException(status_code = 404, detail="User not found")
   
    existing_employee.fullname = employee.fullname
    existing_employee.tldEmail = employee.tldEmail
    session.commit()
    session.refresh(existing_employee)

    return existing_employee

# Delete an Employee
@app.delete("/employeesall/{user}")

def delete_user(employeeId: int, session: Session = Depends(get_session)):
    existing_employee = session.get(Employee, employeeId)
    
    if existing_employee is None:
        raise HTTPException(status_code = 404, detail="User not found")
    
    session.delete(existing_employee)
    session.commit()

    return {"detail": "User deleted successfully"}

# Delete all tables (if you want to start fresh)
# @app.delete_tables("/delete-alltables/")

# def delete_tables():
#     SQLModel.metadata.drop_all(engine)
#     print("All tables deleted.")  

# # Delete 1 or multiple tables
# @app.delete_table("/delete-table/")

# def delete_table():
#     SQLModel.metadata
#     print("Table deleted")




# Optional: Drop existing tables (if you want to start fresh)
# def drop_tables():  
#     SQLModel.metadata.drop_all(engine)
#     print("All tables dropped.")  
# drop_tables()

# def drop_tables():  
#     try:  
#         # Drop all tables defined in the metadata  
#         SQLModel.metadata.drop_all(engine)  
#         print("All tables dropped.")  
#     except SQLAlchemyError as e:  
#         # Handle exceptions and print errors  
#         print(f"Error occurred while dropping tables: {e}")  
# drop_tables()
# SQLModel.metadata.create_all(engine)

# # Call the drop_tables function  
# if __name__ == "__main__":  
#     drop_tables()  

#     # Optional: Create tables after dropping to reset the schema  
#     SQLModel.metadata.create_all(engine)  