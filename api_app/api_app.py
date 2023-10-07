from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Initialize the connection to the database
connection = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_username",
    password="your_password"
)

# Create a cursor object
cursor = connection.cursor()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}

@app.get("/items/")
def get_items():
    # Execute SQL query to fetch data
    cursor.execute("SELECT * FROM your_table_name")
    
    # Fetch all rows from the last executed query
    items = cursor.fetchall()
    
    return {"items": items}