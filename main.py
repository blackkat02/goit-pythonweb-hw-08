from fastapi import FastAPI
import logging

app = FastAPI()


@app.get("/")
def read_root():
    response = {"message": "Welcome to FastAPI"}
    return response
