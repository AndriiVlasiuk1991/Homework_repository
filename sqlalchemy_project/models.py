from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime

engine = create_engine('sqlite:///sqlalchemy_example.db')

Base = declarative_base()


# Модель таблиці "Студенти"
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))

    group = relationship('Group', back_populates='students')
    grades = relationship('Grade', back_populates='student')


# Модель таблиці "Групи"
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    students = relationship('Student', back_populates='group')


# Модель таблиці "Викладачі"
class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    subjects = relationship('Subject', back_populates='teacher')


# Модель таблиці "Предмети"
class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))

    teacher = relationship('Teacher', back_populates='subjects')
    grades = relationship('Grade', back_populates='subject')


# Модель таблиці "Оцінки"
class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))

    student = relationship('Student', back_populates='grades')
    subject = relationship('Subject', back_populates='grades')


# Створення таблиць у базі даних
Base.metadata.create_all(engine)

# Створення сесії для роботи з базою даних
Session = sessionmaker(bind=engine)
session = Session()