import sqlite3

def get_database_list():

    conn = sqlite3.connect("anime_database.db")

    c = conn.cursor()

    c.execute("SELECT * FROM list")

    conn.commit()


    return c.fetchall()
def get_database_latest():

    conn = sqlite3.connect("anime_database.db")

    c = conn.cursor()

    c.execute("SELECT * FROM latest")

    conn.commit()
    
    return c.fetchall()
