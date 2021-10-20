import sqlite3
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn

def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM portfolio")
    print([i[0] for i in cur.description])
    rows = cur.fetchall()

    for row in rows:
        value=float(row[1])*float(row[2])
        print(row[0],value)
    
    
conn=create_connection('rasadb')
select_all_tasks(conn)