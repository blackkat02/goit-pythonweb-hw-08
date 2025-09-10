from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Contact
from src.schemas.schemas import ContactBase, ContactCreate, Contact

async def create_user(db: AsyncSession, user: ContactCreate) -> Contact:
    """
    Створює нового користувача в базі даних.

    Args:
        db (AsyncSession): Сесія бази даних.
        user (UserCreate): Схема Pydantic з даними користувача.

    Returns:
        User: Об'єкт користувача з бази даних.
    """
    # Створення екземпляра моделі SQLAlchemy з отриманих даних.
    db_user = Contact(**user.model_dump())
    
    # Додавання об'єкта до сесії та збереження в базі даних.
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

async def get_users(db: AsyncSession, id: Contact) -> Contact:
    """
    Створює нового користувача в базі даних.

    Args:
        db (AsyncSession): Сесія бази даних.
        user (UserCreate): Схема Pydantic з даними користувача.

    Returns:
        User: Об'єкт користувача з бази даних.
    """
    # Створення екземпляра моделі SQLAlchemy з отриманих даних.
    db_get_user = Contact(**user.model_dump())
    
    # Додавання об'єкта до сесії та збереження в базі даних.
    await db.get(model, id)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user
