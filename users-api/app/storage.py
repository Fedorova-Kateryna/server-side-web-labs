from pwdlib import PasswordHash
from sqlalchemy import select
from . import models

password_hash = PasswordHash.recommended()

class EmailTakenError(Exception):
    pass


async def check_unique_email(session, email: str, exclude_user_id: int = None):
    if exclude_user_id is not None:
        result = await session.scalars(select(models.User).where(models.User.id != exclude_user_id, models.User.email == email.lower()))
    else:
        result = await session.scalars(select(models.User).where(models.User.email == email.lower()))
    if result.first() is not None:
        raise EmailTakenError("Email already registered", 409)

async def create_user(session, data):
    user_info = data.model_dump(exclude={"password"})
    await check_unique_email(session, user_info["email"])
    user = models.User(**user_info)
    user.password_hash = password_hash.hash(data.password)
    user.email = data.email.lower()
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_users(session):
    result = await session.scalars(select(models.User).order_by(models.User.id))
    return result.all()

async def get_user_by_id(session, user_id: int):
    result = await session.scalars(select(models.User).where(models.User.id == user_id))
    return result.first()

async def update_user(session, user_id: int, user):
    current_user = await get_user_by_id(session, user_id)
    if current_user is None:
        return None
    modified_data = user.model_dump(exclude_unset=True, exclude={"password"})
    if 'email' in modified_data:
        await check_unique_email(session, modified_data["email"], user_id)
        modified_data['email'] = user.email.lower()
    if user.password is not None:
        modified_data['password_hash'] = password_hash.hash(user.password)
    for key, value in modified_data.items():
        setattr(current_user, key, value)

    await session.commit()
    await session.refresh(current_user)
    return current_user

async def replace_user(session, user_id: int, user):
    current_user = await get_user_by_id(session, user_id)
    if current_user is None:
        return None

    updated_keys = user.model_dump(exclude={"password"})
    await check_unique_email(session, updated_keys['email'], user_id)
    updated_keys['password_hash'] = password_hash.hash(user.password)
    updated_keys['email'] = user.email.lower()
    for key, value in updated_keys.items():
        setattr(current_user, key, value)
    await session.commit()
    await session.refresh(current_user)
    return current_user

async def delete_user(session, user_id: int):
    current_user = await get_user_by_id(session, user_id)
    if current_user is None:
        return False
    await session.delete(current_user)
    await session.commit()
    return True
