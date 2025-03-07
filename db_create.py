import psycopg2
from loguru import logger
from config import host,user,password,db_name

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name,
)

# connection.autocommit = True

with connection.cursor() as cursor:
    cursor.execute(
        """CREATE TABLE metatest(
            id serial PRIMARY KEY,
            hero varchar(30) NOT NULL,
            matches varchar(30) NOT NULL);"""
    )
    logger.info(f"Table created: {cursor.fetchone()}")