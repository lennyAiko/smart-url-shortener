# shortener_app/main.py

import validators
from fastapi import FastAPI, HTTPException

from . import schemas

app = FastAPI()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.get("/")
def read_root():
    return "Hi, welcome to the smart URL shortener API ;-)"

@app.post("/url")
def create_url(url: schemas.URLBase):
    # to make sure it is actually a valid URL
    # pydantic makes sure it is a string that comes in while validator makes sure it is a valid URL
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
    return f"TODO: Create database entry for: {url.target_url}"