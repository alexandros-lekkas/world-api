from fastapi import APIRouter, HTTPException, Query
from api.utils.db import connect_db

router = APIRouter()

DB_PATH = "sqlite/cities.sqlite3"

@router.get("/cities")
def get_cities(country_iso2: str = Query(None), state_iso2: str = Query(None), page: int = Query(1, ge=1), pageSize: int = Query(10, le=100)):
    """
    Get a list of cities with pagination.
    Optionally filter by country ISO2 code and state ISO2 code.
    """
    offset = (page - 1) * pageSize

    conn = connect_db(DB_PATH)
    cursor = conn.cursor()

    if country_iso2 and state_iso2:
        cursor.execute("SELECT * FROM cities WHERE country_code = ? AND state_code = ? LIMIT ? OFFSET ?", (country_iso2, state_iso2, pageSize, offset))
    elif country_iso2:
        cursor.execute("SELECT * FROM cities WHERE country_code = ? LIMIT ? OFFSET ?", (country_iso2, pageSize, offset))
    else:
        cursor.execute("SELECT * FROM cities LIMIT ? OFFSET ?", (pageSize, offset))

    cities = [dict(row) for row in cursor.fetchall()]
    conn.close()

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")

    return {
        "page": page,
        "pageSize": pageSize,
        "totalCount": len(cities),
        "cities": cities
    }
