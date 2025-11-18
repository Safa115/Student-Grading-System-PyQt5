import sqlite3
from models.person import Person
from models.database_manager import DatabaseManager
from models.grade import Grade

class Instructor(Person):
    """
    Class representing an instructor, inheriting from Person.
    """
    # 1. Tweak: make instructor_id optional for new instances
    def __init__(self, name, email, instructor_id: int = None):
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
        
        # 2. Unified INSERT or UPDATE logic
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
            
            # Retrieve the new ID and store it in the object
            self.instructor_id = cursor.lastrowid 
            print(f"New Instructor added with ID: {self.instructor_id}")
            
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


    # Removed update_instructor method since save_to_db handles updates now
    

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
        # Automatically recalculate GPA after updating grade
        db.calculate_gpa(student_id,course_id)
        conn.close()


    def display_info(self):
        return f"Instructor: {self.name}, Email: {self.email}, ID: {self.instructor_id}"