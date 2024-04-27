import logging
from pathlib import Path
from typing import Tuple
from fastapi import Body, FastAPI, HTTPException, Response
from pydantic import BaseModel
import sqlite3
import sqlite3
import threading
from fastapi import FastAPI, HTTPException,Form
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def open_db_connection() -> Tuple[
    sqlite3.Connection,
    sqlite3.Cursor,
]:
    """
    Return a cursor to make queries
    """
    try:
        db_connection = sqlite3.connect('customers.db', uri=True)
        db_cursor = db_connection.cursor()
        logger.info("Database created and Successfully Connected to SQLite")
        return db_connection, db_cursor
    except sqlite3.Error as error:
        logger.error("Error while connecting to sqlite: %s", error)
        raise


def execute_query(
    db_cursor: sqlite3.Cursor, query: str, query_params: dict
) -> sqlite3.Cursor:
    """
    Return a cursor with the query result
    """
    try:
        return db_cursor.execute(query, query_params)
    except sqlite3.Error as error:
        logger.error("Error while connecting to sqlite: %s", error)
        raise


def close_db_connection(connection: sqlite3.Connection) -> None:
    """
    Close DB connection
    """
    if connection:
        connection.close()
        logger.info("The SQLite connection is closed")


class Customer(BaseModel):
    id: int
    name: str
    dob: str
    email: str
    adhar_number: str
    registration_date: str
    mobile_number: str
    plan_id: int

class Plan(BaseModel):
    id: int
    name: str
    cost: int
    validity: int
    status: str

