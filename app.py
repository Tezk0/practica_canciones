from flask import Flask, render_template, redirect, session, request, flash
from usuario import Usuario
from cancion import Cancion
from favorito import Favorito

app = Flask(__name__)

app.secret_key = "ashifashiogdsjw9u460'41yh9r' fasñkafs"

@app.route("/")
def inicio():
    return redirect("/usuarios")

@app.route("/usuarios")
def usuarios():
    usuarios = Usuario.get_all()

    return render_template("index.html", usuarios=usuarios)

@app.route("/Crear_usuario", methods=['POST'])
def crear():
    nombre = request.form.get('nombre')
    email = request.form.get('email') 
    contrasena = request.form.get('contrasena')

    try:
        user_id = Usuario.save({
            "nombre": nombre,
            "email": email,
            "contrasena": contrasena
        })

        if not user_id:
            flash("No se pudo crear la cuenta.", "error")
            return redirect("/")

    except ValueError as error:
        flash(str(error), "error")
        return redirect("/")

    session['user_id'] = user_id
    session['nombre'] = nombre
    session['contrasena'] = contrasena

    return redirect("/"), flash("Cuenta creada correctamente", "success")

@app.route("/canciones")
def canciones():
    canciones = Cancion.get_all()
    return render_template("canciones.html", canciones=canciones)

@app.route("/Crear_cancion", methods=['POST'])
def crear_cancion():
    titulo = request.form.get('titulo')
    artista = request.form.get('artista')

    try:
        cancion_id = Cancion.save({
            'titulo': titulo,
            'artista': artista
        })

        if not cancion_id: 
            flash("No se pudo crear la cancion", "error")
            return redirect("/canciones")


    except ValueError as error:
        flash(str(error), "error")
        return redirect("/canciones")

    return redirect("/canciones"), flash("Cancion creada!", "success")

@app.route("/usuarios/<int:user_id>")
def usuario(user_id):
    datos = {
        "id": user_id
    }

    usuario = Usuario.get_by_id(datos)

    canciones = Cancion.get_all()

    favoritos= Favorito.get_by_usuario_id(user_id)

    return render_template("usuario.html", usuario=usuario, canciones=canciones,favoritos=favoritos)

@app.route("/Add_favorito", methods=['POST'])
def add():
    datos = {
    "usuario_id": request.form["usuario_id"],
    "cancion_id": request.form["cancion_id"]
    }
    Favorito.agregar_fav(datos)
    return redirect(f"/usuarios/{datos['usuario_id']}")

@app.route("/cancion/<int:cancion_id>")
def mostar_cancion(cancion_id):
    datos = {
        "id": cancion_id
    }

    cancion = Cancion.get_by_id(datos)

    usuarios = Usuario.get_all()

    usuarios_favoritos = Favorito.get_all_users_on_song(cancion_id)

    usuarios_favoritos_ids = [u["id"] for u in usuarios_favoritos]


    return render_template("cancion.html", cancion=cancion, usuarios=usuarios, usuarios_favoritos=usuarios_favoritos, usuarios_favoritos_ids=usuarios_favoritos_ids)

@app.route("/Agregar_usuario_fav", methods=['POST'])
def agregar_usuario_fav():
    datos = {
    "usuario_id": request.form["usuario_id"],
    "cancion_id": request.form["cancion_id"]
    }
    Favorito.agregar_fav(datos)
    return redirect(f"/cancion/{datos['cancion_id']}")


if __name__ == "__main__":
    app.run(debug=True)