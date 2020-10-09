import mysql.connector as conn

from src import config

db = conn.connect(
    host=config.HOST,
    user=config.USER,
    password=config.PASSWORD,
    database=config.DATABASE
)
db_cursor = db.cursor()
