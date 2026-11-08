import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="occupancy_db",
        user="occupancy_user",
        password=os.environ["POSTGRES_PASSWORD"],
    )