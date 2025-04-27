from unittest.mock import patch, ANY
from fastapi.testclient import TestClient
from servidor_HTTP.main import app
from servidor_HTTP.models.schemas import Post
from servidor_HTTP.services.database import DatabaseService

cliente = TestClient(app)

# prueba de rutas get
def test_obtener_posts():
    mockPosts:list = [{"id": 1, "author": "jeshua", "date": "2025-04-25", "text": "Hola, que hay de nuevo"}]
    with patch('services.database.DatabaseService.getPosts') as mockGetPosts:
        mockGetPosts.return_value = mockPosts
        
        #peticion get
        response = cliente.get("/posts")
        
        #verificamos el codigo
        assert response.status_code == 200

        #verificamos el tipo de contenido
        assert response.headers["content-type"] == "application/json"

        #verificar los datos por campo
        data = response.json()
        assert isinstance(data,list) #que sea un diccionario

        for post in data:
            assert "id" in post
            assert "author" in post
            assert "date" in post
            assert "text" in post
        
        mockGetPosts.assert_called_once()

def test_obtener_post_por_id():
    mockPost = Post(author='jeshua', date='2025-04-25', id=1, text='texto de prueba')
    with patch('services.database.DatabaseService.getPost') as mockGetPost:

        mockGetPost.return_value = mockPost

        id = 1
        
        #peticion al servidor
        response = cliente.get(f"/post/{mockPost.id}")
        
        #validacion de codigo
        assert response.status_code == 200
        
        #validacion del tipo de contenido
        assert response.headers["content-type"] == "application/json"
        
        #obtencion y validacion de datos
        data = response.json()
        assert isinstance(data,dict)
        
        #validacion de campos
        assert "id" in data
        assert data["id"] == mockPost.id
        assert "author" in data
        assert "date" in data
        assert "text" in data

        mockGetPost.assert_called()
        mockGetPost.assert_called_once()
        mockGetPost.assert_called_with(mockPost.id)

def test_no_puede_obtener_post_por_id():
    mockPost = None
    with patch('services.database.DatabaseService.getPost') as mockGetPost:

        mockGetPost.return_value = mockPost

        id = 1
        
        #peticion al servidor
        response = cliente.get(f"/post/{id}")
        
        #validacion de codigo
        assert response.status_code == 404
        
        #validacion del tipo de contenido
        assert response.headers["content-type"] == "application/json"
        
        #obtencion y validacion de datos
        data = response.json()
        assert isinstance(data,dict)
        
        #validacion de campos
        assert "id" not in data
        assert "author" not in data
        assert "date" not in data
        assert "text" not in data
        assert "detail" in data
        assert data.get('detail') == "Post no encontrado"

        mockGetPost.assert_called()
        mockGetPost.assert_called_once()
        mockGetPost.assert_called_with(id)
        
        
def test_obtener_post_por_author():
    mockPostAuthor = [{"id": 1, "author": "Ivan Cadena", "date": "2025-04-25", "text": "texto de prueba"}]
    with patch('services.database.DatabaseService.getPostByAuthor') as mockGetPostAuthor:
        mockGetPostAuthor.return_value = mockPostAuthor
        
        #peticion get
        response = cliente.get(f"/post/?author={mockPostAuthor[0]["author"]}")
        
        #verificamos el codigo
        assert response.status_code == 200

        #verificamos el tipo de contenido
        assert response.headers["content-type"] == "application/json"

            #verificar los datos por campo
        data = response.json()
        assert isinstance(data,list) #que sea un diccionario

        for post in data:
            assert "id" in post
            assert "author" in post
            assert post["author"] == mockPostAuthor[0]["author"]
            assert "date" in post
            assert "text" in post

        mockGetPostAuthor.assert_called_once_with(mockPostAuthor[0]["author"])

# Nuevos método integrados al códigos

# # Prueba del método create_post
def test_crear_post():
    new_post = {"id": 1, "author": "Juan Pérez", "date": "2025-04-07", "text": "Este es un post de prueba"}
    with patch('services.database.DatabaseService.createPost') as mockCreatePost:
        mockCreatePost.return_value = new_post

        # Petición post
        response = cliente.post("/posts", json=new_post)

        # Verificación de código
        assert response.status_code == 201
        assert response.headers["Content-Type"] == "application/json"

        # Verificación de los campos
        data = response.json()
        assert "post" in data
        assert data["post"] == new_post

        mockCreatePost.assert_called_once_with(ANY)     

