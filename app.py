from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from scraper import get_flipkart_price, get_amazon_price  # Direct import from the same folder
app = Flask(__name__, static_folder='static')  # Ensures the static folder is served correctly


CORS(app)  # Enable CORS to allow requests from the frontend

# Route to serve the HTML frontend
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare-price', methods=['POST'])
def compare_price():
    data = request.json
    product_name = data.get('product_name')
    if not product_name:
        return jsonify({"error": "Product name is required"}), 400
    
    flipkart_price, flipkart_url = get_flipkart_price(product_name)
    amazon_price, amazon_url = get_amazon_price(product_name)

    return jsonify({
        "flipkart": {"price": flipkart_price, "url": flipkart_url},
        "amazon": {"price": amazon_price, "url": amazon_url}
    })

if __name__ == '__main__':
    app.run(debug=True)
