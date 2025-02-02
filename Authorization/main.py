# -------------------------------- Imports ---------------------------------------------

from db import DB_Manager
from JWT_Manager import JWT_Manager
from flask import Flask, request, jsonify
import controller as c


# -------------------------------- Class instances ---------------------------------------------

app = Flask("user-service")
db_manager = DB_Manager()


# -------------------------------- Liveness endpoint ---------------------------------------------

@app.route("/liveness")
def liveness():
    return "<p>Hello, World!</p>"


# ------------------ User related endpoints ------------------------

@app.route('/register', methods=['POST'])
def register():
    return c.register_user()        

@app.route('/login', methods=['POST'])
def login():
    return c.login_user()

@app.route('/me')
def me():
    return c.get_user_info()


# ------------------ Product related endpoints ------------------------

@app.route('/products',  methods=['GET', 'POST'])
def products_get_post():
        if request.method == 'POST':
            if c.get_role() == 'admin':
                return c.create_product()
            else:
                return jsonify(message='You have no permission to access'), 403

        if request.method == 'GET':
            if c.get_role() == 'user' or 'admin':
                return c.get_all_products()
            else:
                return jsonify(message='You have no permission to access'), 403


@app.route('/product/<product>', methods=['GET', 'PUT', 'DELETE'])
def product_get_put_delete_one(product):
    if request.method == 'GET':
        if c.get_role() == 'user' or 'admin':
            return c.get_product_by_name(product)
        else:
                return jsonify(message='You have no permission to access'), 403
        
    if request.method == 'PUT':
        if c.get_role() == 'admin':
            return c.update_product_by_name(product)
        else:
                return jsonify(message='You have no permission to access'), 403
    if request.method == 'DELETE':
        if c.get_role() == 'admin':
            return c.delete_product_by_name(product)
        else:
                return jsonify(message='You have no permission to access'), 403
    

# ------------------ Invoice related endpoints ------------------------

@app.route('/invoice', methods=['POST'])
def invoices_post():
    if c.get_role() == 'admin':
        return c.create_invoice()
    else:
        return jsonify(message='You have no permission to access'), 403


@app.route('/invoice/<user_id>')
def invoice_get(user_id):
    if c.get_role() == 'user' or 'admin':
        return c.get_invoice_by_user_id(user_id)
    else:
        return jsonify(message='You have no permission to access'), 403


# ------------------ localhost connection ------------------------

app.run(host="localhost", port=5000, debug=True)