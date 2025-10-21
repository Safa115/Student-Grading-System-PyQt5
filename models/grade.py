class Grade:
    def __init__(self,student_id:int,course_id:int,grade:float):
        self.student_id=student_id
        self.course_id=course_id
        self.grade=grade
    #---------- Encapsulation ----------
    def get_student_id(self):
        return self.__student_id
    def set_student_id(self,student_id:int):
        self.__student_id=student_id


    def get_course_id(self):
        return self.__course_id
    def set_course_id(self,course_id:int):
        self.__course_id=course_id


    def get_grade(self):
        return self.__grade
    def set_grade(self,grade:float):
        if 0.0<=grade<=100.0:
            self.__grade=grade
        else:
            raise ValueError("Grade must be between 0.0 and 100.0")
        
    #---------- Additional Methods ----------
    def calculate_grade_points(self):
        """
        Placeholder method for calculating grade points.
        Later will implement based on grading scale.
        """
        pass

    def get_letter_grade(self):
        """
        Placeholder method for converting numeric grade to letter grade.
        """
        pass
    
    def __str__(self):
        """
        Returns a readable representation of the grade.
        """
        return f"Grade(Student ID: {self.student_id}, Course ID: {self.course_id}, Grade: {self.grade})"

