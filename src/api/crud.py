from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database.db import get_async_session
from src.schemas.schemas import ContactBase, ContactCreate, Contact, ContactUpdate
from src.repository import create_contact, get_contacts, get_contact_by_id, update_contact, delete_contact

# Створення роутера для користувачів.
router = APIRouter(prefix="/contacts", tags=["contacts"])

# 1. POST - Створення нового користувача (C - Create)
@router.post("/", response_model=Contact, status_code=status.HTTP_201_CREATED)
async def create_new_contact(contact_in: ContactCreate, db: AsyncSession = Depends(get_async_session)):
    """
    Створює нового користувача.
    """
    # Виклик функції репозиторію для створення користувача в базі даних.
    db_contact = await create_contact(db, contact_in)
    return db_contact

# 2. GET - Отримання списку всіх користувачів (R - Read)
@router.get("/", response_model=List[Contact])
async def get_all_contacts(db: AsyncSession = Depends(get_async_session)):
    """
    Повертає список всіх користувачів.
    """
    contacts = await get_contacts(db)
    return contacts

#3 get_user_by_id
@router.get("/{contact_id}", response_model=Contact)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_async_session)):
    """
    Повертає один контакт за його ID.
    """
    db_contact = await get_contact_by_id.get_contact_by_id(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено.")
    return db_contact

# 4. PUT - Оновлення даних користувача (U - Update)
@router.put("/{contact_id}", response_model=ContactUpdate)
async def update_existing_user(contact_id: int, contact_update: ContactUpdate, db: AsyncSession = Depends(get_async_session)):
    """
    Оновлює дані існуючого користувача.
    """
    updated_contact = await update_contact(db, contact_id, contact_update)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Користувача не знайдено.")
    return updated_contact

# 5. DELETE - Видалення користувача (D - Delete)
@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_contact(contact_id: int, db: AsyncSession = Depends(get_async_session)):
    """
    Видаляє користувача.
    """
    deleted = await delete_contact(db, contact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Користувача не знайдено.")
    return {"message": "Користувача видалено."}
