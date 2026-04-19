# Importing required libraries
import MySQLdb
import os
import MySQLdb.cursors

# Function to connect to MySQL database
def connect():
    # Get environment variables
    MYSQL_HOST = os.getenv("MYSQL_HOSTNAME")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_NAME = os.getenv("MYSQL_NAME")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    
    # Connect to MySQL database and return connection object
    try:
        conn = MySQLdb.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            db=MYSQL_NAME,
            port=int(MYSQL_PORT),
            charset="utf8mb4",
            cursorclass=MySQLdb.cursors.DictCursor
        )
        
        # Return connection object
        return conn
    
    # Handle exception
    except Exception as ex:
        print(ex)
        return None