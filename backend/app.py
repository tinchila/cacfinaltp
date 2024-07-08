import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mysqldb import MySQL
from flask_cors import CORS
import os
from dotenv import load_dotenv
from database import DbSession

load_dotenv()

# Configurar el registro
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
env = os.getenv('FLASK_ENV')

if env == 'production':
    app.config['MYSQL_HOST'] = os.getenv('PROD_MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('PROD_MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('PROD_MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('PROD_MYSQL_DB')
else:
    app.config['MYSQL_HOST'] = os.getenv('LOCAL_MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('LOCAL_MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('LOCAL_MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('LOCAL_MYSQL_DB')

mysql = MySQL(app)

# Guardar imágenes subidas
UPLOAD_FOLDER = 'path_to_save_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta para servir archivos estáticos
@app.route('/path_to_save_images/<path:filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Ruta Obtener todas las bebidas
@app.route('/api/bebidas', methods=['GET'])
def get_bebidas():
    try:
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
    except Exception as e:
        logging.error(f"Error al obtener bebidas: {e}")
        return jsonify({'message': 'Error al obtener bebidas'}), 500

# Ruta Crear una nueva bebida
@app.route('/api/bebidas', methods=['POST'])
def add_bebida():
    try:
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
    except Exception as e:
        logging.error(f"Error al crear bebida: {e}")
        return jsonify({'message': 'Error al crear bebida'}), 500


# Ruta Actualizar una bebida existente
@app.route('/api/bebidas/<int:id>', methods=['PUT'])
def update_bebida(id):
    try:
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
    except Exception as e:
        logging.error(f"Error al actualizar bebida: {e}")
        return jsonify({'message': 'Error al actualizar bebida'}), 500

# Ruta Borrar una bebida
@app.route('/api/bebidas/<int:id>', methods=['DELETE'])
def delete_bebida(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM bebidas WHERE id=%s', (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Bebida eliminada'}), 200
    except Exception as e:
        logging.error(f"Error al eliminar bebida: {e}")
        return jsonify({'message': 'Error al eliminar bebida'}), 500

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('/bebidas/index.html')

if __name__ == '__main__':
    app.run(debug=True)
