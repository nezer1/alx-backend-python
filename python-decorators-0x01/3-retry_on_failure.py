import time
import sqlite3
import functools

#### with_db_connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(r"C:\Users\nyemi\users.db")  # Adjust the path as needed
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

#### retry_on_failure decorator
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        print("All retries failed.")
                        raise
        return wrapper
    return decorator

#### decorated function
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### run
users = fetch_users_with_retry()
print(users)