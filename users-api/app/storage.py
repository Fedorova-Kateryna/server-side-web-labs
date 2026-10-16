from datetime import datetime, UTC
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class EmailTakenError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code
        self.message = message

    def __str__(self):
        return f'{self.error_code}: {self.message}'

users = {}

next_id = 1

def check_unique_email(email: str, exclude_user_id: int = None):
    for user in users.values():
        if user['email'].lower() == email.lower() and user['id'] != exclude_user_id:
            raise EmailTakenError("Email already registered", 409)

async def create_user(data):
    global next_id
    current_id = next_id
    user_info = data.model_dump(exclude={"password"})
    check_unique_email(user_info["email"])
    user_info['id'] = current_id
    user_info['created_at'] = datetime.now(UTC)
    user_info['password_hash'] = password_hash.hash(data.password)
    users[current_id] = user_info
    next_id += 1
    return users[current_id]

async def get_users():
    return list(users.values())

async def get_user_by_id(user_id: int):
    return users.get(user_id)

async def update_user(user_id: int, user):
    current_user = users.get(user_id)
    if current_user is None:
        return None
    modified_data = user.model_dump(exclude_unset=True, exclude={"password"})
    if 'email' in modified_data:
        check_unique_email(modified_data["email"], user_id)
    if user.password is not None:
        current_user['password_hash'] = password_hash.hash(user.password)
    current_user.update(modified_data)
    return users[user_id]

async def replace_user(user_id: int, user):
    current_user = users.get(user_id)
    if current_user is None:
        return None

    updated_keys = user.model_dump(exclude={"password"})
    check_unique_email(updated_keys['email'], user_id)
    current_user['password_hash'] = password_hash.hash(user.password)
    for key in current_user:
        if key in updated_keys:
            current_user[key] = updated_keys[key]
    return users[user_id]

async def delete_user(user_id: int):
    try:
        users.pop(user_id)
        return True
    except KeyError:
        return False
