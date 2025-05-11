from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__, template_folder='.')

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

# Servir archivos estáticos desde la raíz
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
