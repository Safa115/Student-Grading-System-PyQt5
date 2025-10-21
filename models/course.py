class Course:
    def __init__(self, course_id:int,course_name:str,credit_hours:int,instructor_id:int):
        self.course_id=course_id
        self.course_name=course_name
        self.credit_hours=credit_hours
        self.instructor_id=instructor_id
    #---------- Encapsulation ----------
    def get_course_id(self):
        return self.__course_id
    def set_course_id(self,course_id:int):
        self.__course_id=course_id

    def get_course_name(self):
        return self.__course_name
    def set_course_name(self,course_name:str):
        self.__course_name=course_name

    def get_credit_hours(self):
        return self.__credit_hours
    def set_credit_hours(self,credit_hours:int):
        if credit_hours >0:
            self.__credit_hours=credit_hours
        else:
            raise ValueError("Credit hours must be positive")
        

    def get_instructor_id(self):
        return self.__instructor_id
    def set_instructor_id(self,instructor_id:int):
        self.__instructor_id=instructor_id


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
    

