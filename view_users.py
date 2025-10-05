import sqlite3

# Connect to the database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Fetch all users
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# Print column names
col_names = [description[0] for description in cursor.description]
print(" | ".join(col_names))

# Print user data
for row in rows:
    print(row)

conn.close()
