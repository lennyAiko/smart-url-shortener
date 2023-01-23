# shortener_app/main.py

import secrets

import validators
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import schemas, models, crud
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

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
    
    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key

    return db_url

@app.get("/{url_key}")
def forward_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)
    ):
    # := is like a short form of list comprehension, assignment expression, 
    # The := operator is colloquially known as the walrus operator and gives you a new syntax for assigning variables in the middle of expressions.
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)