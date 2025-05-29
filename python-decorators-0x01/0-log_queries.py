import sqlite3
from datetime import datetime

#### decorator to log SQL queries

def log_queries(func):
    # import logging
    # logging.basicConfig(filename='{}.log'.format(func.__name__), level=logging.INFO)
    
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        with open('queries.log', 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] Executing SQL query: {query}\n")
        return(func(*args, **kwargs))
    return wrapper






@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect(r"C:\Users\nyemi\users")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query='SELECT * FROM users')


# import sqlite3

# conn = sqlite3.connect(r"C:\Users\nyemi\users.db")
# cursor = conn.cursor()

# cursor.execute("PRAGMA database_list;")
# for row in cursor.fetchall():
#     print(row)

# conn.close()