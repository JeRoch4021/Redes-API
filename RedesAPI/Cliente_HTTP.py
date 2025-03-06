from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/")
def index():
    return "Hola mundo"

SERVER_URL = "http://0.0.0.0:8080/data"

@app.get("/get-data")
async def get_data():
    async with httpx.AsyncClient() as cliente:
        respuesta = await cliente.get(SERVER_URL)
        return respuesta.json()
    
