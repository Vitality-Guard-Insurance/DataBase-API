from sqlmodel import Session, Field, SQLModel, create_engine, select, inspect # type: ignore
from sqlalchemy import Table, Column, Integer # type: ignore
from sqlalchemy.schema import MetaData  # type: ignore
from sqlalchemy.exc import SQLAlchemyError   # type: ignore
from fastapi import FastAPI, Depends, HTTPException # type: ignore
from typing import Union 
from typing import Optional, List
from datetime import datetime, time
import pandas as pd # type: ignore
app = FastAPI()

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

# Only allow these items to be updated
class EmployeeUpdate(SQLModel):
    status: Optional[str] = None

    full_name: Optional[str] = None  
    first_name: Optional[str] = None  
    last_name: Optional[str] = None

    username: Optional[str] = None
    email: Optional[str] = None  
    
    role_descriptions: Optional[str] = None  
    agency_description: Optional[str] = None  
    group_descriptions: Optional[str] = None 
    
    licensed_states: Optional[str] = None  
    
    date_activated: Optional[datetime] = None  
    date_modified: Optional[datetime] = None  
    date_deactivated: Optional[datetime] = None  

# MySQL database connection parameters, and create mysql engine
mysql_url = "mysql+pymysql://root:hello@localhost:3306/mysqlDB"
engine = create_engine(mysql_url, echo=True)
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
    print("Session Yielded")

# Create/Post an employee
@app.post("/create-employee/", response_model=Employees)

def create_employee(employee: Employees, session: Session = Depends(get_session)):
        
    session.add(employee)
    print("New employee has been created")
        
    return employee

# Read/Get all emoloyees
@app.get("/get-allemployees/", response_model = list[Employees])

def get_allemployees(session: Session = Depends(get_session)):
    
    statement = select(Employees)
    employees = session.exec(statement).all()

    return employees

# Read/Get employee by user_id
# How to query more than one employee?
@app.get("/get-employee/{user_id}", response_model = Employees)

def get_employees(user_id: int, session: Session = Depends(get_session)):

    employee = session.get(Employees, user_id)
    
    if employee is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    return employee

# Update/Put employee by user_id
# How to update more than one employee?
@app.put("/update-employee/{user_id}", response_model=Employees)  

def update_employees(user_id: int, employee: EmployeeUpdate, session: Session = Depends(get_session)):  
    
    existing_employee = session.get(Employees, user_id)

    if existing_employee is None:  
        raise HTTPException(status_code=404, detail="User not found")  
    
    if existing_employee is not None:

        existing_employee.status = employee.status

        existing_employee.full_name = employee.full_name
        existing_employee.first_name = employee.first_name  
        existing_employee.last_name = employee.last_name

        existing_employee.username = employee.username  
        existing_employee.email = employee.email

        existing_employee.role_descriptions = employee.role_descriptions
        existing_employee.agency_description = employee.agency_description
        existing_employee.group_descriptions = employee.group_descriptions

        existing_employee.licensed_states = employee.licensed_states

        existing_employee.date_activated = employee.date_activated 
        existing_employee.date_modified = employee.date_modified  
        existing_employee.date_deactivated = employee.date_deactivated 

    session.commit()
    # session.flush() # will flush changes to the database
    session.refresh(existing_employee)  

    return existing_employee

# Delete an Employee
# How to delete more than one employee
@app.delete("/delete-employee/{user}", response_model = dict)

def delete_user(user_id: int, session: Session = Depends(get_session)):

    existing_employee = session.get(Employees, user_id)

    if existing_employee is None:
        raise HTTPException(status_code = 404, detail="User not found")
    
    session.delete(existing_employee)
    session.commit()

    return {"detail": "User deleted successfully"}
