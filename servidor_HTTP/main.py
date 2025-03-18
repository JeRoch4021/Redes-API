#zona de imports
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from servidor_HTTP.models.schemas import Post, User
from servidor_HTTP.services.database import DatabaseService
from typing import List

posts = []

#aplicacion
app = FastAPI()

#documentacion de la aplicacion
app.title = "Servidor http con fastapi"
app.version = "0.0.1"

#servicios
db_service = DatabaseService()

#rutas y funciones
#ruta principal
@app.get("/",tags=["Home"])#tags indica agrupacion de rutas
def get_home()->HTMLResponse:
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
    else:
        response += f"<h2>No hay conexion a base de datos!!!!</h2>"
    #puede retornar un json (dict) o str o html
    return HTMLResponse(response)

#ruta get principal
@app.get("/posts",tags=["Posts"])
def get_posts()->List[Post]:
    return db_service.getPosts()

#ruta con parametros
@app.get("/post/{post_id}",tags=["Posts"])
def get_post(post_id:int)->Post:
    #busqueda de post
    post = db_service.getPost(post_id)
    if post:    
        return post
    return {"msg":"post not found"}

#ruta con parametros normal y query (clave-valor)
@app.get("/post/",tags=["Posts"])
def get_postq(author:str)->List[Post]:
    #retorno de lista con los posts
    aposts = db_service.getPostByAuthor(author)
    return aposts

#ruta post para subir un nuevo post
@app.post("/posts",tags=['Posts'])
def create_post(
    #body ayuda a convertir los valores a valores dentro del cuerpo de la peticion
    #id:int = Body(), 
    #author:str = Body(), 
    #date:str = Body(), 
    #post:str = Body()
    post: Post
    ):
    #volcar el modelo a diccionario
    #posts.append(post.model_dump())
    msg = db_service.createPost(post)
    return {"msg":msg}

#ruta put para modificar los datos de un post
@app.put("/posts/{post_id}",tags=['Posts'])
def update_post(
    post_id:int,
    #author:str = Body(), 
    #date:str = Body(), 
    #post:str = Body()
    post:Post
    ):
    msg = db_service.updatePost(post_id, post)
    return {"msg":msg}

#ruta delete para un post
@app.delete("/posts/{post_id}",tags=['Posts'])
def delete_post(post_id:int):
    msg = db_service.deletePost(post_id)
    return {"msg":msg}

#rutas de usuario
@app.post("/users",tags=["Users"])
def create_user(user:User):
    msg = db_service.create_user(user)
    return {"msg":msg}

@app.post("/users/validate",tags=["Users"])
def validate_access(user:User):
    return db_service.validate_access(user)