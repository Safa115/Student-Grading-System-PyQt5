import sqlite3

# Connect to the database (it will be created if it doesn't exist)
conn = sqlite3.connect("student_grading.db")
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON")

# Create Student table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    credit_hours INTEGER DEFAULT 0
)
""")

# Create Instructor table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Instructor (
    instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")

# Create Course table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    credit_hours INTEGER NOT NULL,
    instructor_id INTEGER,
    FOREIGN KEY (instructor_id) REFERENCES Instructor(instructor_id)
)
""")

# Create Grade table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Grade (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    grade_value REAL,
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
)
""")

# Save changes and close connection
conn.commit()
conn.close()

print("Database and tables created successfully!")
