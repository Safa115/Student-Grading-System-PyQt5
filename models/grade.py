import sqlite3
import os
import sys

# --- PATH FIX ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
# ----------------

from models.database_manager import DatabaseManager

class Grade:
    def __init__(self, student_id: int, course_id: int, grade_value: float = None, grade: float = None):
        self.student_id = student_id
        self.course_id = course_id
        if grade_value is not None:
            self.grade_value = float(grade_value)
        elif grade is not None:
            self.grade_value = float(grade)
        else:
            self.grade_value = 0.0

    # Helper to get DB path
    @staticmethod
    def get_db_path():
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        return os.path.join(base_path, "student_grading.db")

    def assign_grade(self):
        conn = sqlite3.connect(self.get_db_path())
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Grade WHERE student_id = ? AND course_id = ?", 
                       (self.student_id, self.course_id))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE Grade 
                SET grade_value = ? 
                WHERE student_id = ? AND course_id = ?
            """, (self.grade_value, self.student_id, self.course_id))
        else:
            cursor.execute("""
                INSERT INTO Grade (student_id, course_id, grade_value) 
                VALUES (?, ?, ?)
            """, (self.student_id, self.course_id, self.grade_value))

        conn.commit()
        conn.close()

        try:
            db = DatabaseManager() # DatabaseManager handles its own path now
            db.calculate_gpa(self.student_id, self.course_id)
        except Exception as e:
            print(f"Warning: GPA Calculation issue: {e}")

    @staticmethod
    def get_all_grades_info():
        conn = sqlite3.connect(Grade.get_db_path())
        cursor = conn.cursor()
        query = """
            SELECT G.student_id, S.name, G.course_id, C.name, G.grade_value
            FROM Grade G
            JOIN Student S ON G.student_id = S.student_id
            JOIN Course C ON G.course_id = C.course_id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def delete_grade(student_id, course_id):
        conn = sqlite3.connect(Grade.get_db_path())
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Grade WHERE student_id = ? AND course_id = ?", (student_id, course_id))
        conn.commit()
        conn.close()
        
        try:
            db = DatabaseManager()
            db.calculate_gpa(student_id, course_id)
        except:
            pass

    def calculate_grade_points(self):
        """ Calculates points for GPA (4.0 Scale) """
        g = self.grade_value
        if g >= 90: return 4.0
        elif g >= 80: return 3.0
        elif g >= 70: return 2.0
        elif g >= 60: return 1.0
        else: return 0.0

    def get_letter_grade(self):
        g = self.grade_value
        if g >= 90: return "A"
        elif g >= 80: return "B"
        elif g >= 70: return "C"
        elif g >= 60: return "D"
        else: return "F"