from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from typing import List
from src.database.db import get_async_session
from src.schemas.schemas import ContactCreate, Contact, ContactUpdate
from src.repository.repository import create_contact, get_contacts, get_contact_by_id, update_contact, delete_contact
from src.repository.repository import search_contact_single, search_contact_multi, get_contacts_upcoming_birthdays

router = APIRouter(prefix="/contacts", tags=["contacts"])


# 1. POST - Створення нового контакту (C - Create)
@router.post("/", response_model=ContactCreate, status_code=status.HTTP_201_CREATED)
async def create_new_contact(contact_in: ContactCreate, db: AsyncSession = Depends(get_async_session)):
    """
    Створює новий контакт.
    """
    db_contact = await create_contact(db, contact_in)
    return db_contact


# 2. GET - Отримання списку всіх контактів з пагінацією (R - Read)
@router.get("/", response_model=List[Contact])
async def get_all_contacts(
    db: AsyncSession = Depends(get_async_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """
    Повертає список всіх контактів з підтримкою пагінації.
    """
    contacts = await get_contacts(db, skip=skip, limit=limit)
    return contacts


# 3. GET - Отримання одного контакту за ID (R - Read)
@router.get("/{contact_id}", response_model=Contact)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_async_session)):
    """
    Повертає один контакт за його ID.
    """
    db_contact = await get_contact_by_id(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено.")
    return db_contact

    

# 4. PATCH - Оновлення даних контакту (U - Update)
@router.patch("/{contact_id}", response_model=ContactUpdate)
async def update_existing_contact(
    contact_id: int, 
    contact_update: ContactUpdate, 
    db: AsyncSession = Depends(get_async_session)
):
    """
    Оновлює дані існуючого контакту.
    """
    updated_contact = await update_contact(db, contact_id, contact_update)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено.")
    return updated_contact


# 5. DELETE - Видалення контакту (D - Delete)
@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_contact(contact_id: int, db: AsyncSession = Depends(get_async_session)):
    """
    Видаляє контакт.
    """
    deleted = await delete_contact(db, contact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Контакт не знайдено.")
    return None


# 6. GET - Отримання одного контакту за first_name або  last_name або email, 
# також є опція пошуку по 1,2,3 параметрам багато контактів
@router.post("/search", response_model=list[Contact])
async def search_contacts(
    query: dict,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Універсальний пошук:
    - якщо query має 1 ключ → пошук по одному параметру
    - якщо кілька ключів → пошук по кількох параметрах
    """
    if not query:
        raise HTTPException(status_code=400, detail="Не передано жодного параметра пошуку.")

    if len(query) == 1:
        field, value = next(iter(query.items()))
        contacts = await search_contact_single(db, field, value)
    else:
        contacts = await search_contact_multi(db, query)

    if not contacts:
        raise HTTPException(status_code=404, detail="Контакт(и) не знайдено.")

    return contacts


# 6. GET - Отримання списку контактів з днями народження на найближчі 7 днів.
# @router.post("/search", response_model=list[Contact])
# def get_day_of_year_int() -> int:
#     """Get current day of year (1-365/366)"""
#     now = datetime.datetime.now()
#     return int(now.strftime("%j"))


# def get_current_year() -> int:
#     """Get current year"""
#     return datetime.datetime.now().year


# @router.get("/upcoming-birthdays", response_model=list[Contact])
# async def upcoming_birthdays(db: AsyncSession = Depends(get_async_session)):
#     """
#     Returns all contacts with birthdays in the next 7 days.
#     """
#     return await get_contacts_next_7_days(db)
    
# @router.get("/upcoming-birthdays", response_model=List[Contact])
# async def get_upcoming_birthdays_endpoint(
#     days: int = 7,
#     db: AsyncSession = Depends(get_async_session)
# ):
#     """
#     Отримати контакти з майбутніми днями народження.
    
#     Args:
#         days: Кількість днів для перегляду вперед (макс. 365)
#     """
#     if days < 1 or days > 365:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Days parameter must be between 1 and 365"
#         )
    
#     try:
#         contacts = await get_upcoming_birthdays(db, days)
#         return contacts
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error retrieving upcoming birthdays: {str(e)}"
#         )

@router.get("/upcoming_birthdays/", response_model=List[Contact])
async def get_coming_birthday_contacts(db: AsyncSession = Depends(get_async_session)):
    return await get_contacts_upcoming_birthdays(db)