sqlite_connection, cursor = open_db_connection()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        dob TEXT,
        email TEXT,
        adhar_number TEXT,
        registration_date TEXT,
        mobile_number TEXT,
        plan_id INTEGER,
        FOREIGN KEY (plan_id) REFERENCES plans (id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS plans (
        id INTEGER PRIMARY KEY,
        name TEXT,
        cost INTEGER,
        validity INTEGER,
        status TEXT
    )
''')

# cursor.execute('''
# INSERT INTO plans (id, name, cost, validity, status)
# VALUES (1, 'Platinum365', 100.00, 365, 'Active'),
#        (2, 'Gold180', 75.00, 180, 'Active'),
#        (3, 'Silver90', 35.00, 90, 'Inactive')
# ''')
 
close_db_connection(sqlite_connection)

@app.get("/plans")
def get_plans():
    sqlite_connection, cursor = open_db_connection()
    logger.info("getting plans list")

    cursor.execute('SELECT * from plans')
    plans = cursor.fetchall()
    
    sqlite_connection.commit()
    close_db_connection(sqlite_connection)

    plans_list = []
    for plan in plans:
        customer_dict = {
            'plan_id': plan[0],
            'plan_name': plan[1],
            "plan_cost": plan[2],
            "plans_validity": plan[3],
            "plans_status": plan[4],
        }
        plans_list.append(customer_dict)

    return plans_list

@app.post("/customers")
def create_customer(customer: Customer):
    sqlite_connection, cursor = open_db_connection()
    logger.info("Creating new customer")

    cursor.execute('''
        INSERT INTO customers (name, dob, email, adhar_number, registration_date, mobile_number, plan_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (customer.name, customer.dob, customer.email, customer.adhar_number, customer.registration_date, customer.mobile_number, customer.plan_id))
    sqlite_connection.commit()

    close_db_connection(sqlite_connection)
    customer.id = cursor.lastrowid
    return customer

@app.get("/customers")
def get_customers():
    sqlite_connection, cursor = open_db_connection()
    logger.info("getting customers list")

    cursor.execute('SELECT customers.id, customers.name, customers.dob, customers.email, customers.adhar_number, customers.registration_date, customers.mobile_number, customers.plan_id, plans.name, plans.cost, plans.validity, plans.status FROM customers JOIN plans ON customers.plan_id = plans.id')
    customers = cursor.fetchall()
    
    sqlite_connection.commit()
    close_db_connection(sqlite_connection)

    customer_list = []
    for customer in customers:
        customer_dict = {
            'id': customer[0],
            'name': customer[1],
            'dob': customer[2],
            'email': customer[3],
            'adhar_number': customer[4],
            'registration_date': customer[5],
            'mobile_number': customer[6],
            'plan_id': customer[7],
            'plan_name': customer[8],
            "plan_cost": customer[9],
            "plans_validity": customer[10],
            "plans_status": customer[11],
        }
        customer_list.append(customer_dict)

    return customer_list

@app.get("/customer/{customer_id}")
def get_customer(customer_id: int):
    sqlite_connection, cursor = open_db_connection()
    logger.info("getting customer info")

    cursor.execute('SELECT customers.id, customers.name, customers.dob, customers.email, customers.adhar_number, customers.registration_date, customers.mobile_number, customers.plan_id, plans.name, plans.cost, plans.validity, plans.status FROM customers JOIN plans ON customers.plan_id = plans.id where customers.id = ?', (customer_id,))
    customers = cursor.fetchall()
    
    sqlite_connection.commit()
    close_db_connection(sqlite_connection)

    customer_list = []
    for customer in customers:
        customer_dict = {
            'id': customer[0],
            'name': customer[1],
            'dob': customer[2],
            'email': customer[3],
            'adhar_number': customer[4],
            'registration_date': customer[5],
            'mobile_number': customer[6],
            'plan_id': customer[7],
            'plan_name': customer[8],
            "plan_cost": customer[9],
            "plans_validity": customer[10],
            "plans_status": customer[11],
        }
        customer_list.append(customer_dict)

    return customer_list[0]


@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    sqlite_connection, cursor = open_db_connection()
    logger.info("getting customers list")
    cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    existing_customer = cursor.fetchone()
    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    cursor.execute('''
        UPDATE customers SET
            name = ?,
            dob = ?,
            email = ?,
            adhar_number = ?,
            registration_date = ?,
            mobile_number = ?,
            plan_id = ?
        WHERE id = ?
    ''', (customer.name, customer.dob, customer.email, customer.adhar_number, customer.registration_date, customer.mobile_number, customer.plan_id, customer_id))
    sqlite_connection.commit()
    close_db_connection(sqlite_connection)
    return customer

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    sqlite_connection, cursor = open_db_connection()
    cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
    sqlite_connection.commit()
    close_db_connection(sqlite_connection)
    return {"message": "Customer deleted"}

@app.put("/customers/{customer_id}/renew")
def renew_plan(customer_id: int, renewal_date: str, plan_status: str):
    sqlite_connection, cursor = open_db_connection()
    cursor.execute('UPDATE customers SET renewal_date = ?, plan_status = ? WHERE id = ?', (renewal_date, plan_status, customer_id))
    sqlite_connection.commit()
    close_db_connection(sqlite_connection)
    cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    customer = cursor.fetchone()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return Customer(**customer)

@app.put("/change_plan")
def change_plan(body: dict = Body(...)):
    logger.info("change_plan...")
    logger.info(body)
    sqlite_connection, cursor = open_db_connection()
    customer_id = body.get('customer_id')
    logger.info(customer_id)
    if customer_id is None:
        raise HTTPException(status_code=400, detail="customer_id is required in the request body")
    plan_id = body.get('plan_id')
    logger.info(plan_id)
    if plan_id is None:
        raise HTTPException(status_code=400, detail="plan_id is required in the request body")
    
    cursor.execute('SELECT * FROM plans WHERE id = ?', (plan_id,))
    plan = cursor.fetchall()
    # return plan
    cursor.execute('UPDATE customers SET plan_id = ? WHERE id = ?', (plan_id, customer_id))
    rows_affected = cursor.rowcount
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    sqlite_connection.commit()
    close_db_connection(sqlite_connection)
    return JSONResponse(status_code=200, content={"message": "Plan changed successfully"})

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

@app.on_event("shutdown")
def shutdown_event():
    if hasattr(threading.current_thread(), "sqlite3_connection"):
        threading.current_thread().sqlite3_connection.close()