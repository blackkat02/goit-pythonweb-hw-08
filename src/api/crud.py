from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database.db import get_async_session
from src.schemas.schemas import ContactBase, ContactCreate, Contact
from src.repository import create_user, get_users, get_user_by_id, update_user, delete_user

# Створення роутера для користувачів.
router = APIRouter(prefix="/users", tags=["users"])

# 1. POST - Створення нового користувача (C - Create)
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_new_user(user_in: UserCreate, db: AsyncSession = Depends(get_async_session)):
    """
    Створює нового користувача.
    """
    # Виклик функції репозиторію для створення користувача в базі даних.
    db_user = await create_user(db, user_in)
    return db_user

# 2. GET - Отримання списку всіх користувачів (R - Read)
@router.get("/", response_model=List[Contact])
async def read_users(db: AsyncSession = Depends(get_async_session)):
    """
    Повертає список всіх користувачів.
    """
    users = await get_users(db)
    return users

# 3. GET - Отримання конкретного користувача за ID (R - Read)
@router.get("/{user_id}", response_model=Contact)
async def read_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    """
    Повертає одного користувача за його ID.
    """
    db_user = await get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Користувача не знайдено.")
    return db_user

# 4. PUT - Оновлення даних користувача (U - Update)
@router.put("/{user_id}", response_model=UserRead)
async def update_existing_user(user_id: int, user_update: UserCreate, db: AsyncSession = Depends(get_async_session)):
    """
    Оновлює дані існуючого користувача.
    """
    updated_user = await update_user(db, user_id, user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Користувача не знайдено.")
    return updated_user

# 5. DELETE - Видалення користувача (D - Delete)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    """
    Видаляє користувача.
    """
    deleted = await delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Користувача не знайдено.")
    return {"message": "Користувача видалено."}
