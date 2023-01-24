# shortener_app/schemas.py

from pydantic import BaseModel
from typing import Optional

class URLBase(BaseModel):
    target_url: str
    custom_key: Optional[str]

class URL(URLBase):
    is_active: bool
    clicks: int

    class Config:
        orm_mode = True # object relational mapping mode, for interacting with the db

class URLInfo(URL):
    url: str
    admin_url: str