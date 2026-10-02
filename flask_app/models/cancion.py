from flask_app.config.mysqlconnection import connectToMySQL
DB_NAME =  'esquema_canciones'

class Cancion:
    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.artista = data['artista']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO canciones (titulo, artista) VALUES (%(titulo)s, %(artista)s);"
        # %(dato)s = sentencia preparada
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def get_all(cls):
        query ="SELECT * FROM canciones;"
        resultados = connectToMySQL(DB_NAME).query_db(query)

        canciones = []

        for cancion in resultados:
            canciones.append(cls(cancion))

        return canciones

    @classmethod
    def get_by_id(cls,datos):
        query = "SELECT * FROM canciones WHERE id = %(id)s;"
        resultados = connectToMySQL(DB_NAME).query_db(query,datos)

        return cls(resultados[0])