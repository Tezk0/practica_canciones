from mysqlconnection import connectToMySQL
DB_NAME = 'esquema_canciones'

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.email = data['email']
        self.contrasena = data['contrasena']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuarios (nombre, email, contrasena) VALUES (%(nombre)s, %(email)s, %(contrasena)s);"
        # %(dato)s = sentencia preparada
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        resultados = connectToMySQL(DB_NAME).query_db(query)

        usuarios = []

        for usuario in resultados:
            usuarios.append(cls(usuario))

        return usuarios