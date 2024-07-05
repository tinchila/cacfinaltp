from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mysqldb import MySQL
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sistema'

# Guardar imágenes subidas
UPLOAD_FOLDER = 'path_to_save_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)

# Ruta para servir archivos estáticos
@app.route('/path_to_save_images/<path:filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Ruta Obtener todas las bebidas
@app.route('/api/bebidas', methods=['GET'])
def get_bebidas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM bebidas')
    data = cur.fetchall()
    cur.close()
    
    bebidas = []
    for bebida in data:
        bebidas.append({
            'id': bebida[0],
            'bebida': bebida[1],
            'marca': bebida[2],
            'variedad': bebida[3],
            'precio': bebida[4],
            'imagen': f"{request.url_root}path_to_save_images/{bebida[5]}",
            'cantidad': bebida[6]
        })
    
    return jsonify(bebidas)

# Ruta Crear una nueva bebida
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

# Ruta Actualizar una bebida existente
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

#Ruta Borrar una bebida
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
