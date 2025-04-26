from typing import Optional
from pydantic import BaseModel


# modelo de post
class Post(BaseModel):
    # atributos
    id: Optional[int] = None  # campo opcional
    author: str
    date: str
    text: str


# modelo de usuario
class User(BaseModel):
    # atributos
    id: Optional[int] = None # campo opcional
    username: str
    password: str
