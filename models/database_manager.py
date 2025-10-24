import sqlite3

class DatabaseManager:
    """
    This class handles all database operations such as inserting,
    updating, deleting, and retrieving records from the database.
    """

    def __init__(self, db_name=r"C:\StudentGradingSystem\student_grading.db"):
        self.db_name = db_name

    # ---------- Internal connection methods ----------
    def connect(self):
        return sqlite3.connect(self.db_name)

    # ---------- Student Methods ----------
    def add_student(self, name, email, credit_hours=0):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Student (name, email, credit_hours)
            VALUES (?, ?, ?)
        """, (name, email, credit_hours))
        conn.commit()
        conn.close()

    def get_all_students(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Student")
        students = cursor.fetchall()
        conn.close()
        return students

    def get_student_by_id(self, student_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Student WHERE student_id = ?", (student_id,))
        student = cursor.fetchone()
        conn.close()
        return student

    def update_student(self, student_id, name=None, email=None, credit_hours=None):
        conn = self.connect()
        cursor = conn.cursor()
        if name:
            cursor.execute("UPDATE Student SET name = ? WHERE student_id = ?", (name, student_id))
        if email:
            cursor.execute("UPDATE Student SET email = ? WHERE student_id = ?", (email, student_id))
        if credit_hours is not None:
            cursor.execute("UPDATE Student SET credit_hours = ? WHERE student_id = ?", (credit_hours, student_id))
        conn.commit()
        conn.close()

    def delete_student(self, student_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Student WHERE student_id = ?", (student_id,))
        conn.commit()
        conn.close()

    # ---------- Instructor Methods ----------
    def add_instructor(self, name, email):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Instructor (name, email)
            VALUES (?, ?)
        """, (name, email))
        conn.commit()
        conn.close()

    def get_all_instructors(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Instructor")
        instructors = cursor.fetchall()
        conn.close()
        return instructors

    # ---------- Course Methods ----------
    def add_course(self, name, credit_hours, instructor_id=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Course (name, credit_hours, instructor_id)
            VALUES (?, ?, ?)
        """, (name, credit_hours, instructor_id))
        conn.commit()
        conn.close()

    def get_all_courses(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Course")
        courses = cursor.fetchall()
        conn.close()
        return courses

    # ---------- Grade Methods ----------
    def add_grade(self, student_id, course_id, grade_value):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Grade (student_id, course_id, grade_value)
            VALUES (?, ?, ?)
        """, (student_id, course_id, grade_value))
        conn.commit()
        conn.close()

    def get_grades_by_student(self, student_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Course.name, Grade.grade_value
            FROM Grade
            JOIN Course ON Grade.course_id = Course.course_id
            WHERE Grade.student_id = ?
        """, (student_id,))
        grades = cursor.fetchall()
        conn.close()
        return grades

# ---------- GPA Calculation ----------
    def calculate_gpa(self, student_id,course_id):
      """
    Calculate and update the GPA for a specific student (on a 4.0 scale),
    using Grade class's calculate_grade_points().
    """
      from models.grade import Grade  # Import here to avoid circular import

      conn = self.connect()
      cursor = conn.cursor()

    # Fetch all numeric grades for this student
      cursor.execute("""
        SELECT grade_value FROM Grade WHERE student_id=?
    """, (student_id,))
      grades = cursor.fetchall()

      if not grades:
        print(f"No grades found for student {student_id}.")
        conn.close()
        return 0.0

      total_points = 0
      for (grade_value,) in grades:
        # Create a temporary Grade object to use its method
        g = Grade(student_id=student_id, course_id=course_id, grade=grade_value)

        total_points += g.calculate_grade_points()

      gpa = round(total_points / len(grades), 2)

    # Update student's GPA in the Student table
      cursor.execute("""
        UPDATE Student SET gpa=? WHERE student_id=?
    """, (gpa, student_id))
      conn.commit()
      conn.close()

      print(f"GPA for student {student_id}: {gpa}")
      return gpa



