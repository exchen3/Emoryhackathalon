import sqlite3
import getpass
import hashlib

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create a users table (run this once to set up the table)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password_hash TEXT
)
""")
conn.commit()

# Function to hash passwords (basic SHA-256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Login process
username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")
hashed_pw = hash_password(password)

# Check credentials
cursor.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, hashed_pw))
user = cursor.fetchone()

if user:
    print(f"\n✅ Login successful! Welcome, {username}.")
else:
    print("\n❌ Login failed. Invalid username or password.")

conn.close()
