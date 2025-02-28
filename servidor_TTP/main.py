#zona de imports
from typing import Union
from fastapi import FastAPI

#aplicacion
app = FastAPI()

#rutas y funciones
@app.get("/")
def read_root():
    return {"Hola":"Mundo"}

@app.get("/items/{item_id}")
def read_item(item_id:int, q:Union[str,None] = None):
    return {"item_id":item_id,"q":q}