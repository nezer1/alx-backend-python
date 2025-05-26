
import mysql.connector

def stream_user_ages():
    """Generator that yields user ages one by one."""
    connection = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # Loop 1 (single loop over cursor)
        yield age

    cursor.close()
    connection.close()


def compute_average_age():
    """Computes and prints the average age using a generator."""
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop 2
        total_age += age
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")


# Run the function
compute_average_age()
