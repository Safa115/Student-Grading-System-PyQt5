import sqlite3
from models.person import Person

class Instructor(Person):
    """
    Class representing an instructor, inheriting from Person.
    """
    def __init__(self, name, email, instructor_id: int, department: str):
        super().__init__(name, email)
        self.instructor_id = instructor_id
        self.department = department

    # ---------- Encapsulation ----------
    def get_instructor_id(self):
        return self.instructor_id

    def set_instructor_id(self, instructor_id: int):
        self.instructor_id = instructor_id

    def get_department(self):
        return self.department

    def set_department(self, department: str):
        self.department = department

    # ---------- Database Integration ----------
    def save_to_db(self):
        """
        Save this instructor to the database.
        """
        conn = sqlite3.connect("student_grading.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Instructor (name, email)
            VALUES (?, ?)
        """, (self.name, self.email))

        conn.commit()
        conn.close()
        print(f"Instructor {self.name} added successfully!")



    @staticmethod
    def get_all_instructors():
        """
        Retrieve all instructors from the database.
        """
        conn = sqlite3.connect("student_grading.db")
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
        conn = sqlite3.connect("student_grading.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Instructor WHERE instructor_id = ?", (instructor_id,))
        conn.commit()
        conn.close()
        print(f"Instructor with ID {instructor_id} deleted successfully!")


    def update_instructor(self, new_name=None, new_email=None, new_department=None):
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
    
    def assign_grade(self, student_id: int, course_id: int, grade_value: float):
        """
        Assign or update a grade for a student in a specific course.
        """
        conn = sqlite3.connect("student_grading.db")
        cursor = conn.cursor()

        # Check if a grade already exists for this student & course
        cursor.execute("""
            SELECT grade_id FROM Grade WHERE student_id = ? AND course_id = ?
        """, (student_id, course_id))
        existing = cursor.fetchone()
        if existing:
            # Update the existing grade
            cursor.execute("""
                UPDATE Grade
                SET grade_value = ?
                WHERE student_id = ? AND course_id = ?
            """, (grade_value, student_id, course_id))
            print(f"Updated grade for student {student_id} in course {course_id} to {grade_value}.")
        else:
            # Insert a new grade
            cursor.execute("""
                INSERT INTO Grade (student_id, course_id, grade_value)
                VALUES (?, ?, ?)
            """, (student_id, course_id, grade_value))
            print(f"Assigned grade {grade_value} to student {student_id} for course {course_id}.")

        conn.commit()
        conn.close()



    def __str__(self):
        """
        Returns a readable representation of the instructor.
        """
        return f"Instructor(ID: {self.instructor_id}, Name: {self.name}, Department: {self.department})"
