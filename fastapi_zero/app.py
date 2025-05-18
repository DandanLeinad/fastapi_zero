from http import HTTPStatus

from fastapi import FastAPI

from fastapi_zero.schemas import Message, UserSchema

app = FastAPI(title="FastAPI Zero")


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserSchema)
def create_user(user: UserSchema):
    return user
