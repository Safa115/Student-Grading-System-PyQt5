import sqlite3

class Course:
    def __init__(self, course_name: str, credit_hours: int, instructor_id: int, course_id: int = None):
        # Use setters/internal variables directly to avoid conflict
        self.__course_id = course_id
        self.__course_name = course_name
        self.__credit_hours = credit_hours
        self.__instructor_id = instructor_id

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
        if int(credit_hours) > 0:
            self.__credit_hours = int(credit_hours)
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
       
        return sqlite3.connect(r"student_grading.db")

    def save_to_db(self):
        """
        Saves the course to the database (Insert or Update).
        """
        conn = self.connect()
        cursor = conn.cursor()

        if self.__course_id is not None:
           
            cursor.execute("""
                UPDATE Course
                SET name = ?, credit_hours = ?, instructor_id = ?
                WHERE course_id = ?
            """, (self.__course_name, self.__credit_hours, self.__instructor_id, self.__course_id))
            print(f"Course ID {self.__course_id} updated successfully.")
        else:
            # INSERT Logic
            cursor.execute("""
                INSERT INTO Course (name, credit_hours, instructor_id)
                VALUES (?, ?, ?)
            """, (self.__course_name, self.__credit_hours, self.__instructor_id))
            self.__course_id = cursor.lastrowid
            print(f"New course '{self.__course_name}' added with ID {self.__course_id}.")

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_courses():
        """
        Retrieve all courses with Instructor Name instead of just ID.
        Returns: list of tuples (course_id, course_name, credit_hours, instructor_name, instructor_id)
        """
        conn = Course.connect()
        cursor = conn.cursor()
        # Join to get Instructor Name
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
        """Delete a course from the database by ID."""
        conn = Course.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Course WHERE course_id = ?", (course_id,))
        conn.commit()
        conn.close()