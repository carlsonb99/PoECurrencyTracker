import datetime as dt
import mysql.connector
from mysql.connector import Error


# Class for manipulating DB

class DBConnector:

    def __init__(self, database, user, password):
        self.conn = None
        self.database = database
        self.user = user
        self.password = password

    # Conect to requested database
    def connect():
    try:
        conn = mysql.connector.connect(
            host='localhost', database=self.database, user=self.user, password=self.password)

    if conn.is_connected():
        print('Connected to database...\n')

    except Error as e:
        print(e)

    # Insert desired data
    def insert(table_info, data):

        # table_info: [table_name, column_name(s), values_string]
        # data: [values]
        query = "INSERT INTO "+table_info[0]+"("+table_info[1]+") VALUES("+table_info[2]")"
        
        cursor = conn.cursor()
        cursor.executemany(query,data)

    def select():