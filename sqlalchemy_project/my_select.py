from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Subject, Teacher, Group

db_url = 'sqlite:///mynotes.db'

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()


def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    top_students = (
        session.query(Student, func.avg(Grade.value).label('average_grade'))
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .limit(5)
        .all()
    )
    return top_students


def select_2(subject_name):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    top_student = (
        session.query(Student, func.avg(Grade.value).label('average_grade'))
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .first()
    )
    return top_student


def select_3(subject_name):
    """Знайти середній бал у групах з певного предмета."""
    average_grades_by_group = (
        session.query(Group, func.avg(Grade.value).label('average_grade'))
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.name == subject_name)
        .group_by(Group.id)
        .all()
    )
    return average_grades_by_group


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    average_grade_overall = (
        session.query(func.avg(Grade.value).label('average_grade'))
        .scalar()
    )
    return average_grade_overall


def select_5(teacher_name):
    """Знайти, які курси читає певний викладач."""
    courses_taught_by_teacher = (
        session.query(Subject.name)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Teacher.name == teacher_name)
        .distinct()
        .all()
    )
    return courses_taught_by_teacher


def select_6(group_name):
    """Знайти список студентів у певній групі."""
    students_in_group = (
        session.query(Student)
        .join(Group, Student.group_id == Group.id)
        .filter(Group.name == group_name)
        .all()
    )
    return students_in_group


def select_7(group_name, subject_name):
    """Знайти оцінки студентів в окремій групі з певного предмета."""
    grades_in_group_subject = (
        session.query(Student, Grade)
        .join(Group, Student.group_id == Group.id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return grades_in_group_subject


def select_8(teacher_name):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    average_teacher_grades = (
        session.query(func.avg(Grade.value).label('average_grade'))
        .join(Subject, Subject.id == Grade.subject_id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    return average_teacher_grades


def select_9(student_name):
    """Знайти список курсів, які відвідує певний студент."""
    courses_attended_by_student = (
        session.query(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Student.id == Grade.student_id)
        .filter(Student.name == student_name)
        .distinct()
        .all()
    )
    return courses_attended_by_student


def select_10(student_name, teacher_name):
    """Список курсів, які певному студенту читає певний викладач."""
    courses_taught_to_student_by_teacher = (
        session.query(Subject.name)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Student.id == Grade.student_id)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .distinct()
        .all()
    )
    return courses_taught_to_student_by_teacher

def select_11(teacher_name, student_name):
    """Середній бал, який певний викладач ставить певному студентові."""
    average_teacher_grades_to_student = (
        session.query(func.avg(Grade.value).label('average_grade'))
        .join(Subject, Subject.id == Grade.subject_id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .join(Student, Student.id == Grade.student_id)
        .filter(Teacher.name == teacher_name, Student.name == student_name)
        .scalar()
    )
    return average_teacher_grades_to_student


def select_12(group_name, subject_name):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""
    last_lecture_grades = (
        session.query(Student, Grade)
        .join(Group, Student.group_id == Group.id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .order_by(Grade.date.desc())
        .all()
    )
    return last_lecture_grades


if __name__ == "__main__":
    result_1 = select_1()
    print("Select 1:")
    for student, average_grade in result_1:
        print(f"Student Name: {student.name}, Average Grade: {average_grade:.2f}")

    result_2 = select_2("site")
    print("\nSelect 2:")
    if result_2:
        student, average_grade = result_2
        print(f"Student Name: {student.name}, Average Grade: {average_grade:.2f}")
    else:
        print("No data found.")

    result_3 = select_3("attorney")
    print("\nSelect 3:")
    for group, average_grade in result_3:
        print(f"Group Name: {group.name}, Average Grade: {average_grade:.2f}")

    result_4 = select_4()
    print("\nSelect 4:")
    print(f"Overall Average Grade: {result_4:.2f}")

    result_5 = select_5("Melissa Smith")
    print("\nSelect 5:")
    if result_5:
        for course in result_5:
            print(course[0])
    else:
        print("No courses found.")

    result_6 = select_6("Group 1")
    print("\nSelect 6:")
    for student in result_6:
        print(f"Student Name: {student.name}")

    result_7 = select_7("Group 2", "admit")
    print("\nSelect 7:")
    for student, grade in result_7:
        print(f"Student Name: {student.name}, Grade: {grade.value}")

    result_8 = select_8("Christopher Burton")
    print("\nSelect 8:")
    print(f"Average Grade: {result_8:.2f}")

    result_9 = select_9("Chris Yoder")
    print("\nSelect 9:")
    for course in result_9:
        print(course[0])

    result_10 = select_10("Ashley Cruz", "Colton Harris")
    print("\nSelect 10:")
    for course in result_10:
        print(course[0])

    result_11 = select_11("Christopher Burton", "Lori Nguyen")
    print("\nSelect 11:")
    print(f"Average Grade: {result_11:.2f}")

    result_12 = select_12("Group 3", "attorney")
    print("\nSelect 12:")
    for student, grade in result_12:
        print(f"Student Name: {student.name}, Grade: {grade.value}")

    session.close()
