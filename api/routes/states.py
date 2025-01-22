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
        "totalCount": len(states),
        "states": states
    }

@router.get("/states/details/{state_code}")
def get_state_details(state_code: str):
    """
    Get details of a specific state.
    
    Args:
        state_code (str): The state code.
        
    Returns (dict): A dictionary containing the state details.
    """
    conn = connect_db(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM states WHERE id = ?", (state_code,))
    state = cursor.fetchone()

    conn.close()

    if not state:
        raise HTTPException(status_code=404, detail="State not found")

    return dict(state)
