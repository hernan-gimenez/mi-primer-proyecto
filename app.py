from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

# Configuración
app.config['TEMPLATES_AUTO_RELOAD'] = True

# File to store links
LINKS_FILE = 'links.txt'

def load_links():
    if not os.path.exists(LINKS_FILE):
        return []
    with open(LINKS_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_link(link):
    with open(LINKS_FILE, 'a', encoding='utf-8') as f:
        f.write(link + '\n')

@app.route('/')
def home():
    links = load_links()
    return render_template('index.html', links=links)

@app.route('/save', methods=['POST'])
def save():
    link = request.form.get('link', '').strip()
    if link:
        save_link(link)
    return redirect(url_for('home'))

# Ruta para archivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Ruta para manejar rutas de la aplicación SPA
@app.route('/<path:path>')
def serve_any(path):
    return app.send_static_file('index.html')

# Manejo de errores 404
@app.errorhandler(404)
def not_found(e):
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Asegurarse de que el directorio de plantillas exista
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Crear archivo de enlaces si no existe
    if not os.path.exists(LINKS_FILE):
        open(LINKS_FILE, 'a').close()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
