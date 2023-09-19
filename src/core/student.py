class Student():

    def __init__(self, student_number, first_name, last_name, year):
        self.student_number = student_number
        self.first_name = first_name
        self.last_name = last_name
        self.year = year

    def greet(self):
        return "Hi, " + self.first_name + " " + self.last_name

