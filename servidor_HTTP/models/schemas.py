from pydantic import BaseModel
from typing import Optional

#modelo de post
class Post(BaseModel):
    #atributos
    id: Optional[int] = None #campo opcional
    author: str
    date: str
    text: str

#modelo de usuario
class User(BaseModel):
    #atributos
    id: int
    username: str
    password: str