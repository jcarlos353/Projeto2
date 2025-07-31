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

@app.route('/api/tvl')
def api_tvl():
    try:
        url = 'https://api.llama.fi/protocols'
        response = requests.get(url)
        data = response.json()

        top_10 = sorted(data, key=lambda x: x.get('tvl', 0), reverse=True)[:10]

        result = [
            {
                'name': item['name'],
                'tvl': item['tvl'],
                'url': item.get('url', '')
            }
            for item in top_10
        ]
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')