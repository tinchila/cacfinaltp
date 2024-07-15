from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mysqldb import MySQL
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuración de la conexión a la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'sistema'

# Inicialización de la extensión MySQL
mysql = MySQL(app)

# Directorio donde se guardarán las imágenes subidas
UPLOAD_FOLDER = 'path_to_save_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta para servir archivos estáticos
@app.route('/path_to_save_images/<path:filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Ruta para obtener todas las bebidas
@app.route('/api/bebidas', methods=['GET'])
def get_bebidas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM bebidas')
    data = cur.fetchall()
    bebidas = []
    for row in data:
        bebidas.append({
            'id': row[0],
            'bebida': row[1],
            'marca': row[2],
            'variedad': row[3],
            'precio': row[4],
            'imagen': f"{request.host_url}{app.config['UPLOAD_FOLDER']}/{row[5]}",
            'cantidad': row[6]
        })
    cur.close()
    return jsonify(bebidas)

# Ruta para crear una nueva bebida
@app.route('/api/bebidas', methods=['POST'])
def add_bebida():
    bebida = request.form['bebida']
    marca = request.form['marca']
    variedad = request.form['variedad']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    imagen = request.files['imagen']
    
    imagen_filename = imagen.filename
    imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO bebidas (bebida, marca, variedad, precio, imagen, cantidad) VALUES (%s, %s, %s, %s, %s, %s)', 
                (bebida, marca, variedad, precio, imagen_filename, cantidad))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Bebida creada'}), 201

# Ruta para actualizar una bebida existente
@app.route('/api/bebidas/<int:id>', methods=['PUT'])
def update_bebida(id):
    bebida = request.form['bebida']
    marca = request.form['marca']
    variedad = request.form['variedad']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    imagen = request.files['imagen']
    
    imagen_filename = imagen.filename
    imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))

    cur = mysql.connection.cursor()
    cur.execute('UPDATE bebidas SET bebida=%s, marca=%s, variedad=%s, precio=%s, imagen=%s, cantidad=%s WHERE id=%s', 
                (bebida, marca, variedad, precio, imagen_filename, cantidad, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Bebida actualizada'}), 200

# Ruta para borrar una bebida
@app.route('/api/bebidas/<int:id>', methods=['DELETE'])
def delete_bebida(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM bebidas WHERE id=%s', (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Bebida eliminada'}), 200

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('/bebidas/index.html')

if __name__ == '__main__':
    app.run(debug=True)
