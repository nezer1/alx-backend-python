import mysql.connector
import csv
import os
import uuid

# Database configuration
DB_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'
CSV_FILE = 'user_data.csv'

# MySQL connection configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
}

# Connect to MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        print("Connected to MySQL Server")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create database if not exists
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database {DB_NAME} created successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Connect to ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(database=DB_NAME, **MYSQL_CONFIG)
        print(f"Connected to database {DB_NAME}")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create user_data table if not exists
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(10, 2) NOT NULL
            )
        """)
        print(f"Table {TABLE_NAME} created successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Insert data into user_data table
def insert_data(connection, data):
    try:
        cursor = connection.cursor()
        query = f"""
            INSERT INTO {TABLE_NAME} (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(query, data)
        connection.commit()
        print(f"Inserted {cursor.rowcount} rows into {TABLE_NAME}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()

# Read data from CSV file
def read_data_from_csv(file):
    data = []
    with open(file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header
        for row in csvreader:
            user_id = str(uuid.uuid4())
            name = row[0].strip()
            email = row[1].strip()
            age = float(row[2].strip())
            data.append((user_id, name, email, age))
    return data

def main():
    # Connect to MySQL server
    connection = connect_db()
    if not connection:
        return

    # Create database ALX_prodev
    create_database(connection)

    # Connect to ALX_prodev database
    connection = connect_to_prodev()
    if not connection:
        return

    # Create user_data table
    create_table(connection)

    # Read data from CSV
    data = read_data_from_csv(CSV_FILE)

    # Insert data into user_data table
    insert_data(connection, data)

    # Close connection
    connection.close()
    print("MySQL connection closed")

if __name__ == "__main__":
    main()

def stream_users():


import mysql.connector
import csv
import os
import uuid

# Database configuration
DB_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'
CSV_FILE = 'user_data.csv'

# MySQL connection configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
}

# Connect to MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        print("Connected to MySQL Server")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create database if not exists
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database {DB_NAME} created successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Connect to ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(database=DB_NAME, **MYSQL_CONFIG)
        print(f"Connected to database {DB_NAME}")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create user_data table if not exists
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(10, 2) NOT NULL
            )
        """)
        print(f"Table {TABLE_NAME} created successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Insert data into user_data table
def insert_data(connection, data):
    try:
        cursor = connection.cursor()
        query = f"""
            INSERT INTO {TABLE_NAME} (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(query, data)
        connection.commit()
        print(f"Inserted {cursor.rowcount} rows into {TABLE_NAME}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()

# Read data from CSV file
def read_data_from_csv(file):
    data = []
    with open(file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header
        for row in csvreader:
            user_id = str(uuid.uuid4())
            name = row[0].strip()
            email = row[1].strip()
            age = float(row[2].strip())
            data.append((user_id, name, email, age))
    return data

def main():
    # Connect to MySQL server
    connection = connect_db()
    if not connection:
        return

    # Create database ALX_prodev
    create_database(connection)

    # Connect to ALX_prodev database
    connection = connect_to_prodev()
    if not connection:
        return

    # Create user_data table
    create_table(connection)

    # Read data from CSV
    data = read_data_from_csv(CSV_FILE)

    # Insert data into user_data table
    insert_data(connection, data)

    # Close connection
    connection.close()
    print("MySQL connection closed")

if __name__ == "__main__":
    main()
