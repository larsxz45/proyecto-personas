from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__, template_folder='templates')

# Configuración de la base de datos
DB_HOST = 'dpg-d7b8b72dbo4c73csju8g-a.oregon-postgres.render.com'
DB_NAME = 'personas_db_ymek'
DB_USER = 'personas_db_ymek_user'
DB_PASSWORD = 'jATPfz43jqHvke0XbsWHNqin4N24Lbpy'


def conectar_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            sslmode='require'
        )
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)


# Crear persona
def crear_persona(dni, nombre, apellido, direccion, telefono):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO personas (dni, nombre, apellido, direccion, telefono)
        VALUES (%s, %s, %s, %s, %s)
    """, (dni, nombre, apellido, direccion, telefono))
    conn.commit()
    conn.close()


# Obtener registros
def obtener_registros():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas ORDER BY apellido")
    registros = cursor.fetchall()
    conn.close()
    return registros


# Página principal
@app.route('/')
def index():
    return render_template('index.html')


# Registrar persona
@app.route('/registrar', methods=['POST'])
def registrar():
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    telefono = request.form['telefono']

    crear_persona(dni, nombre, apellido, direccion, telefono)

    return redirect(url_for('index'))


# Mostrar registros
@app.route('/administrar')
def administrar():
    registros = obtener_registros()
    return render_template('administrar.html', registros=registros)


# Eliminar registro (CORREGIDO)
@app.route('/eliminar/<int:id>')
def eliminar_registro(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personas WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('administrar'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)