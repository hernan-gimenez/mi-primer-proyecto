from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# File to store links
LINKS_FILE = 'links.txt'

def load_links():
    if not os.path.exists(LINKS_FILE):
        return []
    with open(LINKS_FILE, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_link(link):
    with open(LINKS_FILE, 'a') as f:
        f.write(link + '\n')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        link = request.form.get('link', '').strip()
        if link:
            save_link(link)
        return redirect(url_for('index'))
    
    links = load_links()
    return render_template('index.html', links=links)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
