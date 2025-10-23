import sqlite3
class Course:
    def __init__(self, course_id: int, course_name: str, credit_hours: int, instructor_id: int):
        self.course_id = course_id
        self.course_name = course_name
        self.credit_hours = credit_hours
        self.instructor_id = instructor_id

    # ---------- Encapsulation ----------
    def get_course_id(self):
        return self.__course_id

    def set_course_id(self, course_id: int):
        self.__course_id = course_id

    def get_course_name(self):
        return self.__course_name

    def set_course_name(self, course_name: str):
        self.__course_name = course_name

    def get_credit_hours(self):
        return self.__credit_hours

    def set_credit_hours(self, credit_hours: int):
        if credit_hours > 0:
            self.__credit_hours = credit_hours
        else:
            raise ValueError("Credit hours must be positive")

    def get_instructor_id(self):
        return self.__instructor_id

    def set_instructor_id(self, instructor_id: int):
        self.__instructor_id = instructor_id

    # ---------- Database Methods ----------
    @staticmethod
    def connect():
        """Connect to the SQLite database."""
        return sqlite3.connect("database/student_grading.db")

    def save_to_db(self):
        """Insert a new course record into the database."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Course (name, credit_hours, instructor_id)
            VALUES (?, ?, ?)
        """, (self.course_name, self.credit_hours, self.instructor_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_courses():
        """Retrieve all courses from the database."""
        conn = Course.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Course")
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_course_by_id(course_id: int):
        """Retrieve a course by its ID."""
        conn = Course.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Course WHERE course_id = ?", (course_id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def update_course(self):
        """Update course details in the database."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Course
            SET name = ?, credit_hours = ?, instructor_id = ?
            WHERE course_id = ?
        """, (self.course_name, self.credit_hours, self.instructor_id, self.course_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_course(course_id: int):
        """Delete a course from the database by ID."""
        conn = Course.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Course WHERE course_id = ?", (course_id,))
        conn.commit()
        conn.close()
    #---------- Additional Methods ----------

    def enroll_student(self, student_id:int):
     """
       Enroll a student in this course by adding a record to the Enrollment table.
     """
     conn = self.connect()
     cursor = conn.cursor()

     # Check if already enrolled
     cursor.execute("""
        SELECT * FROM Enrollment WHERE student_id = ? AND course_id = ?
     """, (student_id, self.course_id))
     exists = cursor.fetchone()

     if exists:
        print(f" Student {student_id} is already enrolled in course {self.course_id}.")
     else:
        cursor.execute("""
            INSERT INTO Enrollment (student_id, course_id)
            VALUES (?, ?)
        """, (student_id, self.course_id))
        conn.commit()
        print(f"Student {student_id} enrolled successfully in {self.course_name}.")

     conn.close()

       
    def course_summary(self):
     """
     Returns a summary of the course with instructor name and number of enrolled students.
     """
     conn = self.connect()
     cursor = conn.cursor()

    # Instructor name
     cursor.execute("SELECT name FROM Instructor WHERE instructor_id = ?", (self.instructor_id,))
     instructor_row = cursor.fetchone()
     instructor_name = instructor_row[0] if instructor_row else "Unknown"

    # Number of enrolled students
     cursor.execute("SELECT COUNT(*) FROM Enrollment WHERE course_id = ?", (self.course_id,))
     count_row = cursor.fetchone()
     enrolled_count = count_row[0] if count_row else 0

     conn.close()

     return (
        f"📘 Course Summary:\n"
        f"- ID: {self.course_id}\n"
        f"- Name: {self.course_name}\n"
        f"- Credit Hours: {self.credit_hours}\n"
        f"- Instructor: {instructor_name}\n"
        f"- Enrolled Students: {enrolled_count}"
    )

    def __str__(self):
        """
        Returns a readable representation of the course.
        """
        return f"Course(ID: {self.course_id}, Name: {self.course_name}, Credit Hours: {self.credit_hours}, Instructor ID: {self.instructor_id})"
    

