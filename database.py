# import sqlite3

# connection = sqlite3.connect("database.db")

# cursor = connection.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS messages(
#     id INTEGER PRIMARY KEY,
#     name TEXT,
#     email TEXT,
#     message TEXT
# )
# """)

# connection.commit()

# print("Table created successfully!")

# connection.close()
###############################################################

import sqlite3

# Connect to the database
connection = sqlite3.connect("database.db")

# Create a cursor object
cursor = connection.cursor()

# Create the messages table
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT
)
""")

# Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Save changes
connection.commit()

print("Tables created successfully!")

# Close the connection
connection.close()