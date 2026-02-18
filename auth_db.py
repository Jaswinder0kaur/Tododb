import mysql.connector

conn = mysql.connector.connect(
    host = " sql12.freesqldatabase.com",
    user = "sql12817373",
    password = "KawrCidaYM",
    database = "sql12817373",
    port = 3306
)

csr = conn.cursor()