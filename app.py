from flask import Flask, render_template, request, jsonify
import requests
import sqlite3

app = Flask(__name__)

# Banco de dados
def init_db():
    with sqlite3.connect('dados.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS acessos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                user_agent TEXT
            )
        ''')

@app.before_request
def registrar_acesso():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    with sqlite3.connect('dados.db') as conn:
        conn.execute("INSERT INTO acessos (ip, user_agent) VALUES (?, ?)", (ip, user_agent))

# Autenticação simples
API_KEY = "12345"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/precos')
def api_precos():
    key = request.args.get('key')
    if key != API_KEY:
        return jsonify({'error': 'Acesso não autorizado'}), 401

    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin,ethereum,cardano,solana,dogecoin',
        'vs_currencies': 'usd'
    }
    r = requests.get(url, params=params)
    return jsonify(r.json())

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="0.0.0.0")