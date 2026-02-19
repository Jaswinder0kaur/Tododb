import mysql.connector
from mysql.connector import pooling

# ---------- CONNECTION POOL (VERY IMPORTANT) ----------
dbconfig = {
    "host": "sql12.freesqldatabase.com",   # removed space
    "user": "sql12817373",
    "password": "KawrCidaYM",
    "database": "sql12817373",
    "port": 3306,
    "connection_timeout": 28800,  # 8 hours
    "autocommit": True
}

# Create pool (prevents disconnect)
pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **dbconfig
)

def get_connection():
    return pool.get_connection()

conn = get_connection()
csr = conn.cursor(buffered=True)


# ---------- AUTO RECONNECT ----------
def reconnect():
    global conn, csr
    try:
        conn.ping(reconnect=True, attempts=3, delay=2)
    except:
        conn = get_connection()
        csr = conn.cursor(buffered=True)
