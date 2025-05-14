from http import HTTPStatus

from fastapi_zero.schemas import Message
from fastapi import FastAPI

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}
