import sqlite3

# Establish connection to the database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create the students table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    firstname TEXT,
                    lastname TEXT,
                    checkintime TEXT
                )''')

# Add the students to the table
students = [
    (1, 'John', 'Doe', '2021-02-18 16:39:00 UTC'),
    (2, 'Jane', 'Smith', '2021-02-15 19:35:00 UTC')
]
cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?)", students)

# Commit the changes and close the database connection
conn.commit()
conn.close()
