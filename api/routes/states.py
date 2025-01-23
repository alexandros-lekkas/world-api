from fastapi import APIRouter, HTTPException, Query

from api.utils.db import connect_db

router = APIRouter()

DB_PATH = "sqlite/states.sqlite3"

@router.get("/states")
def get_states(country_iso2: str = Query(None), page: int = Query(1, ge=1), pageSize: int = Query(10, le=100)):
    """
    Get a list of states with pagination.
    Optionally filter by country ISO2 code.
    """
    offset = (page - 1) * pageSize

    conn = connect_db(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM states")
    total_count = cursor.fetchone()[0]

    if country_iso2:
        cursor.execute("SELECT * FROM states WHERE country_code = ? LIMIT ? OFFSET ?", (country_iso2, pageSize, offset))
    else:
        cursor.execute("SELECT * FROM states LIMIT ? OFFSET ?", (pageSize, offset))

    states = [dict(row) for row in cursor.fetchall()]
    conn.close()

    if not states:
        raise HTTPException(status_code=404, detail="No states found")

    return {
        "page": page,
        "pageSize": pageSize,
        "count": len(states),
        "total_count": total_count,
        "states": states
    }

@router.get("/states/details/{country_iso2}/{state_iso2}")
def get_state_details(country_iso2: str, state_iso2: str):
    """
    Get details of a specific state by its country and state code.
    
    Args:
        country_iso2 (str): The ISO2 code of the country.
        state_iso2 (str): The ISO2 code of the state.
        
    Returns (dict): A dictionary containing the state details.
    """
    conn = connect_db(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM states WHERE country_code = ? AND iso2 = ?",
        (country_iso2, state_iso2)
    )
    state = cursor.fetchone()

    conn.close()

    if not state:
        raise HTTPException(status_code=404, detail="State not found")

    return dict(state)
