import sqlite3
import os
import sys

# --- PATH FIX ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
# ----------------

class Course:
    def __init__(self, course_name: str, credit_hours: int, instructor_id: int, course_id: int = None):
        self.__course_id = course_id
        self.__course_name = course_name
        self.__credit_hours = credit_hours
        self.__instructor_id = instructor_id

    # Helper to get DB path correctly in both script and .exe modes
    @staticmethod
    def get_db_path():
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        return os.path.join(base_path, "student_grading.db")

    # ---------- Encapsulation ----------
    def get_course_id(self): return self.__course_id
    def set_course_id(self, course_id: int): self.__course_id = course_id
    def get_course_name(self): return self.__course_name
    def set_course_name(self, course_name: str): self.__course_name = course_name
    def get_credit_hours(self): return self.__credit_hours
    def set_credit_hours(self, credit_hours: int):
        if int(credit_hours) > 0: self.__credit_hours = int(credit_hours)
        else: raise ValueError("Credit hours must be positive")
    def get_instructor_id(self): return self.__instructor_id
    def set_instructor_id(self, instructor_id: int): self.__instructor_id = instructor_id

    # ---------- Database Methods ----------
    @staticmethod
    def connect():
        return sqlite3.connect(Course.get_db_path())

    def save_to_db(self):
        conn = self.connect()
        cursor = conn.cursor()

        if self.__course_id is not None:
            cursor.execute("""
                UPDATE Course
                SET name = ?, credit_hours = ?, instructor_id = ?
                WHERE course_id = ?
            """, (self.__course_name, self.__credit_hours, self.__instructor_id, self.__course_id))
        else:
            cursor.execute("""
                INSERT INTO Course (name, credit_hours, instructor_id)
                VALUES (?, ?, ?)
            """, (self.__course_name, self.__credit_hours, self.__instructor_id))
            self.__course_id = cursor.lastrowid

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_courses():
        conn = Course.connect()
        cursor = conn.cursor()
        query = """
            SELECT C.course_id, C.name, C.credit_hours, I.name, C.instructor_id 
            FROM Course C
            LEFT JOIN Instructor I ON C.instructor_id = I.instructor_id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def delete_course(course_id: int):
        conn = Course.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Course WHERE course_id = ?", (course_id,))
        conn.commit()
        conn.close()