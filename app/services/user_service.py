from schemas.user_request import UserCreate
from schemas.user_response import UserResponse

users_db = []
user_id_counter = 1

def create_user(user: UserCreate) -> UserResponse:
    global user_id_counter

    new_user = UserResponse(
        id=user_id_counter,
        name=user.name,
        age=user.age
    )

    users_db.append(new_user)
    user_id_counter += 1
    return new_user


def get_all_users():
    return users_db


def get_user_by_id(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    return None
