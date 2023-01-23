# shortener_app/main.py

import secrets

import validators
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import schemas, models
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.get("/")
def read_root():
    return "Hi, welcome to the smart URL shortener API ;-)"

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    # to make sure it is actually a valid URL
    # pydantic makes sure it is a string that comes in while validator makes sure it is a valid URL
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url