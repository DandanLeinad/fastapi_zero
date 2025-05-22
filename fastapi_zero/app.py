from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)
from fastapi_zero.settings import Settings

app = FastAPI(title="FastAPI Zero")
database = []


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá, Mundo!"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    engine = create_engine(Settings().DATABASE_URL)
    session = Session(engine)

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists",
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already exists",
            )

    db_user = User(
        username=user.username,
        password=user.password,
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users/", status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {"users": database}


@app.get(
    "/users/{user_id}",
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def read_user(user_id: int):
    """
    Recupera um usuário por ID.
    """
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    return database[user_id - 1]


@app.put(
    "/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user: UserSchema, user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete(
    "/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    user = database.pop(user_id - 1)
    return user
