import requests

#prueba de rutas get
def test_get_posts():
    #ruta del api
    url = "http://127.0.0.1:8000/posts"
    
    #peticion get
    response = requests.get(url)
    
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
def test_get_post_byid(id:int):
    #ruta del servidor
    url = f"http://127.0.0.1:8000/post/{id}"
    
    #peticion al servidor
    response = requests.get(url)
    
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
        
def test_get_post_byauthor(author:str):
    #ruta del api
    url = f"http://127.0.0.1:8000/post/?author={author}"
    
    #peticion get
    response = requests.get(url)
    
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
def test_create_post(post_id, author:str, date:str, text:str):
    # Ruta del url
    url = "http://127.0.0.1:8000/posts"
    # Ingreso de los datos a los campos
    new_post = {"id": int(post_id), 
               "author": author, 
               "date": date, 
               "text": text}
    # Petición post
    response = requests.post(url, json=new_post)

    # Verificación de código
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"

    # Verificación de los campos
    data = response.json()
    if "post" in data:
        post = data["post"]
        assert post["id"] == new_post["id"]
        assert post["author"] == new_post["author"]
        assert post["date"] == new_post["date"]
        assert post["text"] == new_post["text"]

    assert "msg" in response.json()
    print(response.json())

# Prueba del método update_post
def test_update_post(post_id, author:str, date:str, text:str):
    # Ruta del url
    url = f"http://127.0.0.1:8000/posts/{post_id}"
    # Ingreso de los datos a los campos
    new_update_post = {"id": int(post_id), 
                       "author": author, 
                       "date": date, 
                       "text": text}
    # Petición put
    response = requests.put(url, json=new_update_post)

    # Verificación de código
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    # Verificación de los campos
    data = response.json()
    if "post" in data:
        post = data["post"]
        assert post["id"] == new_update_post["id"]
        assert post["author"] == new_update_post["author"]
        assert post["date"] == new_update_post["date"]
        assert post["text"] == new_update_post["text"]

    assert "msg" in response.json()
    print(response.json())
   
# Prueba del método delete_post
def test_delete_post(post_id):
    # Ruta del url
    url = f"http://127.0.0.1:8000/posts/{post_id}"

    # Petición delete
    response = requests.delete(url)

    # Verificación de código
    assert response.status_code == 204
    assert response.text == ""

    assert "msg" in response.json()
    print(response.json())


#llamadas de funciones
test_get_posts()
test_get_post_byid(1)
test_get_post_byauthor("Ivan Cadena")

# Nuevos métodos asignados
test_create_post(1, "Juan Pérez", "2025-04-07", "Este es un post de prueba")
test_update_post(1, "Juan Pérez", "2025-05-21", "Este es un cambio en el post")
test_delete_post(1)

#prueba creater_user
def test_create_user(requests_mock):
    url = "http://localhost:5000/users"
    mock_response = {"message": "Usuario creado exitosamente"}
    
    requests_mock.post(url, json=mock_response)
    result = client.create_user("juan", "1234", "http://localhost:5000")
    
    assert result == mock_response
#prueba validate_access
def test_validate_access(requests_mock):
    url = "http://localhost:5000/users/validate"
    mock_response = {"message": "Acceso concedido"}
    
    requests_mock.post(url, json=mock_response)
    result = client.validate_access("juan", "1234", "http://localhost:5000")
    
    assert result == mock_response
