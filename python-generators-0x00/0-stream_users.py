import mysql.connector

def stream_users():
    connection = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='ALX_prodev'
    )
    cursor = connection.cursor()  # return rows as dicts

    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row  # yield one row at a time

    cursor.close()
    connection.close()
