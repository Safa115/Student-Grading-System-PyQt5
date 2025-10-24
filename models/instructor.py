import sqlite3
from models.person import Person
from models.database_manager import DatabaseManager
from models.grade import Grade

class Instructor(Person):
    """
    Class representing an instructor, inheriting from Person.
    """
    def __init__(self, name, email, instructor_id: int):
        super().__init__(name, email)
        self.instructor_id = instructor_id
        

    # ---------- Encapsulation ----------
    def get_instructor_id(self):
        return self.instructor_id

    def set_instructor_id(self, instructor_id: int):
        self.instructor_id = instructor_id


    # ---------- Database Integration ----------
    def save_to_db(self):
      conn = sqlite3.connect(r"C:\StudentGradingSystem\student_grading.db")
      cursor = conn.cursor()
    
    # check if email exists
      cursor.execute("SELECT * FROM Instructor WHERE email = ?", (self.email,))
      existing = cursor.fetchone()
      if existing:
        print(f"Instructor with email {self.email} already exists.")
        conn.close()
        return

      cursor.execute("""
        INSERT INTO Instructor (name, email)
        VALUES (?, ?)
    """, (self.name, self.email))
      conn.commit()
      conn.close()


    @staticmethod
    def get_all_instructors():
        """
        Retrieve all instructors from the database.
        """
        conn = sqlite3.connect(r"C:\StudentGradingSystem\student_grading.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Instructor")
        instructors = cursor.fetchall()
        conn.close()
        return instructors
    


    @staticmethod
    def delete_instructor(instructor_id):
        """
        Delete an instructor from the database by ID.
        """
        conn = sqlite3.connect(r"C:\StudentGradingSystem\student_grading.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Instructor WHERE instructor_id = ?", (instructor_id,))
        conn.commit()
        conn.close()
        print(f"Instructor with ID {instructor_id} deleted successfully!")


    def update_instructor(self, new_name=None, new_email=None):
        """
        Update the instructor’s information in the database.
        """
        conn = sqlite3.connect("student_grading.db")
        cursor = conn.cursor()

        if new_name:
            cursor.execute("UPDATE Instructor SET name = ? WHERE instructor_id = ?", (new_name, self.instructor_id))
            self.name = new_name

        if new_email:
            cursor.execute("UPDATE Instructor SET email = ? WHERE instructor_id = ?", (new_email, self.instructor_id))
            self.email = new_email

       

        conn.commit()
        conn.close()
        print(f"Instructor {self.instructor_id} updated successfully!")



    # ---------- Additional Methods ----------
    
    def assign_grade(self, student_id, course_id, grade_value):
      """
    Assign or update a student's grade for a specific course,
    then automatically update the student's GPA.
    """
       

      db = DatabaseManager()
      conn = db.connect()
      cursor = conn.cursor()

    # Check if grade already exists for this student & course
      cursor.execute("""
        SELECT grade_id FROM Grade WHERE student_id=? AND course_id=?
    """, (student_id, course_id))
      existing_grade = cursor.fetchone()

      if existing_grade:
        # Update existing grade
        cursor.execute("""
            UPDATE Grade SET grade_value=? WHERE student_id=? AND course_id=?
        """, (grade_value, student_id, course_id))
        print(f"Updated grade for student {student_id} in course {course_id} to {grade_value}.")
      else:
        # Insert new grade
        cursor.execute("""
            INSERT INTO Grade (student_id, course_id, grade_value)
            VALUES (?, ?, ?)
        """, (student_id, course_id, grade_value))
        print(f"Assigned grade {grade_value} to student {student_id} in course {course_id}.")

      conn.commit()
    #  Automatically recalculate GPA after updating grade
      db.calculate_gpa(student_id,course_id)
      conn.close()


    def display_info(self):
        return f"Instructor: {self.name}, Email: {self.email}"
