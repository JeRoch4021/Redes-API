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
    
    
#llamadas de funciones
test_get_posts()
test_get_post_byid(1)
test_get_post_byauthor("Ivan Cadena")