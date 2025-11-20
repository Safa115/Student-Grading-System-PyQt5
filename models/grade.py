import sqlite3
from models.database_manager import DatabaseManager

class Grade:
    def __init__(self, student_id: int, course_id: int, grade_value: float = None, grade: float = None):
        self.student_id = student_id
        self.course_id = course_id
        
        # Handle both parameter names to avoid errors from legacy calls
        if grade_value is not None:
            self.grade_value = float(grade_value)
        elif grade is not None:
            self.grade_value = float(grade)
        else:
            self.grade_value = 0.0

    def assign_grade(self):
        """
        Assigns or Updates a grade. 
        If the grade exists, it updates it. If not, it inserts a new one.
        Then triggers GPA calculation.
        """
        conn = sqlite3.connect(r"student_grading.db")
        cursor = conn.cursor()

        # Check if grade exists
        cursor.execute("SELECT * FROM Grade WHERE student_id = ? AND course_id = ?", 
                       (self.student_id, self.course_id))
        existing = cursor.fetchone()

        if existing:
            # Update existing grade
            cursor.execute("""
                UPDATE Grade 
                SET grade_value = ? 
                WHERE student_id = ? AND course_id = ?
            """, (self.grade_value, self.student_id, self.course_id))
            print(f"Updated grade for Student {self.student_id} in Course {self.course_id}")
        else:
            # Insert new grade
            cursor.execute("""
                INSERT INTO Grade (student_id, course_id, grade_value) 
                VALUES (?, ?, ?)
            """, (self.student_id, self.course_id, self.grade_value))
            print(f"Assigned new grade for Student {self.student_id}")

        conn.commit()
        conn.close()

        # Automatically recalculate GPA after updating grade
        try:
            db = DatabaseManager()
            db.calculate_gpa(self.student_id, self.course_id)
        except Exception as e:
            print(f"Warning: GPA Calculation issue: {e}")

    @staticmethod
    def get_all_grades_info():
        """
        Returns list of tuples: (student_id, student_name, course_id, course_name, grade_value)
        """
        conn = sqlite3.connect(r"student_grading.db")
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
        conn = sqlite3.connect(r"student_grading.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Grade WHERE student_id = ? AND course_id = ?", (student_id, course_id))
        conn.commit()
        conn.close()
        
        # Recalculate GPA after deletion
        try:
            db = DatabaseManager()
            db.calculate_gpa(student_id, course_id)
        except:
            pass

    def get_letter_grade(self):
        g = self.grade_value
        if g >= 90: return "A"
        elif g >= 80: return "B"
        elif g >= 70: return "C"
        elif g >= 60: return "D"
        else: return "F"