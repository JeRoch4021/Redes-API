import requests

#URL del servidor FastAPI
Servidor_URL = "http://192.168.109.1:8080"

def get_posts():
    #Sirve para obtener todos los posts
    response = requests.get(f"{Servidor_URL}/posts")
    print("\n Todos los Posts: ", response.json())

def get_post_con_id():
    #Solicitar un ID y obtiene un post específico
    post_id = input("Escribe el ID del post: ")
    response = requests.get(f"{Servidor_URL}/post/{post_id}")
    print(f"\nPost con ID {post_id}: ", response.json())

def get_posts_con_author():
    #Solicitar a un autor y obtener sus posts
    autor = input("Escribe el nombre del autor: ")
    response = requests.get(f"{Servidor_URL}/post/?author={autor}")
    print(f"\nPosts de {autor}: ", response.json())

def crear_post():
    #Crear un nuevo post solicitando datos al usuario
    post_id = input("Escribe el ID del post: ")
    autor = input("Escribe el autor del post: ")
    date = input("Nueva fecha (dd-mm-aaaa): ")
    text = input("Nuevo contenido: ")

    post_data = {"id": int(post_id), "author": autor, "date": date, "text": text}
    response = requests.post(f"{Servidor_URL}/posts", json=post_data)
    print("\nPost Creado: ", response.json())
    
def update_post():
    #Actualizar un post solicitando datos al usuario
    post_id = input("Escribe el ID del post a actualizar: ")
    autor = input("Nuevo autor: ")
    date = input("Nueva fecha (aaaa-mm-dd): ")
    text = input("Nuevo contenido: ")

    post_data = {"id": int(post_id), "author": autor, "date": date, "text": text}
    response = requests.put(f"{Servidor_URL}/posts/{post_id}", json=post_data)
    print("\nPost Actualizado: ", response.json())

def delete_post():
    #Eliminar un post solicitando su ID
    post_id = input("Escribe el ID del post a eliminar: ")
    response = requests.delete(f"{Servidor_URL}/posts/{post_id}")
    print("\nPost eliminado: ", response.json())

#Manejo de usuarios

def create_user():
    username = input("Ingrese el nombre de usuario: ")
    password = input("Ingrese la contraseña: ")
    user_data = {"username": username, "password": password}
    response = requests.post(f"{Servidor_URL}/users", json=user_data)
    print("\nRespuesta del servidor: ", response.json())

def validate_access():
    username = input("Ingrese el nombre de usuario: ")
    password = input("Ingrese la contraseña: ")
    user_data = {"username": username, "password": password}
    response = requests.post(f"{Servidor_URL}/users/validate", json=user_data)
    print("\nRespuesta del servidor: ", response.json())

def main():
    #Menu interactivo para el usuario pueda elegir la acción a realizar
    print("Cliente HTTP para el Servidor HTTP")
    print("Escribe alguna de las siguientes acciones:")
    print("- 'get'  -> Ver todos los posts")
    print("- 'post' -> Buscar un post por ID")
    print("- 'author'   -> Buscar un post por autor")
    print("- 'create'   -> Crear un nuevo post")
    print("- 'update'   -> Modificar un post")
    print("- 'delete'   -> Borrar un post")
    print("- 'user' -> Crear un nuevo usuario")
    print("- 'login'    -> Validar acceso de usuario")
    print("- 'exit'     -> Terminar el programa")

    while True:
        #Declaramos la acción que queremos realizar 
        accion = input(f"\n{Servidor_URL}/").strip().lower()

        if accion == "get":
            get_posts()
        elif accion == "post":
            get_post_con_id()
        elif accion == "author":
            get_posts_con_author()
        elif accion == "create":
            crear_post()
        elif accion == "update":
            update_post()
        elif accion == "delete":
            delete_post()
        elif accion == 'user':
            crear_post()
        elif accion == 'login':
            validate_access()
        elif accion == "exit":
            print("Saliendo del programa")
            break
        else:
            print("Comando no reconocido, intentelo de nuevo.")

if __name__ == "__main__":
    main()