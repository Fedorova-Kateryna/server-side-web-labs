from fastapi import FastAPI, status, HTTPException
from . import schemas
from . import storage

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users", response_model=list[schemas.UserRead])
async def get_users():
    return await storage.get_users()

@app.get("/users/{user_id}", response_model=schemas.UserRead)
async def get_user_by_id(user_id: int):
    user = await storage.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        return user

@app.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate):
    try:
        result = await storage.create_user(user)
    except storage.EmailTakenError:
        raise HTTPException(status_code=409, detail="Email already registered")
    return result

@app.put("/users/{user_id}", response_model=schemas.UserRead)
async def replace_user(user_id: int, user: schemas.UserCreate):
    try:
        result = await storage.replace_user(user_id, user)
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return result
    except storage.EmailTakenError:
        raise HTTPException(status_code=409, detail="Email already registered")

@app.patch("/users/{user_id}", response_model=schemas.UserRead)
async def update_partly_user(user_id: int, user: schemas.UserUpdate):
    try:
        result = await storage.update_user(user_id, user)
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return result
    except storage.EmailTakenError:
        raise HTTPException(status_code=409, detail="Email already registered")

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    result = await storage.delete_user(user_id)
    if result is False:
        raise HTTPException(404, "User not found")
