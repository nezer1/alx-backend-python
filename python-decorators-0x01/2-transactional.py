import sqlite3
import functools

# Decorator to open and close DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(r"C:\Users\nyemi\users.db")  # Adjust the path as needed
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Decorator to wrap the function in a transaction
def transactional(func):
    @functools.wraps(func) #ensures func metadata is remembered
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
    return wrapper

# Function to update email inside a transaction and connection context
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Run the function
update_user_email(user_id=1, new_email="new_email@example.com")
