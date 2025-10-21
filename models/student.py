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
    def calculate_gpa(self):
           """
        Placeholder method for GPA calculation.
        Later will calculate based on student's grades and credit hours.
        """
           pass
    def __str__(self):
           """
        Returns a readable representation of the student.
        """
           return f"Student(ID: {self.student_id}, Name: {self.name},GPA: {self.gpa})"
    
     # ---------- Database Integration ----------
    def save_to_db(self):
        """
        Save the student into the database.
        If the student already exists, update instead.
        """
        db = DatabaseManager()
        if self.student_id:  # Existing student → update
            db.execute_query("""
                UPDATE Student SET name=?, email=?, credit_hours=? WHERE student_id=?
            """, (self.name, self.email, self.credit_hours, self.student_id))
        else:  # New student → insert
            db.execute_query("""
                INSERT INTO Student (name, email, credit_hours) VALUES (?, ?, ?)
            """, (self.name, self.email, self.credit_hours))
        db.close()

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
