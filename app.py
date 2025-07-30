from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

def get_crypto_prices():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,cardano&vs_currencies=usd'
    response = requests.get(url)
    return response.json()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/precos')
def api_precos():
    return jsonify(get_crypto_prices())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')