# # Prueba del método update_post
def test_modificar_post():
    update_post = {"id": 1, "author": "Juan Pérez", "date": "2025-04-07", "text": "Este es un post modificado"}
    with patch ('services.database.DatabaseService.updatePost') as mockUpdatePost:
        mockUpdatePost.return_value = update_post

        # Petición put
        response = cliente.put(f"/posts/{update_post["id"]}", json=update_post)

        # Verificación de código
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

        # Verificación de los campos
        data = response.json()
        assert "post" in data
        assert data["post"] == update_post


        args, kwargs = mockUpdatePost.call_args
        assert args[0] == update_post["id"]

        assert args[1].id == update_post["id"]
        assert args[1].author == update_post["author"]
        assert args[1].date == update_post["date"]
        assert args[1].text == update_post["text"]        
   
# Prueba del método delete_post
def test_borrar_post():
    post_id = 1
    with patch ('services.database.DatabaseService.deletePost') as mockDeletePost:
        mockDeletePost.return_value = post_id

        # Petición delete
        response = cliente.delete(f"/posts/{post_id}")

        # Verificación de código
        assert response.status_code == 204
        assert response.text == ''

        mockDeletePost.assert_called_once_with(post_id)

def test_borrar_post_no_encontrado():
    post_id = 5
    with patch ('services.database.DatabaseService.deletePost') as mockDeletePost:
        mockDeletePost.return_value = None

        # Petición delete
        response = cliente.delete(f"/posts/{post_id}")

        # Verificación de código
        assert response.status_code == 404
        assert response.json() == {"detail": "Post no encontrado"}

        mockDeletePost.assert_called_once_with(post_id)

def test_error_borrar_post():
    post_id = 1
    with patch ('services.database.DatabaseService.deletePost') as mockDeletePost:
        mockDeletePost.return_value = "Error"

        # Petición delete
        response = cliente.delete(f"/posts/{post_id}")

        # Verificación de código
        assert response.status_code == 500
        assert response.json() == {"detail": "Error al eliminar el post"}

        mockDeletePost.assert_called_once_with(post_id) 

#prueba creater_user
def test_crear_usuario():
    user_data = {"id": 1, "username": "juan", "password": "1234"}
    respuesta_esperada = {"mensaje": "Usuario creado exitosamente"}
    with patch ('services.database.DatabaseService.create_user') as mockCreateUser:
        mockCreateUser.return_value = respuesta_esperada["mensaje"]
    
        response = cliente.post("/users", json=user_data)
        data = response.json()

        assert response.status_code == 200
        assert data == respuesta_esperada

        mockCreateUser.assert_called_once_with(user_data["username"], user_data["password"])

def test_crear_usuario_ya_existente():
    user_data = {"id": 1, "username": "juan", "password": "1234"}
    with patch ('services.database.DatabaseService.create_user') as mockCreateUser:
        mockCreateUser.return_value = "Usuario ya existe"
    
        response = cliente.post("/users", json=user_data)

        assert response.status_code == 409
        assert response.json() == {"detail": "El usuario ya existe"}

        mockCreateUser.assert_called_once_with(user_data["username"], user_data["password"])

def test_error_crear_usuario():
    user_data = {"id": 1, "username": "juan", "password": "1234"}
    with patch ('services.database.DatabaseService.create_user') as mockCreateUser:
        mockCreateUser.return_value = None
    
        response = cliente.post("/users", json=user_data)

        assert response.status_code == 400
        assert response.json() == {"detail": "Error al crear el usuario"}

        mockCreateUser.assert_called_once_with(user_data["username"], user_data["password"])

#prueba validate_access
def test_validate_access():
    user_data = {"username": "juan", "password": "1234"}
    respuesta_esperada = {"mensaje": "Acceso concedido"}
    with patch ('services.database.DatabaseService.validate_access') as mockValidateUser:
        mockValidateUser.return_value = respuesta_esperada

        response = cliente.post("/users/validate", json=user_data)
        data = response.json()

        assert response.status_code == 200
        assert "mensaje" in data
        assert data == respuesta_esperada

        mockValidateUser.assert_called_once_with(user_data["username"], user_data["password"])

def test_validate_fail():
    user_data = {"username": "juan", "password": "1234"}
    with patch ('services.database.DatabaseService.validate_access') as mockValidateUser:
        mockValidateUser.return_value = False

        response = cliente.post("/users/validate", json=user_data)

        assert response.status_code == 401
        assert response.json() == {"detail": "Acceso denegado"}


