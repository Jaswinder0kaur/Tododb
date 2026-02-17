import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "WJ28@krhps",
    database = "streamlitproject"
)

csr = conn.cursor()