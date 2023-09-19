# Loosely coupled ORM usage in python

This is a sample repository showing how we can use pure domain models with SQLAlchemy in python.

## Running the tests

- Create a virtual environment by running `python -m venv venv`
- Install the dependencies by running `pip install -r requirements.txt`
- Run tests using your IDE or `python -m pytest`

## Architecture

![Class diagram of the project](http://www.plantuml.com/plantuml/svg/dLFDRjiy4BphANYBV50U88SW-69yG4u5cXGz6WmvbbdpXo6NJTNKxrwgLXA9KeIYF1ZmpEnobfgzYSG39QEhU5JMyy0Dqyg2EW_c0XrSTL0I3CPJnmpC8qAigWlckJZo5cmB3ojXHRVxFm3ifQfOFg_qhGjdR3X2ynZPFQLSGfbWenFFwCwc_fQh_3yesquaUnLY5d23HLhpDRO3prsL9RG8rOHg0q3rPbPsUfVrTM7F1TXdU1SLkT0L0uW0JgXXIL6tcL39ouye2OqFg00kQoMdu5D2w6eV89NWXCswsIzMqQVzLnUEfLbdZCepJq7j8aROgVnoMtVl3EYWRFlWXiyOYyxu0P48zPloDb_5hMJ2oCNMemTjhiUEhrXopsVTQPghNlI0sDzTEAICxeoJIMFgwyneroencN3eNbtqlylpDStroEIAQFXJlTjhf7kscUaNOGHVzl3b6SvZtjbl41dUyoDOUBr9OM7LkALooRR_pLvXoua_yeWxgqXnhNuY5A_n4ecJ4YUctYIrSDP2a79sTrw4pMB94FHTH8nPMsIeQLQBvE2i_g1tW77V_qPMz5jBxVsJviKYh2WNz_kqbC8xIsW3xn_idyBe4QAA12imZ-IGoC9xatppQxmaLM5v4BmZCq5GxO5o97jylcopcHgDVPRdb2rmoRzcUqvU9ZzFU6667FkpaLLr0okJqRy1)

## Why?

We want to keep our domains as free of dependencies as possible.
This enables us to let our domain specific code live on for ages,
disregarding the current buzz in the developer space. Frameworks come and go, but our code needs to live on.

This example shows how to keep a _completely pure_ python domain entity,
while still using SQLAlchemy to persist and query a database for the entity.

Here's the pure class:

```python
class Student():
    """
    A Student is the main logic class of our system.
    It's important to keep it as readable, maintainable and free of dependencies as possible.
    """

    def __init__(self, student_number, first_name, last_name, year):
        self.student_number = student_number
        self.first_name = first_name
        self.last_name = last_name
        self.year = year

    def greet(self):
        """
        :return: An iunformal greeting of the student
        """
        return f"Hi, {self.first_name} {self.last_name}"
```

This class has absolutely no external dependencies and should be compatible with python 20.  
It stands as a clear counterpart to the followin Django-bound entity; that has a parameterless constructor
imposed upon it in favor of a static factory method, and each field is initialized using
tightly coupled factory methods for metadata _and_ value instances.  
It clearly violates all of the SOLID principles all in one nice package. 

```python
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
```

Granted there are valuable information in the django-bound class like last names having
a maximum length of 30. However, those rules are frequently very use-case and customer governed.
A last name in the UK has totally different qualities than a last name in India or other parts of Asia.
By moving these rules into _metadata_ specific classes _per solution_ we can leverage a larger flexibility.
Here's an example of moving the metadata out of the entity:

```python
student_table = Table(
    'students',
    cls.metadata,
    Column('student_number', String, primary_key=True),
    Column('first_name', String(50)),
    Column('last_name', String(50)),
    Column('year', Integer, CheckConstraint('year >= 1 '))
)
registry().map_imperatively(Student, student_table, primary_key=student_table.c.student_number)
```

## Traditional misunderstandings

Traditional misunderstandings around the difficulties of "onion architecture" and 
"loosesly coupled ORM usage" involve

- You'll need a method per query on entity-specific repositories
- You'll never replace your persistence mechanism
- The built-in classes already implement UnitOfWork and Repository

This example shows that the effort is no bigger and that the generalizations
leave our freedom in place, except our freedom is bigger since we _can_ replace each individual
class' persistence mechanisms on a whim. Provided of course our mechanism supports
the five Repository methods: create, read, update, delete and query.