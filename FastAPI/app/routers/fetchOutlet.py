from fastapi import APIRouter
from app.utility import initDB_cnxn

import psycopg2

router = APIRouter(
    prefix="/fetchOutlet",
    tags=["fetchOutlet"]
)

@router.get("/")
def get():
    cnxn = initDB_cnxn()
    result = getRestaurant(cnxn)
    return result 

def getRestaurant(cnxn):

    cur = cnxn.cursor()
    cur.execute("SELECT * FROM RestaurantGet();")
    rows = cur.fetchall()

    result = []
    for index, row in enumerate(rows):
        result.append({
            "id": index,
            "name": row[0],
            "address": row[1],
            "lat": row[2],
            "lng": row[3],
            "waze_url": row[4],
            "radius": 5000
        })

    cur.close()

    return result