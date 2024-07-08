import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
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

# Configuración para producción y desarrollo
if env == 'production':
    # Configuración de la base de datos PostgreSQL en Render
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('PROD_DATABASE_URL')
else:
    # Configuración de la base de datos local MySQL (si es necesario)
    app.config['MYSQL_HOST'] = os.getenv('LOCAL_MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('LOCAL_MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('LOCAL_MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('LOCAL_MYSQL_DB')

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
        with DbSession(app.config['SQLALCHEMY_DATABASE_URI']) as db:
            db.execute('SELECT * FROM bebidas')
            data = db.fetchall()
            bebidas = []
            for row in data:
                bebidas.append({
                    'id': row['id'],
                    'bebida': row['bebida'],
                    'marca': row['marca'],
                    'variedad': row['variedad'],
                    'precio': row['precio'],
                    'imagen': f"{request.host_url}{app.config['UPLOAD_FOLDER']}/{row['imagen']}",
                    'cantidad': row['cantidad']
                })
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

        with DbSession(app.config['SQLALCHEMY_DATABASE_URI']) as db:
            db.execute('INSERT INTO bebidas (bebida, marca, variedad, precio, imagen, cantidad) VALUES (%s, %s, %s, %s, %s, %s)', 
                        (bebida, marca, variedad, precio, imagen_filename, cantidad))
            db.commit()

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

        with DbSession(app.config['SQLALCHEMY_DATABASE_URI']) as db:
            db.execute('UPDATE bebidas SET bebida=%s, marca=%s, variedad=%s, precio=%s, imagen=%s, cantidad=%s WHERE id=%s', 
                        (bebida, marca, variedad, precio, imagen_filename, cantidad, id))
            db.commit()

        return jsonify({'message': 'Bebida actualizada'}), 200
    except Exception as e:
        logging.error(f"Error al actualizar bebida: {e}")
        return jsonify({'message': 'Error al actualizar bebida'}), 500

# Ruta Borrar una bebida
@app.route('/api/bebidas/<int:id>', methods=['DELETE'])
def delete_bebida(id):
    try:
        with DbSession(app.config['SQLALCHEMY_DATABASE_URI']) as db:
            db.execute('DELETE FROM bebidas WHERE id=%s', (id,))
            db.commit()

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
