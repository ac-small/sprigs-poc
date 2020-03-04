#!/usr/bin/python
from config import config
import psycopg2

def connect():
    """ Connect to the PostgreSQL database server
        Returns cursor and connection """
    connection = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
      
        # create a cursor
        cursor = connection.cursor()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return cursor, connection

def close(cursor, connection):
    """Close the communication with the PostgreSQL"""
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()
        print('Database connection closed.')