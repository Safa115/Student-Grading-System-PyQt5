from models.person import Person
class Instructor(Person):
    """
    class representing an instructor, inheriting from person.
    """
    def __init__(self, name, email,instructor_id:int,department:str):
        super().__init__(name, email)
        self.instructor_id=instructor_id
        self.department=department
        #----------Encapsulation----------
    def get_instructor_id(self):
      return self.__instructor_id
    def set_instructor_id(self,instructor_id:int):
       self.__instructor_id=instructor_id


    def get_department(self):
       return self.__department
    def set_department(self,department:str):
     self.__department=department


            #---------- Additional Methods----------
    def assign_grade(self,student,cource,grade):
                """
                Placeholder method for assigning a grade to a student for a course.
                """
                pass
        
    def __str__(self):
          """
         Returns a readable representation of the instructor.
          """
          return f"Instructor(ID: {self.instructor_id}, Name: {self.name}, Department: {self.department})"

        

