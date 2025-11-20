import sqlite3
from models.person import Person

class Student(Person):
    """
    Class representing a student, inheriting from Person.
    """
    def __init__(self, name: str, email: str, student_id: int = None, credit_hours: int = 0, gpa: float = 0.0):
        super().__init__(name, email)
        self.student_id = student_id
        self.credit_hours = credit_hours
        self.gpa = gpa

    # ---------- Encapsulation ----------
    def get_student_id(self):
        return self.student_id

    def set_student_id(self, student_id: int):
        self.student_id = student_id

    def get_gpa(self):
        return self.gpa

    def get_credit_hours(self):
        return self.credit_hours

    # ---------- Database Integration ----------
    def save_to_db(self):
        """
        Save or update the student into the database.
        """
        conn = sqlite3.connect(r"C:\StudentGradingSystem\student_grading.db")
        cursor = conn.cursor()

        if self.student_id:
            # Update existing student (Name and Email only, GPA/Hours are updated by Grades)
            cursor.execute("""
                UPDATE Student 
                SET name = ?, email = ?
                WHERE student_id = ?
            """, (self.name, self.email, self.student_id))
            print(f"Student ID {self.student_id} updated.")
        else:
            # Insert new student
            # Check duplicates first
            cursor.execute("SELECT student_id FROM Student WHERE email = ?", (self.email,))
            if cursor.fetchone():
                print(f"Student with email '{self.email}' already exists.")
                conn.close()
                return

            cursor.execute("""
                INSERT INTO Student (name, email, credit_hours, gpa)
                VALUES (?, ?, 0, 0.0)
            """, (self.name, self.email))
            
            self.student_id = cursor.lastrowid
            print(f"New student '{self.name}' saved with ID {self.student_id}.")

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_students():
        """
        Retrieve all students with specific columns for the UI table.
        Returns: list of tuples (id, name, email, credit_hours, gpa)
        """
        conn = sqlite3.connect(r"C:\StudentGradingSystem\student_grading.db")
        cursor = conn.cursor()
        
        # Explicitly select columns in the order the UI expects
        cursor.execute("SELECT student_id, name, email, credit_hours, gpa FROM Student")
        
        students = cursor.fetchall()
        conn.close()
        return students

    @staticmethod
    def delete_student(student_id: int):
        """
        Delete a student by ID.
        """
        conn = sqlite3.connect(r"C:\StudentGradingSystem\student_grading.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Student WHERE student_id = ?", (student_id,))
        conn.commit()
        conn.close()
        print(f"Student ID {student_id} deleted.")

    def display_info(self):
        return f"Student: {self.name}, Email: {self.email}, GPA: {self.gpa}"