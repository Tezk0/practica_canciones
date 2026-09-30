from flask import Flask, render_template, redirect, session, request, flash
from usuario import Usuario

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









if __name__ == "__main__":
    app.run(debug=True)