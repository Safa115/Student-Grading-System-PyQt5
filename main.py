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
