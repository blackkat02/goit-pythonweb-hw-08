from sqlalchemy import Column, Integer, String, ForeignKey, DATE
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String, nullable=False)
    student_last_name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    ratings = relationship("Rating", back_populates="student")
    group = relationship("Group", back_populates="students")


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_name = Column(String, nullable=False)
    subjects = relationship("Subject", back_populates="teacher")


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String, nullable=False, unique=True)
    students = relationship("Student", back_populates="group")


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    date = Column(DATE, default=date.today)
    student = relationship("Student", back_populates="ratings")
    subject = relationship("Subject", back_populates="ratings")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String, nullable=False, unique=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="subjects")
    ratings = relationship("Rating", back_populates="subject")
