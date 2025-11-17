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
#----------------------------------------------------------
from models.database_manager import DatabaseManager
from models.course import Course
from models.student import Student
from models.instructor import Instructor
from models.grade import Grade


def test_database_integration():
    print("Starting Database Integration Test...\n")
    
    # ---------- Step 1: Add Instructor ----------
    instructor = Instructor(name="Dr. mostafa", email="mostafa@email.com", instructor_id=None)
    instructor.save_to_db()
    print("Instructor added!")

    # ---------- Step 2: Add Course ----------
    course = Course(course_id=None, course_name="Python 101", credit_hours=3, instructor_id=6)  
    course.save_to_db()
    course.enroll_student(student_id=1)

    print("Course added!")

    # ---------- Step 3: Add Student ----------
    student = Student(name="Sofi", email="sofi@email.com", student_id=None)
    student.save_to_db()
    print("Student added!")

    # ---------- Step 4: Enroll Student ----------
    course.enroll_student(student_id=5)  
    print("Student enrolled in course!")

    # ---------- Step 5: Assign Grade ----------
    instructor.assign_grade(student_id=1, course_id=1, grade_value=90)
    print("Grade assigned!")

    # ---------- Step 6: Calculate GPA ----------
    db = DatabaseManager()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT gpa FROM Student WHERE student_id = ?", (1,))
    updated_gpa = cursor.fetchone()[0]
    conn.close()
    print(f" Updated GPA for student 1: {updated_gpa}\n")

    # ---------- Step 7: Course Summary ----------
    summary = course.course_summary()
    print("\nCourse Summary:")
    print(summary)

if __name__ == "__main__":
    test_database_integration()
