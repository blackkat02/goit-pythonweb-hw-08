from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import ContactsModel
from src.schemas.schemas import ContactBase, ContactCreate, ContactUpdate, Contact
from typing import List, Optional
from sqlalchemy import select


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

    
async def get_contact_by_last_name(db: AsyncSession, contact_id: int) -> Contact | None:
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

