import sqlite3
import os
import sys
from models.person import Person

class Student(Person):
    def __init__(self, name: str, email: str, student_id: int = None, credit_hours: int = 0, gpa: float = 0.0):
        super().__init__(name, email)
        self.student_id = student_id
        self.credit_hours = credit_hours
        self.gpa = gpa
        self.db_path = self.get_db_path()

    def get_db_path(self):
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        return os.path.join(base_path, "student_grading.db")

    def get_student_id(self):
        return self.student_id

    def set_student_id(self, student_id: int):
        self.student_id = student_id

    def get_gpa(self):
        return self.gpa

    def get_credit_hours(self):
        return self.credit_hours

    def save_to_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if self.student_id:
            cursor.execute("""
                UPDATE Student 
                SET name = ?, email = ?
                WHERE student_id = ?
            """, (self.name, self.email, self.student_id))
            print(f"Student ID {self.student_id} updated.")
        else:
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
        # Helper to get DB path statically
        if getattr(sys, 'frozen', False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        path = os.path.join(base, "student_grading.db")

        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, name, email, credit_hours, gpa FROM Student")
        students = cursor.fetchall()
        conn.close()
        return students

    @staticmethod
    def delete_student(student_id: int):
        # Helper to get DB path statically
        if getattr(sys, 'frozen', False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        path = os.path.join(base, "student_grading.db")

        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Student WHERE student_id = ?", (student_id,))
        conn.commit()
        conn.close()
        print(f"Student ID {student_id} deleted.")

    def display_info(self):
        return f"Student: {self.name}, Email: {self.email}, GPA: {self.gpa}"