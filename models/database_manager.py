import sqlite3

class DatabaseManager:
    def __init__(self, db_name=r"student_grading.db"):
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Student (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                credit_hours INTEGER DEFAULT 0,
                gpa REAL DEFAULT 0.0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Instructor (
                instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Course (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                credit_hours INTEGER NOT NULL,
                instructor_id INTEGER,
                FOREIGN KEY (instructor_id) REFERENCES Instructor(instructor_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Grade (
                grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id INTEGER,
                grade_value REAL,
                FOREIGN KEY (student_id) REFERENCES Student(student_id),
                FOREIGN KEY (course_id) REFERENCES Course(course_id)
            )
        """)
        
        conn.commit()
        conn.close()

    # ---------- Student Methods ----------
    def add_student(self, name, email, credit_hours=0):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Student (name, email, credit_hours)
            VALUES (?, ?, ?)
        """, (name, email, credit_hours))
        conn.commit()
        conn.close()

    def get_all_students(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Student")
        students = cursor.fetchall()
        conn.close()
        return students

    def get_student_by_id(self, student_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Student WHERE student_id = ?", (student_id,))
        student = cursor.fetchone()
        conn.close()
        return student

    def update_student(self, student_id, name=None, email=None, credit_hours=None):
        conn = self.connect()
        cursor = conn.cursor()
        if name:
            cursor.execute("UPDATE Student SET name = ? WHERE student_id = ?", (name, student_id))
        if email:
            cursor.execute("UPDATE Student SET email = ? WHERE student_id = ?", (email, student_id))
        if credit_hours is not None:
            cursor.execute("UPDATE Student SET credit_hours = ? WHERE student_id = ?", (credit_hours, student_id))
        conn.commit()
        conn.close()

    def delete_student(self, student_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Student WHERE student_id = ?", (student_id,))
        conn.commit()
        conn.close()

    # ---------- Instructor Methods ----------
    def add_instructor(self, name, email):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Instructor (name, email)
            VALUES (?, ?)
        """, (name, email))
        conn.commit()
        conn.close()

    def get_all_instructors(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Instructor")
        instructors = cursor.fetchall()
        conn.close()
        return instructors

    # ---------- Course Methods ----------
    def add_course(self, name, credit_hours, instructor_id=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Course (name, credit_hours, instructor_id)
            VALUES (?, ?, ?)
        """, (name, credit_hours, instructor_id))
        conn.commit()
        conn.close()

    def get_all_courses(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Course")
        courses = cursor.fetchall()
        conn.close()
        return courses

    # ---------- Grade Methods ----------
    def add_grade(self, student_id, course_id, grade_value):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Grade (student_id, course_id, grade_value)
            VALUES (?, ?, ?)
        """, (student_id, course_id, grade_value))
        conn.commit()
        conn.close()

    def get_grades_by_student(self, student_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Course.name, Grade.grade_value
            FROM Grade
            JOIN Course ON Grade.course_id = Course.course_id
            WHERE Grade.student_id = ?
        """, (student_id,))
        grades = cursor.fetchall()
        conn.close()
        return grades

    # ---------- GPA Calculation (Weighted) ----------
    def calculate_gpa(self, student_id, course_id=None):
        conn = self.connect()
        cursor = conn.cursor()

        query = """
            SELECT G.grade_value, C.credit_hours
            FROM Grade G
            JOIN Course C ON G.course_id = C.course_id
            WHERE G.student_id = ?
        """
        cursor.execute(query, (student_id,))
        records = cursor.fetchall()

        if not records:
            cursor.execute("UPDATE Student SET gpa = 0.0, credit_hours = 0 WHERE student_id = ?", (student_id,))
            conn.commit()
            conn.close()
            return 0.0

        total_weighted_points = 0
        total_credits = 0

        for grade_val, credit_hours in records:
            # Convert numeric grade to 4.0 scale points
            if grade_val >= 90: points = 4.0
            elif grade_val >= 80: points = 3.0
            elif grade_val >= 70: points = 2.0
            elif grade_val >= 60: points = 1.0
            else: points = 0.0
            
            total_weighted_points += (points * credit_hours)
            total_credits += credit_hours

        if total_credits > 0:
            final_gpa = round(total_weighted_points / total_credits, 2)
        else:
            final_gpa = 0.0

        cursor.execute("""
            UPDATE Student 
            SET gpa = ?, credit_hours = ? 
            WHERE student_id = ?
        """, (final_gpa, total_credits, student_id))
        
        conn.commit()
        conn.close()
        return final_gpa

    # ---------- Dashboard Statistics Methods ----------
    def get_general_stats(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM Student")
        total_students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Course")
        total_courses = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Instructor")
        total_instructors = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(gpa) FROM Student")
        avg_gpa = cursor.fetchone()[0]
        avg_gpa = round(avg_gpa, 2) if avg_gpa else 0.0

        conn.close()
        return total_students, total_courses, total_instructors, avg_gpa

    def get_grade_distribution(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT grade_value FROM Grade")
        grades = cursor.fetchall()
        conn.close()

        distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for g in grades:
            score = g[0]
            if score >= 90: distribution['A'] += 1
            elif score >= 80: distribution['B'] += 1
            elif score >= 70: distribution['C'] += 1
            elif score >= 60: distribution['D'] += 1
            else: distribution['F'] += 1
        
        return distribution

    def get_course_enrollment_stats(self):
        conn = self.connect()
        cursor = conn.cursor()
        
        query = """
            SELECT C.name, COUNT(G.student_id) 
            FROM Course C
            LEFT JOIN Grade G ON C.course_id = G.course_id
            GROUP BY C.course_id
        """
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        
        return data