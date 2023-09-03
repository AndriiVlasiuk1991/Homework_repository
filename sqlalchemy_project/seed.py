from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from models import Student, Group, Teacher, Subject, Grade
from random import randint, choice

db_url = 'sqlite:///mynotes.db'

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

groups = [Group(name=f"Group {i}") for i in range(1, 4)]

teachers = [Teacher(name=fake.name()) for _ in range(5)]

subjects = [Subject(name=fake.word(), teacher=choice(teachers)) for _ in range(8)]

students = []
for _ in range(randint(30, 50)):
    student = Student(name=fake.name(), group=choice(groups))
    students.append(student)
    session.add(student)

for student in students:
    for subject in subjects:
        for _ in range(randint(1, 4)):
            date = fake.date_time_between(start_date='-1y', end_date='now')
            grade = Grade(value=randint(60, 100), date=date, student=student, subject=subject)
            session.add(grade)


session.commit()


session.close()