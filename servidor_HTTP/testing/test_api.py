from fastapi.testclient import TestClient
from servidor_HTTP.main import app

cliente = TestClient(app)

#prueba de rutas get
def test_get_posts():
    #ruta del api
    #url = "http://127.0.0.1:8000/posts"
    
    #peticion get
    response = cliente.get("/posts")
    
    try:
        #verificamos el codigo
        assert response.status_code == 200

        #verificamos el tipo de contenido
        assert response.headers["content-type"] == "application/json"

        #verificar los datos por campo
        data = response.json()
        assert isinstance(data,list) #que sea un diccionario

        for post in data:
            assert isinstance(post,dict)
            assert "id" in post
            assert "author" in post
            assert "date" in post
            assert "text" in post
        print("Prueba exitosa!!!!!")
    except AssertionError as e:
        print("Prueba fracasada!!!!")

#prueba de get post por id
def test_get_post_byid():
    #ruta del servidor
    id = 1
    #url = f"http://127.0.0.1:8000/post/{id}"
    
    #peticion al servidor
    response = cliente.get(f"/post/{id}")
    
    try:
        #validacion de codigo
        assert response.status_code == 200
        
        #validacion del tipo de contenido
        assert response.headers["content-type"] == "application/json"
        
        #obtencion y validacion de datos
        data = response.json()
        assert isinstance(data,dict)
        
        #validacion de campos
        assert "id" in data
        assert "author" in data
        assert "date" in data
        assert "text" in data
        print("Prueba exitosa!!!!")
    except AssertionError as e:
        print("Prueba fracasada!!!!!")
        
def test_get_post_byauthor():
    author = "Ivan Cadena"
    #ruta del api
    #url = f"http://127.0.0.1:8000/post/?author={author}"
    
    #peticion get
    response = cliente.get(f"/post/?author={author}")
    
    try:
        #verificamos el codigo
        assert response.status_code == 200

        #verificamos el tipo de contenido
        assert response.headers["content-type"] == "application/json"

        #verificar los datos por campo
        data = response.json()
        assert isinstance(data,list) #que sea un diccionario

        for post in data:
            assert isinstance(post,dict)
            assert "id" in post
            assert "author" in post
            assert "date" in post
            assert "text" in post
        print("Prueba exitosa!!!!!")
    except AssertionError as e:
        print("Prueba fracasada!!!!")

# Nuevos método integrados al códigos

# Prueba del método create_post
def test_create_post():
    post_id = 1 
    author:str = "Juan Pérez"
    date:str = "2025-04-07"
    text:str = "Este es un post de prueba"
    # Ruta del url
    #url = "http://127.0.0.1:8000/posts"
    # Ingreso de los datos a los campos
    new_post = {"id": int(post_id), 
               "author": author, 
               "date": date, 
               "text": text}
    # Petición post
    response = cliente.post("/posts", json=new_post)

    # Verificación de código
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"

    # Verificación de los campos
    data = response.json()
    if "post" in data:
        post = data["post"]
        assert post == new_post
    assert "msg" in data
    print(data)

# Prueba del método update_post
def test_update_post():
    post_id = 1
    author:str = "Juan Pérez"
    date:str = "2025-05-21"
    text:str = "Este es un cambio en el post"
    # Ruta del url
    #url = f"http://127.0.0.1:8000/posts/{post_id}"
    # Ingreso de los datos a los campos
    new_update_post = {"id": int(post_id), 
                       "author": author, 
                       "date": date, 
                       "text": text}
    # Petición put
    response = cliente.put(f"/posts/{post_id}", json=new_update_post)

    # Verificación de código
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    # Verificación de los campos
    data = response.json()
    if "post" in data:
        post = data["post"]
        assert post == new_update_post
    assert "msg" in data
    print(data)
   
# Prueba del método delete_post
def test_delete_post():
    post_id = 1
    # Ruta del url
    #url = f"http://127.0.0.1:8000/posts/{post_id}"

    # Petición delete
    response = cliente.delete(f"/posts/{post_id}")

    # Verificación de código
    assert response.status_code == 204
    assert response.text == ""

#Funciones complementarias para creater_user y validate_access
def create_user(username, password):
    #url = "http://127.0.0.1:8000/users"
    user_data = {"username": username, "password": password}
    response = cliente.post("/users", json=user_data)
    return response.json()

def validate_access(username, password):
    #url = "http://127.0.0.1:8000/users/validate"
    user_data = {"username": username, "password": password}
    response = cliente.post("/users/validate", json=user_data)
    return response.json()

#prueba creater_user
def test_create_user():
    result = create_user("juan", "1234")
    
    try:
        assert "message" in result
        assert result["message"] == "Usuario creado exitosamente"
        print("Preuba de creación exitosa", result)
    except AssertionError:
        print("Fallo de la prueba de creación", result)

#prueba validate_access
def test_validate_access():
    result = validate_access("juan", "1234")

    try:
        assert "message" in result
        assert result["message"] == "Acceso concedido"
        print("Prueba de validación exitosa", result)
    except AssertionError:
        print("Fallo de la prueba de validación", result)

