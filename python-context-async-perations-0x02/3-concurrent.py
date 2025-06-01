import aiosqlite
import asyncio

DB_PATH = "users.db"  # adjust the path if needed

# Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All users:")
            for user in users:
                print(user)
            return users

# Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("\nUsers older than 40:")
            for user in older_users:
                print(user)
            return older_users

# Concurrent execution
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Run the event loop
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
