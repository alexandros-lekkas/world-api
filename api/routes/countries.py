from fastapi import APIRouter, HTTPException, Query

from utils.db import connect_db

router = APIRouter()

DB_PATH = "sqlite/countries.sqlite3"

@router.get("/countries")
def get_countries(page: int = Query(1, ge=1),
                  pageSize: int = Query(10, le=100)):
    """
    Get a list of countries with pagination.
    
    Args:
        page (int): The page number.
        pageSize (int): The number of countries per page.
        
    Returns (dict): A dictionary containing a list of countries.
    """
    offset = (page - 1) * pageSize
    
    conn = connect_db(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM countries LIMIT ? OFFSET ?", (pageSize, offset))
    countries = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        "page": page,
        "pageSize": pageSize,
        "totalCount": len(countries),
        "countries": countries
    }
    
@router.get("/countries/{iso2}")
def get_country_details(iso2: str):
    """
    Get details of a specific country.
    
    Args:
        iso2 (str): The ISO2 code of the country.
        
    Returns (dict): A dictionary containing the details of the country.
    """
    conn = connect_db(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM countries WHERE iso2 = ?", (iso2,))
    country = cursor.fetchone()
    
    conn.close()
    
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    return dict(country)
