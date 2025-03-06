#zona de imports
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from models.schemas import Post
from typing import List

#posts
posts = [{
            "id":1,
            "author":"Ivan Cadena",
            "date":"02-03-2025",
            "text":"Como estan todos?"
         },{
            "id":2,
            "author":"Ivan Cadena",
            "date":"02-03-2025",
            "text":"Porque nadie responde"
         },{
            "id":3,
            "author":"Ivan Cadena",
            "date":"02-03-2025",
            "text":"Acaso estoy solo?"
         }]

#aplicacion
app = FastAPI()

#documentacion de la aplicacion
app.title = "Servidor http con fastapi"
app.version = "0.0.1"

#rutas y funciones
#ruta principal
@app.get("/",tags=["Home"])#tags indica agrupacion de rutas
def get_home()->HTMLResponse:
    #puede retornar un json (dict) o str o html
    return HTMLResponse("""
                        <h1>Primer proyecto con fastapi</h1>
                        <p>
                            Proyecto para la materia de topicos para
                            el despliegue de paplicaciones de la carrera
                            de ingenieria en sistemas.
                        </p>
                        """)

#ruta get principal
@app.get("/posts",tags=["Posts"])
def get_posts()->List[Post]:
    return posts

#ruta con parametros
@app.get("/post/{post_id}",tags=["Posts"])
def get_post(post_id:int)->Post:
    #busqueda de post
    for post in posts:
        if post.get("id") == post_id:
            return post
    return {"msg":"post not found"}

#ruta con parametros normal y query (clave-valor)
@app.get("/post/",tags=["Posts"])
def get_postq(author:str)->List[Post]:
    aposts = []
    #busqueda de post por autor
    for post in posts:
        if post.get("author") == author:
            aposts.append(post)
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
    posts.append(post.model_dump())
    return {"msg":"recived!!"}

#ruta put para modificar los datos de un post
@app.put("/posts/{post_id}",tags=['Posts'])
def update_post(
    post_id:int,
    #author:str = Body(), 
    #date:str = Body(), 
    #post:str = Body()
    post:Post
    ):
    #contenedor de post
    u_post = dict()
    #filtrado de posts
    for o_post in posts:
        if o_post.get("id") == post_id:
            u_post = o_post
            break
    #modificacion de los datos
    u_post['author'] = post.author
    u_post['date'] = post.date
    u_post['text'] = post.text
    
    return {"msg":"updated!!"}

#ruta delete para un post
@app.delete("/posts/{post_id}",tags=['Posts'])
def delete_post(post_id:int):
    #busqueda del post
    for post in posts:
        if post.get("id") == post_id:
            posts.remove(post)
    return {"msg":"deleted!!!"}