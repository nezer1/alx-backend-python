import sqlite3

class ExecuteQuery:
    def __init__(self, db_path, query, params=None):
        self.db_path = db_path
        self.query = query
        self.params = params or ()
        self.conn = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        if exc_type:
            print("An error occurred:", exc_val)
        # Returning False lets exceptions propagate
        return False
    


query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(r"C:\Users\nyemi\users.db", query, params) as results:
    for row in results:
        print(row)