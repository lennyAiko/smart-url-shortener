# shortener_app/main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "Hi, welcome to the smart URL shortener API ;-)"