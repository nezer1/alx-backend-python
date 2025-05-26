

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    
    # SQL does the filtering!
    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Process batches and filter users older than 25."""
    for batch in stream_users_in_batches(batch_size):  # 1st loop
        filtered_users = [user for user in batch if user[3] > 25]  # 2nd loop (list comp is a loop)
        yield filtered_users  # Yield filtered batch
