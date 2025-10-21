import sqlite3

# Connect to the database (it will be created if it doesn't exist)
conn = sqlite3.connect("student_grading.db")
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON")

# ---------- Insert sample data into Instructor table ----------
instructors = [
    ("Dr. Sarah Ahmed", "sarah@univ.edu"),
    ("Dr. Omar Hassan", "omar@univ.edu"),
    ("Dr. Lina Youssef", "lina@univ.edu")
]
cursor.executemany("INSERT INTO Instructor (name, email) VALUES (?, ?)", instructors)

# ---------- Insert sample data into Student table ----------
students = [
    ("Safa Abdelkarim", "safa@student.com", 12),
    ("Ali Mohamed", "ali@student.com", 9),
    ("Nour Hassan", "nour@student.com", 15)
]
cursor.executemany("INSERT INTO Student (name, email, credit_hours) VALUES (?, ?, ?)", students)

# ---------- Insert sample data into Course table ----------
courses = [
    ("Python Programming", 3, 1),
    ("Data Science", 3, 1),
    ("Database Systems", 3, 2),
    ("Machine Learning", 4, 3)
]
cursor.executemany("INSERT INTO Course (name, credit_hours, instructor_id) VALUES (?, ?, ?)", courses)

# ---------- Insert sample data into Grade table ----------
grades = [
    (1, 1, 95.0),  # Safa - Python
    (1, 2, 88.0),  # Safa - Data Science
    (2, 1, 76.0),  # Ali - Python
    (2, 3, 82.0),  # Ali - Database
    (3, 2, 90.0),  # Nour - Data Science
    (3, 4, 85.0)   # Nour - Machine Learning
]
cursor.executemany("INSERT INTO Grade (student_id, course_id, grade_value) VALUES (?, ?, ?)", grades)

# Save changes and close the connection
conn.commit()
conn.close()

print("Sample data inserted successfully into the database!")
