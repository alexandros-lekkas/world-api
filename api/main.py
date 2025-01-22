from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

DB_PATH = "sqlite/database.sqlite"

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/countries")
def get_countries():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM countries")
    countries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return { "countries": countries }