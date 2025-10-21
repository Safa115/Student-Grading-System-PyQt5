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
    def enroll_student(self,student):
        """
        Placeholder method for enrolling a student in the course.
        """
        pass
    def course_summary(self):
        """
        Placeholder method for providing a summary of the course.
        """
        pass
    def __str__(self):
        """
        Returns a readable representation of the course.
        """
        return f"Course(ID: {self.course_id}, Name: {self.course_name}, Credit Hours: {self.credit_hours}, Instructor ID: {self.instructor_id})"
    

