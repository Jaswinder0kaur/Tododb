import mysql.connector

dbconfig = {
    "host": "sql12.freesqldatabase.com",
    "user": "sql12817373",
    "password": "KawrCidaYM",
    "database": "sql12817373",
    "port": 3306
}

def get_connection():
    return mysql.connector.connect(**dbconfig)


