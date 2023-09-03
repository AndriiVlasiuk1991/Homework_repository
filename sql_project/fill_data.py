from datetime import datetime
from faker import Faker
from random import randint, choice
import sqlite3

fake = Faker()


def create_random_students(num_students):
    students = []
    for _ in range(num_students):
        students.append((
            fake.first_name(),
            fake.last_name(),
            randint(1980, 2007)
        ))
    return students


def create_random_professors(num_professors):
    professors = []
    for _ in range(num_professors):
        professors.append((
            fake.first_name(),
            fake.last_name()
        ))
    return professors


def create_random_groups(num_groups):
    groups = []
    for _ in range(num_groups):
        groups.append((
            fake.word().upper(),
        ))
    return groups


def create_random_subjects(num_subjects, professors):
    subjects = []
    for _ in range(num_subjects):
        subjects.append((
            fake.word().capitalize(),
            choice(professors)[0]
        ))
    return subjects


def create_random_grades(students, subjects):
    grades = []
    for student in students:
        for subject in subjects:
            grades.append((
                student[0],
                subject[0],
                randint(1, 100),
                fake.date_between(start_date="-1y", end_date="today")
            ))
    return grades


def populate_database():
    num_students = 50
    num_groups = 3
    num_subjects = 8
    num_professors = 5

    con = sqlite3.connect('salary.db')
    cur = con.cursor()

    # Заповнення Students
    students = create_random_students(num_students)
    students_with_group = [(first_name, last_name, birth_year, randint(1, num_groups)) for
                           first_name, last_name, birth_year in students]
    cur.executemany("INSERT INTO Students (FirstName, LastName, BirthYear, GroupID) VALUES (?, ?, ?, ?)",
                    students_with_group)
    con.commit()

    # Заповнення Groups
    groups = create_random_groups(num_groups)
    cur.executemany("INSERT INTO Groups (GroupName) VALUES (?)", groups)
    con.commit()

    # Заповнення Professors
    professors = create_random_professors(num_professors)
    cur.executemany("INSERT INTO Professors (FirstName, LastName) VALUES (?, ?)", professors)
    con.commit()

    # Заповнення Subjects
    subjects = create_random_subjects(num_subjects, professors)
    cur.executemany("INSERT INTO Subjects (SubjectName, ProfessorID) VALUES (?, ?)", subjects)
    con.commit()

    # Заповнення Grades
    students = cur.execute("SELECT StudentID FROM Students").fetchall()
    subjects = cur.execute("SELECT SubjectID FROM Subjects").fetchall()
    grades = create_random_grades(students, subjects)
    cur.executemany("INSERT INTO Grades (StudentID, SubjectID, Grade, GradeDate) VALUES (?, ?, ?, ?)", grades)
    con.commit()

    con.close()

if __name__ == '__main__':
    populate_database()
