from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

hora = datetime.now().strftime("%H:%M")

@app.route("/")
def inicio():
    return render_template("bienvenida.html")

@app.route("/opciones")
def opciones():
    return render_template("opciones.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/pedido")
def pedido():
    return render_template("pedido.html")

@app.route("/confirmacion", methods=["POST"])
def confirmacion():

    nombre = request.form["nombre"]
    platillo = request.form["platillo"]
    cantidad = request.form["cantidad"]
    hora = datetime.now().strftime("%H:%M")

    # tiempos base de preparación
    tiempos = {
        "Tacos": 3,
        "Hamburguesa": 8,
        "Hotdog": 5,
        "Refresco": 1
    }

    tiempo_base = tiempos.get(platillo, 3)

    tiempo_estimado = tiempo_base * int(cantidad)

    conexion = sqlite3.connect("pedidos.db")
    cursor = conexion.cursor()

    cursor.execute(
    "INSERT INTO pedidos (nombre, platillo, cantidad, estado, tiempo_estimado) VALUES (?, ?, ?, ?, ?)",
    (nombre, platillo, cantidad, "Pendiente", tiempo_estimado)
)

    conexion.commit()

    numero_pedido = cursor.lastrowid

    conexion.close()

    return render_template(
    "confirmacion.html",
    nombre=nombre,
    platillo=platillo,
    cantidad=cantidad,
    numero_pedido=numero_pedido,
    tiempo_estimado=tiempo_estimado,
    hora=hora
)
 
@app.route("/cocina")
def cocina():

    conexion = sqlite3.connect("pedidos.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM pedidos WHERE estado != 'Entregado' ORDER BY id DESC")

    pedidos = cursor.fetchall()

    conexion.close()

    return render_template("cocina.html", pedidos=pedidos)

@app.route("/cambiar_estado/<int:id>", methods=["POST"])
def cambiar_estado(id):

    nuevo_estado = request.form["estado"]

    conexion = sqlite3.connect("pedidos.db")
    cursor = conexion.cursor()

    cursor.execute(
        "UPDATE pedidos SET estado=? WHERE id=?",
        (nuevo_estado, id)
    )

    conexion.commit()
    conexion.close()

    return redirect(url_for("cocina"))

@app.route("/consultar")
def consultar():
    return render_template("consultar.html")

@app.route("/buscar_pedido", methods=["POST"])
def buscar_pedido():

    numero = request.form["numero_pedido"]

    conexion = sqlite3.connect("pedidos.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM pedidos WHERE id=?", (numero,))
    pedido = cursor.fetchone()

    conexion.close()

    if pedido:
        return render_template("resultado.html", pedido=pedido)
    else:
        return render_template("resultado.html", pedido=None)

@app.route("/estado/<int:pedido_id>")
def estado(pedido_id):
    conn = sqlite3.connect("pedidos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT estado FROM pedidos WHERE id=?", (pedido_id,))
    estado = cursor.fetchone()

    conn.close()

    return {"estado": estado[0]}

if __name__ == "__main__":
    app.run(debug=True)