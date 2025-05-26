# zona de imports
import os
import logging
from typing import List

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import status

from models.schemas import Post, User
from services.database import DatabaseService

posts = []

# aplicacion
app = FastAPI()

# configuracion del loggin level del servidor
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# documentacion de la aplicacion
app.title = "Servidor http con fastapi"
app.version = "0.0.1"

# servicios
db_service = DatabaseService()

# rutas y funciones
# ruta principal
@app.get("/", tags=["Home"])  # tags indica agrupacion de rutas
def get_home() -> HTMLResponse:
    response = """
                <h1>Primer proyecto con fastapi</h1>
                <p>
                    Proyecto para la materia de topicos para
                    el despliegue de paplicaciones de la carrera
                    de ingenieria en sistemas.
                </p>
                """
    if db_service.isConnected():
        response += f"<h2>Conectado a base de datos!!!!</h2>"
        logger.debug("esta es la pagina web!!!")
    else:
        response += f"<h2>No hay conexion a base de datos!!!!</h2>"
    # puede retornar un json (dict) o str o html
    return HTMLResponse(response)


# ruta get principal
@app.get("/posts", tags=["Posts"])
def get_posts() -> List[Post]:
    return db_service.getPosts()


# ruta con parametros
@app.get("/post/{post_id}", tags=["Posts"])
def get_post(post_id: int) -> Post:
    # busqueda de post
    post = db_service.getPost(post_id)

    if not post:
        raise HTTPException(detail="Post no encontrado", status_code=404)
    
    return post


# ruta con parametros normal y query (clave-valor)
@app.get("/post/", tags=["Posts"])
def get_postq(author: str) -> List[Post]:
    # retorno de lista con los posts
    aposts = db_service.getPostByAuthor(author)

    if not aposts:
        raise HTTPException(detail="Autor no encontrado", status_code=404)
        
    return aposts


# ruta post para subir un nuevo post
@app.post("/posts", status_code=201)
def create_post(
    # body ayuda a convertir los valores a valores dentro del cuerpo de la peticion
    # id:int = Body(),
    # author:str = Body(),
    # date:str = Body(),
    # post:str = Body()
    post: Post,
):
    # volcar el modelo a diccionario
    # posts.append(post.model_dump())
    post_creado = db_service.createPost(post)
    
    if not post_creado:
        raise HTTPException(detail="Error al crear el post", status_code=500)
    else:
        return {"post": post_creado}


# ruta put para modificar los datos de un post
@app.put("/posts/{post_id}", tags=["Posts"])
def update_post(
    post_id: int,
    # author:str = Body(),
    # date:str = Body(),
    # post:str = Body()
    post: Post,
):
    post_modificado = db_service.updatePost(post_id, post)

    if not post_modificado:
        raise HTTPException(detail="El post no se pudo actualizar", status_code=404)
    else:
        return {"post": post_modificado}


# ruta delete para un post
@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int):
    post_borrado = db_service.deletePost(post_id)

    if not post_borrado:
        raise HTTPException(detail="Post no encontrado", status_code=404)
    
    if post_borrado == "Error":
        raise HTTPException(detail="Error al eliminar el post", status_code=500)

    return {"post": post_borrado}


# rutas de usuario
@app.post("/users", tags=["Users"])
def create_user(user: User):
    post_crear_usuario = db_service.create_user(user.username, user.password)

    if post_crear_usuario == "Usuario ya existe":
        raise HTTPException(detail="El usuario ya existe", status_code=409)
    
    if not post_crear_usuario:
        raise HTTPException(detail="Error al crear el usuario", status_code=400)

    return {"mensaje": post_crear_usuario}


@app.post("/users/validate", tags=["Users"])
def validate_access(user: User):
    post_validar_acceso = db_service.validate_access(user.username, user.password)

    if not post_validar_acceso:
        raise HTTPException(detail="Acceso denegado", status_code=401)
    
    return {"mensaje": "Acceso concedido"}
