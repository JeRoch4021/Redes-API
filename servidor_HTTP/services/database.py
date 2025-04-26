from mysql import connector as conn
from models.schemas import Post, User

#objeto de conexion
class DatabaseService:
    SERVER_CONFIG = {
        "user": "root",
        "password": "JeR0204&&T411erBD",
        "port": 3306,
        "bd": "chatdb"
        }
    #******* metodo constructor *******#
    def __init__(self)->None:
        #tratamiento de excepcion
        try:
            self._con = conn.connect(user=DatabaseService.SERVER_CONFIG['user'],
                                 password=DatabaseService.SERVER_CONFIG['password'],
                                 database=DatabaseService.SERVER_CONFIG['bd'],
                                 port=DatabaseService.SERVER_CONFIG['port']
                                )
        except conn.Error as e:
            self._con = None
    #******* metodos de instancia *******#
    def getPosts(self)->list:
        #tratamiento de excepcion
        try:
            #obtenemos el cursor
            cursor = self._con.cursor()
            
            #preparamos la sentencia
            sentencia = """
            SELECT p.id, u.username, p.message_date, p.message
            FROM users as u join messages as p on u.id = p.user_id;
            """
            
            #ejeccion de la sentencia y obtencion de los resultados
            cursor.execute(sentencia)
            data = cursor.fetchall()
            
            #paso de datos a modelos
            posts = []
            for row in data:
                post = Post(id=row[0],author=row[1],date=str(row[2]),text=row[3])
                posts.append(post)
                
            #guardamos los cambios
            self._con.commit()
            
            #retorno de datos
            return posts
        except conn.Error as e:
            return []
        
    def getPost(self, post_id:int)->Post:
        #tratamiento de excepcion
        try:
            #obtenemos el cursor
            cursor = self._con.cursor()
            
            #preparamos la sentencia
            sentencia = f"""
            SELECT p.id, u.username, p.message_date, p.message
            FROM users as u join messages as p on u.id = p.user_id
            WHERE p.id = {post_id};
            """
            
            #ejeccion de la sentencia y obtencion de los resultados
            cursor.execute(sentencia)
            data = cursor.fetchall()
            
            #paso de datos a modelos
            post = Post(id=data[0][0],author=data[0][1],date=str(data[0][2]),text=data[0][3])
                
            #guardamos los cambios
            # self._con.commit()
            
            #retorno de datos
            return post
        except Exception as error:
            raise error
        except conn.Error | IndexError as databaseError:
            raise databaseError
        
    def getPostByAuthor(self, author:str)->list:
        #tratamiento de excepcion
        try:
            #obtenemos el cursor
            cursor = self._con.cursor()
            #preparamos la sentencia
            sentencia = f"""
            SELECT p.id, u.username, p.message_date, p.message
            FROM users as u join messages as p on u.id = p.user_id
            WHERE u.username = '{author}';
            """
            
            #ejeccion de la sentencia y obtencion de los resultados
            cursor.execute(sentencia)
            data = cursor.fetchall()
            
            #paso de datos a modelos
            posts = []
            for row in data:
                post = Post(id=row[0],author=row[1],date=str(row[2]),text=row[3])
                posts.append(post)
                
            #guardamos los cambios
            self._con.commit()
            
            #retorno de datos
            return posts
        except conn.Error as e:
            return []
        
    def createPost(self, post:Post)->dict:
        #tratamiento de errores
        try:
            #puntero a conexion
            cursor = self._con.cursor()
            
            #sentencia de creacion
            sentencia = "insert into messages (user_id, message, message_date) values (%s,%s,%s)"
            parametros = (int(post.author), post.text, post.date)
            
            #ejecucion de la sentencia
            cursor.execute(sentencia,parametros)
            
            #guardamos los cambios
            self._con.commit()
            return "exito al crear!!!"
        except conn.Error as e:
            print(f"Error creando post: {e}")
            return None
        
    def updatePost(self, post_id, post:Post)->str:
        #tratamiento de error
        try:
            #obtener el puntero a conexion
            cursor = self._con.cursor()
            
            #sentencia de actualizacion
            sentencia = "update messages set message = %s, message_date = %s where id = %s"
            parametros = (post.text, post.date, post_id)
            
            #ejecucion de la sentencia
            cursor.execute(sentencia, parametros)
            
            #guardamos los cambios
            self._con.commit()
            return "exito al actualizar!!!"
        except conn.Error as e:
            print(f"Error al actualizar post: {e}")
            return None
        
    def deletePost(self, post_id:int)->str:
        try:
            #obtener el puntero a conexion
            cursor = self._con.cursor()
            
            #sentencia de baja
            sentencia = f"delete from messages where id = {post_id}"
            
            #ejecutamos la sentencia
            cursor.execute(sentencia)
            
            #guardamos los cambios
            self._con.commit()
            return "exito al eliminar!!!"
        except conn.Error as e:
            print(f"Error al eliminarr post: {e}")
            return None
        
    def create_user(self, user:User)->str:
        #tratamiento de errores
        try:
            #puntero a conexion
            cursor = self._con.cursor()
            
            #sentencia de creacion
            sentencia = "insert into users (username, password) values (%s,%s)"
            parametros = (user.username,user.password)
            
            #ejecucion de la sentencia
            cursor.execute(sentencia,parametros)
            
            #guardamos los cambios
            self._con.commit()
            return "exito al crear!!!"
        except conn.Error as e:
            print(f"Error al crear usuario: {e}")
            return None
        
    def validate_access(self, user:User)->dict:
        response = dict()
        #tratamiento de errores
        try:
            #puntero a conexion
            cursor = self._con.cursor()
            
            #sentencia
            sentencia = f"select id, username, password from users where username = '{user.username}';"
            
            #ejecucion de la sentencia
            cursor.execute(sentencia)
            data = cursor.fetchall()
            
            #validacion de usuario
            if len(data) > 0:
                _, _, password = data[0]
                #validacion de contraseña
                if user.password == password:
                    response['status'] = 'exito'
                    response['msg'] = 'datos validados!!!'
                else:
                    response['status'] = 'error'
                    response['msg'] = 'contraseña incorrecta!!!'
            else:
                response['status'] = 'error'
                response['msg'] = 'usuario inexistente!!!'
            #cerramos la transaccion
            self._con.commit()
            return response
        except conn.Error as e:
            response['status'] = 'error'
            response['msg'] = 'error en la validacion!!!'
            return response
        
    #******* metodos de atributo *******#
    def isConnected(self)->bool:
        return True if self._con else False
