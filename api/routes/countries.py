from fastapi import APIRouter, HTTPException

from utils.db import connect_db

router = APIRouter()

DB_PATH = "sqlite/countries.sqlite3"

@router.get("/countries")
def get_countries()