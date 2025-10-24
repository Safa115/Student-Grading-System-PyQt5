from models.person import Person
from models.database_manager import DatabaseManager
class Student(Person):
    """
    Class representing a student, inheriting from Person.
    """
    def __init__(self,name:str,email:str,student_id:int,credit_hours:int=0,gpa:float=0.0):
       super().__init__(name,email)
       self.student_id=student_id
       self.credit_hours= credit_hours
       self.gpa=gpa
    #---------- Encapsulation ----------
    def get_student_id(self):
         return self.__student_id
    def set_student_id(self,student_id:int):
         self.__student_id=student_id
    
        
    def get_gpa(self):
         return self.__gpa
    def set_gpa(self,gpa:float):
         if 0.0<=gpa<4.0:
              self.__gpa = gpa

         else:
               raise ValueError("GPA must be between 0.0 and 4.0")
         

    
    def get_credit_hours(self):
         return self.__credit_hours
    def set_credit_hours(self,credit_hours:int):
         if credit_hours >=0:
              self.__credit_hours=credit_hours
         else:
              raise ValueError("Credit hours cannot be negative")
         
         #---------- Additional Methods ----------
    def display_info(self):
        return f"Student: {self.name}, Email: {self.email}, GPA: {self.gpa}, Credit Hours: {self.credit_hours}"
    
     # ---------- Database Integration ----------
    def save_to_db(self):
      """
    Save the student into the database.
    If the student already exists (same email), print a message instead of inserting again.
    If the student_id exists, update instead.
    """
      db = DatabaseManager()
      conn = db.connect()
      cursor = conn.cursor()

    # Check if student already exists by email
      cursor.execute("SELECT * FROM Student WHERE email = ?", (self.email,))
      existing = cursor.fetchone()

      if existing and not self.student_id:
        print(f"Student with email '{self.email}' already exists.")
        conn.close()
        return

      if self.student_id:  # Existing student → update
        cursor.execute("""
            UPDATE Student 
            SET name = ?, email = ?, credit_hours = ? 
            WHERE student_id = ?
        """, (self.name, self.email, self.credit_hours, self.student_id))
      else:  # New student → insert
        cursor.execute("""
            INSERT INTO Student (name, email, credit_hours)
            VALUES (?, ?, ?)
        """, (self.name, self.email, self.credit_hours))

      conn.commit()
      conn.close()
      print(f"Student '{self.name}' saved successfully!")

    @staticmethod
    def get_all_students():
        """
        Retrieve all students from the database.
        """
        db = DatabaseManager()
        students = db.fetch_all("SELECT * FROM Student")
        db.close()
        return students

    @staticmethod
    def delete_student(student_id: int):
        """
        Delete a student by ID.
        """
        db = DatabaseManager()
        db.execute_query("DELETE FROM Student WHERE student_id=?", (student_id,))
        db.close()      
