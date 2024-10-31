from flask import Flask, render_template, request, jsonify
import serial
app = Flask(__name__)
arduino = serial.Serial('COM3', 9600) 

# Sample product data
products = {
    '8901491503020': {'Product ID': '8901491503020', 'Product Name': 'lays Wafers', 'Product Description': 'Rs', 'Price': 20},
    'X8901765119971': {'Product ID': '8901765119971', 'Product Name': 'Hauser refill - blue', 'Product Description': 'Rs', 'Price': 10},
    '8908000034211': {'Product ID': '8908000034211', 'Product Name': 'Cold coffee', 'Product Description': 'Rs', 'Price': 300},
    
}

# Sample cart data
cart = []

@app.route('/')
def index():
    return render_template('index.html', products=products, cart=cart)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    scanned_code = request.form['scanned_code']
    if scanned_code in products:
        cart.append(products[scanned_code])
        arduino.write(b'C')  # Send 'C' to Arduino
        return jsonify({'cart': cart})
    else:
        return jsonify({'error': 'Product not found'}), 404
    
@app.route('/delete_from_cart', methods=['POST'])
def delete_from_cart():
    item_id = request.form['item_id']
    for item in cart:
        if item['Product ID'] == item_id:
            cart.remove(item)
            arduino.write(b'0')  # Send '0' to Arduino
    return jsonify({'cart': cart})
    return jsonify({'error': 'Item not found in cart'}), 404

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    # Implement payment processing logic here
    return 'Payment processing...'

if __name__ == '__main__':
    app.run(debug=True)