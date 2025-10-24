import sqlite3

class Grade:
    def __init__(self, student_id: int, course_id: int, grade: float):
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade

    # ---------- Encapsulation ----------
    def get_student_id(self):
        return self.__student_id

    def set_student_id(self, student_id: int):
        self.__student_id = student_id

    def get_course_id(self):
        return self.__course_id

    def set_course_id(self, course_id: int):
        self.__course_id = course_id

    def get_grade(self):
        return self.__grade

    def set_grade(self, grade: float):
        if 0.0 <= grade <= 100.0:
            self.__grade = grade
        else:
            raise ValueError("Grade must be between 0.0 and 100.0")

    # ---------- Additional Methods ----------
    def calculate_grade_points(self):
        """
        Calculate grade points based on the numeric grade.
        Typical 4.0 GPA scale conversion.
        """
        if self.grade >= 90:
            return 4.0
        elif self.grade >= 80:
            return 3.0
        elif self.grade >= 70:
            return 2.0
        elif self.grade >= 60:
            return 1.0
        else:
            return 0.0


    def get_letter_grade(self):
        """
        Convert numeric grade to letter grade.
        """
        if self.grade >= 90:
            return "A"
        elif self.grade >= 80:
            return "B"
        elif self.grade >= 70:
            return "C"
        elif self.grade >= 60:
            return "D"
        else:
            return "F"

    # ---------- Database Integration ----------
    def save_to_db(self):
        """Insert a new grade record into the database."""
        conn = sqlite3.connect(r"C:\StudentGradingSystem\student_grading.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Grade (student_id, course_id, grade_value) VALUES (?, ?, ?)",
            (self.student_id, self.course_id, self.grade)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_grades_by_student(student_id):
        """Fetch all grades for a given student."""
        conn = sqlite3.connect(r"C:\StudentGradingSystem\student_grading.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Grade WHERE student_id = ?", (student_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def update_grade(student_id, course_id, new_grade):
        """Update an existing grade for a student in a specific course."""
        conn = sqlite3.connect(r"C:\StudentGradingSystem\student_grading.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Grade SET grade_value = ? WHERE student_id = ? AND course_id = ?",
            (new_grade, student_id, course_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete_grade(student_id, course_id):
        """Delete a grade record for a given student and course."""
        conn = sqlite3.connect(r"C:\StudentGradingSystem\student_grading.db")
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Grade WHERE student_id = ? AND course_id = ?",
            (student_id, course_id)
        )
        conn.commit()
        conn.close()

    def __str__(self):
        letter = self.get_letter_grade()
        return (
            f"Grade -> Student ID: {self.student_id}, "
            f"Course ID: {self.course_id}, "
            f"Numeric Grade: {self.grade}, "
            f"Letter Grade: {letter}"
        )
