class Student():

    def __init__(self, student_number, first_name, last_name, year):
        self.student_number = student_number
        self.first_name = first_name
        self.last_name = last_name
        self.year = year

    def greet(self):
        return f"Hi, {self.first_name} {self.last_name}"

"""
The above is a pure domain entity.
This is a sample of a very django-coupled entity:

from django.db import models

class Student(models.Model):
    student_number = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    year = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    def greet(self):
        return f"Hi, {self.first_name} {self.last_name}"

    @classmethod
    def create_student(cls, student_number, first_name, last_name, year):
        student = cls(student_number=student_number, first_name=first_name, last_name=last_name, year=year)
        return student

"""