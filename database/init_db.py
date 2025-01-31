import sqlite3

conn = sqlite3.connect('database/careconnect.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    security_question TEXT NOT NULL,
    security_answer TEXT NOT NULL,
    language TEXT NOT NULL
)
''')

# Create doctors table
cursor.execute('''
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialist TEXT NOT NULL,
    email TEXT NOT NULL,
    mobile TEXT NOT NULL
)
''')

# Insert sample users
cursor.executemany('''
INSERT INTO users (username, name, mobile, email, password, security_question, security_answer, language)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', [
    ('user_1234567890', 'John Doe', '1234567890', 'john@example.com', 'password123', 'What is your pet’s name?', 'Fluffy', 'English'),
    ('user_0987654321', 'Jane Smith', '0987654321', 'jane@example.com', 'password456', 'What is your favorite color?', 'Blue', 'Hindi')
])

# Insert sample doctors
cursor.executemany('''
INSERT INTO doctors (name, specialist, email, mobile)
VALUES (?, ?, ?, ?)
''', [
    ('Dr. Alice', 'Cardiologist', 'alice@example.com', '1111111111'),
    ('Dr. Bob', 'Dermatologist', 'bob@example.com', '2222222222')
])

conn.commit()
conn.close()
