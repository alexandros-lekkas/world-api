import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

COUNTRIES_DB_PATH = "sqlite/countries.sqlite3"

def connect_db(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/countries")
def get_countries(skip: int = 0, limit: int = 10):
    conn = connect_db(COUNTRIES_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM countries LIMIT ? OFFSET ?", (limit, skip))
    countries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"countries": countries}