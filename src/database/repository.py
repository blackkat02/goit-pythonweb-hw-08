import datetime

from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Student, Group, Teacher, Subject, Rating


# ---------- CREATE ----------
async def create_student(
    name: str, last_name: str, group_id: int, session: AsyncSession
):
    student = Student(student_name=name, student_last_name=last_name, group_id=group_id)
    session.add(student)
    await session.commit()
    await session.refresh(student)
    return student


async def create_group(name: str, session: AsyncSession):
    group = Group(group_name=name)
    session.add(group)
    await session.commit()
    await session.refresh(group)
    return group


async def create_teacher(name: str, session: AsyncSession):
    teacher = Teacher(teacher_name=name)
    session.add(teacher)
    await session.commit()
    await session.refresh(teacher)
    return teacher


async def create_subject(name: str, teacher_id: int, session: AsyncSession):
    subject = Subject(subject_name=name, teacher_id=teacher_id)
    session.add(subject)
    await session.commit()
    await session.refresh(subject)
    return subject


async def create_rating(
    student_id: int, subject_id: int, rating: int, session: AsyncSession
):
    record = Rating(
        student_id=student_id,
        subject_id=subject_id,
        rating=rating,
        date=datetime.date.today(),
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record


# ---------- READ ALL ----------
async def get_all_students(session: AsyncSession):
    result = await session.execute(select(Student))
    return result.scalars().all()


async def get_all_groups(session: AsyncSession):
    result = await session.execute(select(Group))
    return result.scalars().all()


async def get_all_teachers(session: AsyncSession):
    result = await session.execute(select(Teacher))
    return result.scalars().all()


async def get_all_subjects(session: AsyncSession):
    result = await session.execute(select(Subject))
    return result.scalars().all()


async def get_all_ratings(session: AsyncSession):
    result = await session.execute(select(Rating))
    return result.scalars().all()


# ---------- READ BY ID ----------
async def get_student_by_id(student_id: int, session: AsyncSession):
    result = await session.execute(select(Student).filter(Student.id == student_id))
    return result.scalar_one_or_none()


async def get_group_by_id(group_id: int, session: AsyncSession):
    result = await session.execute(select(Group).filter(Group.id == group_id))
    return result.scalar_one_or_none()


async def get_teacher_by_id(teacher_id: int, session: AsyncSession):
    result = await session.execute(select(Teacher).filter(Teacher.id == teacher_id))
    return result.scalar_one_or_none()


async def get_subject_by_id(subject_id: int, session: AsyncSession):
    result = await session.execute(select(Subject).filter(Subject.id == subject_id))
    return result.scalar_one_or_none()


async def get_rating_by_id(rating_id: int, session: AsyncSession):
    result = await session.execute(select(Rating).filter(Rating.id == rating_id))
    return result.scalar_one_or_none()


# ---------- SELECT QUERIES ----------


async def select_1(session: AsyncSession):
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    """
    stmt = (
        select(Student.student_name, func.avg(Rating.rating).label("avg_rating"))
        .join(Rating, Student.id == Rating.student_id)
        .group_by(Student.id)
        .order_by(text("avg_rating DESC"))
        .limit(5)
    )
    result = await session.execute(stmt)
    return result.all()


async def select_2(subject_name: str, session: AsyncSession):
    """
    Знайти студента з найвищим середнім балом з певного предмета.
    """
    stmt = (
        select(Student.student_name, func.avg(Rating.rating).label("avg_rating"))
        .join(Rating, Student.id == Rating.student_id)
        .join(Subject, Rating.subject_id == Subject.id)
        .where(Subject.subject_name == subject_name)
        .group_by(Student.id)
        .order_by(text("avg_rating DESC"))
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.first()


async def select_3(group_name: str, session: AsyncSession):
    """
    Знайти середній бал у групах з певного предмета.
    """
    stmt = (
        select(Group.group_name, func.avg(Rating.rating).label("avg_rating"))
        .join(Student, Group.id == Student.group_id)
        .join(Rating, Student.id == Rating.student_id)
        .where(Group.group_name == group_name)
        .group_by(Group.id)
    )
    result = await session.execute(stmt)
    return result.first()


async def select_4(session: AsyncSession):
    """
    Знайти середній бал на потоці (по всій базі даних).
    """
    stmt = select(func.avg(Rating.rating).label("avg_rating"))
    result = await session.execute(stmt)
    return result.first()


async def select_5(teacher_name: str, session: AsyncSession):
    """
    Знайти, які курси читає певний викладач.
    """
    stmt = (
        select(Subject.subject_name)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .where(Teacher.teacher_name == teacher_name)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_6(group_name: str, session: AsyncSession):
    """
    Знайти список студентів у певній групі.
    """
    stmt = (
        select(Student.student_name)
        .join(Group, Student.group_id == Group.id)
        .where(Group.group_name == group_name)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_7(group_name: str, subject_name: str, session: AsyncSession):
    """
    Знайти оцінки студентів у окремій групі з певного предмета.
    """
    stmt = (
        select(Student.student_name, Rating.rating)
        .join(Group, Student.group_id == Group.id)
        .join(Rating, Student.id == Rating.student_id)
        .join(Subject, Rating.subject_id == Subject.id)
        .where(Group.group_name == group_name)
        .where(Subject.subject_name == subject_name)
    )
    result = await session.execute(stmt)
    return result.all()


async def select_8(teacher_name: str, session: AsyncSession):
    """
    Знайти середній бал, який поставив певний викладач зі своїх предметів.
    """
    stmt = (
        select(func.avg(Rating.rating).label("avg_rating"))
        .join(Subject, Rating.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .where(Teacher.teacher_name == teacher_name)
    )
    result = await session.execute(stmt)
    return result.first()


async def select_9(student_id: int, session: AsyncSession):
    """
    Знайти список курсів, які відвідує студент.
    """
    stmt = (
        select(Subject.subject_name)
        .join(Rating, Subject.id == Rating.subject_id)
        .where(Rating.student_id == student_id)
        .group_by(Subject.id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_10(student_id: int, teacher_name: str, session: AsyncSession):
    """
    Список курсів, які певний викладач читає певному студенту.
    """
    stmt = (
        select(Subject.subject_name)
        .join(Rating, Subject.id == Rating.subject_id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .where(Rating.student_id == student_id)
        .where(Teacher.teacher_name == teacher_name)
        .group_by(Subject.id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()
