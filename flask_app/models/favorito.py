from flask_app.config.mysqlconnection import connectToMySQL

DB_NAME = "esquema_canciones"

class Favorito:
    @classmethod
    def get_by_usuario_id(cls, usuario_id):
        query = """
            SELECT c.id, c.titulo, c.artista
            FROM usuarios AS u
            LEFT JOIN favoritos AS f ON f.usuario_id = u.id
            LEFT JOIN canciones AS c ON c.id = f.cancion_id
            WHERE u.id = %(usuario_id)s;
        """
        resultados = connectToMySQL(DB_NAME).query_db(query, {"usuario_id": usuario_id})

        return [fila for fila in resultados if fila["id"] is not None]
    
    @classmethod
    def get_all_users_on_song(cls, cancion_id):
        query = """
            SELECT DISTINCT u.id, u.nombre
            FROM favoritos AS f
            INNER JOIN usuarios AS u ON u.id = f.usuario_id
            WHERE f.cancion_id = %(cancion_id)s;
        """
        return connectToMySQL(DB_NAME).query_db(query, {"cancion_id": cancion_id})

    @classmethod
    def agregar_fav(cls, data):
        check_if_duplicate = """
            SELECT usuario_id
            FROM favoritos
            WHERE usuario_id = %(usuario_id)s
            AND cancion_id = %(cancion_id)s;
        """

        duplicate = connectToMySQL(DB_NAME).query_db(check_if_duplicate, data)

        if duplicate:
            return "Usuario duplicado"

        query = """
            INSERT INTO favoritos (usuario_id, cancion_id)
            VALUES (%(usuario_id)s, %(cancion_id)s);
        """
        resultado = connectToMySQL(DB_NAME).query_db(query, data)

        return resultado is not False