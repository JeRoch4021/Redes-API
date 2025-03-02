#zona de imports
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

#posts
posts = [{
            "id":1,
            "author":"Ivan Cadena",
            "date":"02-03-2025",
            "post":"Como estan todos?"
         },{
            "id":2,
            "author":"Ivan Cadena",
            "date":"02-03-2025",
            "post":"Porque nadie responde"
         },{
            "id":3,
            "author":"Ivan Cadena",
            "date":"02-03-2025",
            "post":"Acaso estoy solo?"
         }]

#aplicacion
app = FastAPI()

#documentacion de la aplicacion
app.title = "Servidor http con fastapi"
app.version = "0.0.1"

#rutas y funciones
#ruta principal
@app.get("/",tags=["Home"])#tags indica agrupacion de rutas
def get_home():
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
def get_posts():
    return posts

#ruta con parametros
@app.get("/post/{post_id}",tags=["Posts"])
def get_post(post_id:int):
    #busqueda de post
    for post in posts:
        if post.get("id") == post_id:
            return post
    return {"msg":"post not found"}

#ruta con parametros normal y query (clave-valor)
@app.get("/post/",tags=["Posts"])
def get_postq(author:str):
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
    id:int = Body(), 
    author:str = Body(), 
    date:str = Body(), 
    post:str = Body()
    ):
    posts.append({
        'id': id,
        'author': author,
        'date': date,
        'post': post
    })
    return {"msg":"recived!!"}