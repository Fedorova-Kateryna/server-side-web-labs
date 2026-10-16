from fastapi import FastAPI, status, HTTPException, Depends, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi.responses import JSONResponse
from . import db
from . import schemas
from . import storage

app = FastAPI(title="Users API", version="0.2.0")

@app.exception_handler(storage.EmailTakenError)
async def email_taken_exception_handler(request: Request, exc: storage.EmailTakenError):
    return JSONResponse(status_code=409, content={"detail": "Email already registered"})

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users", response_model=list[schemas.UserRead])
async def get_users(session: AsyncSession = Depends(db.get_session)):
    return await storage.get_users(session)

@app.get("/users/{user_id}", response_model=schemas.UserRead)
async def get_user_by_id(user_id: Annotated[int, Path(ge=1, le=2147483647)], session: AsyncSession = Depends(db.get_session)):
    user = await storage.get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user

@app.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(db.get_session)):
    try:
        result = await storage.create_user(session, user)
    except storage.EmailTakenError:
        raise storage.EmailTakenError()
    return result

@app.put("/users/{user_id}", response_model=schemas.UserRead)
async def replace_user(user_id: Annotated[int, Path(ge=1, le=2147483647)], user: schemas.UserCreate, session: AsyncSession = Depends(db.get_session)):
    try:
        result = await storage.replace_user(session, user_id, user)
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return result
    except storage.EmailTakenError:
        raise storage.EmailTakenError()

@app.patch("/users/{user_id}", response_model=schemas.UserRead)
async def update_partly_user(user_id: Annotated[int, Path(ge=1, le=2147483647)], user: schemas.UserUpdate, session: AsyncSession = Depends(db.get_session)):
    try:
        result = await storage.update_user(session, user_id, user)
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return result
    except storage.EmailTakenError:
        raise storage.EmailTakenError()

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: Annotated[int, Path(ge=1, le=2147483647)], session: AsyncSession = Depends(db.get_session)):
    result = await storage.delete_user(session, user_id)
    if result is False:
        raise HTTPException(404, "User not found")
