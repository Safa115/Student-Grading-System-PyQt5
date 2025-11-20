import sqlite3
import os
import sys

# --- PATH FIX ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
# ----------------

try:
    from models.person import Person
except ModuleNotFoundError:
    from person import Person

from models.database_manager import DatabaseManager
from models.grade import Grade

class Instructor(Person):
    """
    Class representing an instructor, inheriting from Person.
    """
    def __init__(self, name, email, instructor_id: int = None):
        super().__init__(name, email)
        self.instructor_id = instructor_id
        
    # Helper to get DB path correctly
    @staticmethod
    def get_db_path():
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        return os.path.join(base_path, "student_grading.db")

    # ---------- Encapsulation ----------
    def get_instructor_id(self):
        return self.instructor_id

    def set_instructor_id(self, instructor_id: int):
        self.instructor_id = instructor_id

    # ---------- Database Integration ----------
    def save_to_db(self):
        conn = sqlite3.connect(self.get_db_path())
        cursor = conn.cursor()
        
        if self.instructor_id is not None:
            # Update Existing Instructor
            cursor.execute("UPDATE Instructor SET name = ?, email = ? WHERE instructor_id = ?",
                           (self.name, self.email, self.instructor_id))
            print(f"Instructor ID {self.instructor_id} updated successfully!")
        else:
            # Insert New Instructor
            cursor.execute("""
                INSERT INTO Instructor (name, email)
                VALUES (?, ?)
            """, (self.name, self.email))
            
            self.instructor_id = cursor.lastrowid 
            print(f"New Instructor added with ID: {self.instructor_id}")
            
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_instructors():
        conn = sqlite3.connect(Instructor.get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Instructor")
        instructors = cursor.fetchall()
        conn.close()
        return instructors
    
    @staticmethod
    def delete_instructor(instructor_id):
        conn = sqlite3.connect(Instructor.get_db_path())
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Instructor WHERE instructor_id = ?", (instructor_id,))
        conn.commit()
        conn.close()
        print(f"Instructor with ID {instructor_id} deleted successfully!")

    # ---------- Additional Methods ----------
    
    def assign_grade(self, student_id, course_id, grade_value):
        """
        Assign or update a student's grade for a specific course,
        then automatically update the student's GPA.
        """
        # Note: DatabaseManager handles the path internally now
        db = DatabaseManager()
        conn = db.connect()
        cursor = conn.cursor()

        # Check if grade already exists
        cursor.execute("""
            SELECT grade_id FROM Grade WHERE student_id=? AND course_id=?
        """, (student_id, course_id))
        existing_grade = cursor.fetchone()

        if existing_grade:
            cursor.execute("""
                UPDATE Grade SET grade_value=? WHERE student_id=? AND course_id=?
            """, (grade_value, student_id, course_id))
            print(f"Updated grade for student {student_id} in course {course_id} to {grade_value}.")
        else:
            cursor.execute("""
                INSERT INTO Grade (student_id, course_id, grade_value)
                VALUES (?, ?, ?)
            """, (student_id, course_id, grade_value))
            print(f"Assigned grade {grade_value} to student {student_id} in course {course_id}.")

        conn.commit()
        # Automatically recalculate GPA after updating grade
        db.calculate_gpa(student_id, course_id)
        conn.close()

    def display_info(self):
        return f"Instructor: {self.name}, Email: {self.email}, ID: {self.instructor_id}"