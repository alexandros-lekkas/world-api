from fastapi import APIRouter, HTTPException, Query

from api.utils.db import connect_db

router = APIRouter()

DB_PATH = "sqlite/states.sqlite3"

@router.get("/states")
def get_states(page: int = Query(1, ge=1),
               pageSize: int = Query(10, le=100)):
    """
    Get a list of states with pagination.
    
    Args:
        page (int): The page number.
        pageSize (int): The number of states per page.
        
    Returns (dict): A dictionary containing a list of states.
    """
    offset = (page - 1) * pageSize

    conn = connect_db(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM states LIMIT ? OFFSET ?", (pageSize, offset))
    states = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "page": page,
        "pageSize": pageSize,
        "totalCount": len(states),
        "states": states
    }


@router.get("/states/{country_iso2}")
def get_states_by_country(country_iso2: str):
    """
    Get all states for a specific country.
    
    Args:
        country_iso2 (str): The ISO2 code of the country.
        
    Returns (dict): A dictionary containing the list of states.
    """
    conn = connect_db(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM states WHERE country_iso2 = ?", (country_iso2,))
    states = [dict(row) for row in cursor.fetchall()]

    conn.close()

    if not states:
        raise HTTPException(status_code=404, detail="No states found for this country")

    return {"states": states}


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

    cursor.execute("SELECT * FROM states WHERE code = ?", (state_code,))
    state = cursor.fetchone()

    conn.close()

    if not state:
        raise HTTPException(status_code=404, detail="State not found")

    return dict(state)
