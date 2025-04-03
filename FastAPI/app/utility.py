from app.config import DATABASE_URL

import psycopg2
from urllib.parse import urlparse

def initDB_cnxn():

    url = urlparse(DATABASE_URL)
    
    cnxn = psycopg2.connect(
        dbname=url.path[1:],  # Exclude the leading '/'
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    return cnxn 