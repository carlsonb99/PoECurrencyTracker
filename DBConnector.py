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

    def __del__(self):
        # Close DB Connection
        print("\nClosing DB Connection...")
        self.conn.close()

    # Conect to requested database
    def connect(self):
        
        try:
            self.conn = mysql.connector.connect(host='localhost', database=self.database, user=self.user, password=self.password)

            if self.conn.is_connected():
                print('Connected to database!')

        except Error as e:
            print('Error: ',e)

    # Insert desired data
    def insert(self,table_info, data):

        try:
            # table_info: [table_name, column_name(s), values_string]
            # data: [values]
            query = "INSERT INTO "+" "+table_info[0]+" "+table_info[1]+" VALUES "+table_info[2]
            
            print('Inserting data into DB...')

            cursor = self.conn.cursor()
            cursor.executemany(query,data)

            self.conn.commit()
            cursor.close()

            print('Data commited!\n')

        except Error as e:
            print('Error: ',e)


    def select():
        print('empty')