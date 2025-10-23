import sqlite3

# Open a connection to the database
conn = sqlite3.connect("student_grading.db")
cursor = conn.cursor()

# Add a new column "gpa" if it doesn't exist
try:
    cursor.execute("ALTER TABLE Student ADD COLUMN gpa REAL DEFAULT 0.0;")
    print("Column 'gpa' added successfully ")
except sqlite3.OperationalError as e:
    print("The column might already exist:", e)

# Commit changes and close the connection
conn.commit()
conn.close()
