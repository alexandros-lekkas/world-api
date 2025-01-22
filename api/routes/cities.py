from fastapi import APIRouter, HTTPException, Query
from api.utils.db import connect_db

router = APIRouter()

DB_PATH = "sqlite/cities.sqlite3"

@router.get("/cities")
def get_cities(page: int = Query(1, ge=1),
               pageSize: int = Query(10, le=100)):
    """
    Get a list of cities with pagination.
    
    Args:
        page (int): The page number.
        pageSize (int): The number of cities per page.
        
    Returns (dict): A dictionary containing a list of cities.
    """
    offset = (page - 1) * pageSize

    conn = connect_db(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cities LIMIT ? OFFSET ?", (pageSize, offset))
    cities = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "page": page,
        "pageSize": pageSize,
        "totalCount": len(cities),
        "cities": cities
    }

@router.get("/cities/{state_code}")
def get_cities_by_state(state_code: str, page: int = Query(1, ge=1),
                        pageSize: int = Query(10, le=100)):
    """
    Get cities in a specific state with pagination.
    
    Args:
        state_code (str): The state code.
        page (int): The page number.
        pageSize (int): The number of cities per page.
        
    Returns (dict): A dictionary containing the cities in the state.
    """
    offset = (page - 1) * pageSize

    conn = connect_db(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM cities WHERE state_code = ? LIMIT ? OFFSET ?", 
        (state_code, pageSize, offset)
    )
    cities = [dict(row) for row in cursor.fetchall()]

    conn.close()

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found for this state")

    return {
        "page": page,
        "pageSize": pageSize,
        "cities": cities
    }

@router.get("/cities/by-country/{country_iso2}")
def get_cities_by_country(country_iso2: str, page: int = Query(1, ge=1),
                          pageSize: int = Query(10, le=100)):
    """
    Get cities in a specific country with pagination.
    
    Args:
        country_iso2 (str): The ISO2 code of the country.
        page (int): The page number.
        pageSize (int): The number of cities per page.
        
    Returns (dict): A dictionary containing the cities in the country.
    """
    offset = (page - 1) * pageSize

    conn = connect_db(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM cities WHERE country_code = ? LIMIT ? OFFSET ?", 
        (country_iso2, pageSize, offset)
    )
    cities = [dict(row) for row in cursor.fetchall()]

    conn.close()

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found for this country")

    return {
        "page": page,
        "pageSize": pageSize,
        "cities": cities
    }
