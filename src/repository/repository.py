from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import ContactsModel
from src.schemas.schemas import ContactBase, ContactCreate, ContactUpdate, Contact
from typing import List, Optional
from sqlalchemy import select, extract
from sqlalchemy import or_, and_


async def create_contact(db: AsyncSession, contact: ContactCreate) -> Contact:
    """
    Створює нового користувача в базі даних.

    Args:
        db (AsyncSession): Сесія бази даних.
        user (UserCreate): Схема Pydantic з даними користувача.

    Returns:
        User: Об'єкт користувача з бази даних.
    """
    db_contact = ContactsModel(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone_number=contact.phone_number,
        birthday=contact.birthday,
        other_info=contact.other_info
    )
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact
   

async def get_contacts(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Contact]:
    """
    Повертає список всіх контактів з бази даних.

    Args:
        db (AsyncSession): Сесія бази даних.
        skip (int): Кількість записів, які потрібно пропустити (для пагінації).
        limit (int): Максимальна кількість записів для повернення.

    Returns:
        List[Contact]: Список об'єктів контактів.
    """
    stmt = select(ContactsModel).offset(skip).limit(limit)
    result = await db.execute(stmt)
    contacts = result.scalars().all()
    return contacts


async def get_contact_by_id(db: AsyncSession, contact_id: int) -> Contact | None:
    """
    Повертає один контакт за його ID.

    Args:
        db (AsyncSession): Сесія бази даних.
        contact_id (int): ID контакту.

    Returns:
        Contact | None: Об'єкт контакту або None, якщо його не знайдено.
    """
    # Запит до бази даних для отримання контакту за ID.
    return await db.get(ContactsModel, contact_id)


async def update_contact(db: AsyncSession, contact_id: int, body: ContactUpdate) -> Optional[Contact]:
    """
    Оновлює існуючий контакт у базі даних.

    Args:
        db (AsyncSession): Сесія бази даних.
        contact_id (int): ID контакту.
        body (ContactUpdate): Схема Pydantic з даними для оновлення.

    Returns:
        Optional[Contact]: Оновлений об'єкт контакту або None, якщо його не знайдено.
    """
    contact = await db.get(ContactsModel, contact_id)
    if contact:
        for field, value in body.model_dump(exclude_unset=True).items():
            setattr(contact, field, value)
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(db: AsyncSession, contact_id: int) -> Contact | None:
    """
    Видаляє контакт за його ID.

    Args:
        db (AsyncSession): Сесія бази даних.
        contact_id (int): ID контакту.

    Returns:
        Contact | None: Видалений об'єкт контакту або None, якщо його не знайдено.
    """
    db_contact = await db.get(ContactsModel, contact_id)

    if db_contact:
        await db.delete(db_contact)
        await db.commit()
        return db_contact 

    return None


async def search_contacts_repo(db: AsyncSession, filters: dict[str, str]) -> List[ContactsModel]:
    """
    Універсальний пошук контактів по 1 або кількох параметрах.
    Використовує OR між умовами (тобто знайде, якщо хоча б одне співпаде).
    """
    if not filters:
        return []

    conditions = []
    for field, value in filters.items():
        model_field = getattr(ContactsModel, field, None)
        if model_field is not None:
            conditions.append(model_field.ilike(f"%{value}%"))

    if not conditions:
        return []

    stmt = select(ContactsModel).filter(or_(*conditions))
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_contacts_upcoming_birthdays(db: AsyncSession) -> List[Contact]:
    today = date.today()
    future_date = today + timedelta(days=7)

    if today.month == future_date.month:
        # Easy option within one month
        stmt = (
            select(ContactsModel)
            .where(
                and_(
                    extract("month", ContactsModel.birthday) == today.month,
                    extract("day", ContactsModel.birthday).between(today.day, future_date.day),
                )
            )
        )
    else:
        # Transition in a month
        stmt = (
            select(Contact)
            .where(
                or_(
                    # Days between now and the end of the month
                    and_(
                        extract("month", Contact.birthday) == today.month,
                        extract("day", Contact.birthday) >= today.day,
                    ),
                    # Days from next month to future_date
                    and_(
                        extract("month", Contact.birthday) == future_date.month,
                        extract("day", Contact.birthday) <= future_date.day,
                    ),
                )
            )
        )

    result = await db.execute(stmt)
    return result.scalars().all()