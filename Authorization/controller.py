# -------------------------------- Imports ---------------------------------------------

from flask import request, jsonify, Response
from db import ProductManager, InvoiceManager, DB_Manager
from JWT_Manager import JWT_Manager


# -------------------------------- Class instances ---------------------------------------------

product_manager = ProductManager()
invoice_manager = InvoiceManager()
db_manager = DB_Manager()
jwt_manager = JWT_Manager('private_key.pem', 'public_key.pem')

# ---------------------------- Products controls -------------------------------------

def create_product():
    data = request.get_json()
    if(data.get('name') == None or data.get('price') == None or data.get('quantity') == None):
        return Response(status=400)
    else:
        try:
            result = product_manager.insert_product(data.get('name'), data.get('price'), data.get('quantity'))
                
            print (f"result: {result}")
            return jsonify(id=result[0], name=result[1], price=result[2], quantity=result[3], entry_date=result[4])
        except Exception as ex:
            return jsonify(message=str(ex)), 400

def get_all_products():
    try:
        list_products = product_manager.get_all_products()
        products = [tuple(row) for row in list_products]
        return jsonify(products)
    except Exception as ex:
        return jsonify(message=str(ex)), 400

def get_product_by_name(name):
    try:
        product = product_manager.get_product_by_name(name)
        product_one = [tuple(row) for row in product]
        return jsonify(product_one)
    except Exception as ex:
        return jsonify(message=str(ex)), 400

def update_product_by_name(product_to_update):
    data = request.get_json()
    if(data.get('name') == None or data.get('price') == None or data.get('quantity') == None):
        return Response(status=400)
    else:
        try:
            result = product_manager.update_product_by_name(product_to_update, data.get('name'), data.get('price'), 
                        data.get('quantity'))
            print(f"result [2]: {result[2]}")
            return jsonify(id=result[0], name=result[1], price=result[2], quantity=result[3])
        except Exception as ex:
            return jsonify(message=str(ex)), 400

def delete_product_by_name(product_to_delete):
    try:
        product_manager.delete_product_by_name(product_to_delete)
        return jsonify(message= f'Product: {product_to_delete} was deleted.')
    except Exception as ex:
        return jsonify(message=str(ex)), 400


# ---------------------------- Invoice controls -------------------------------------

def create_invoice():
    data = request.get_json()
    if(data.get('user_id') == None or data.get('total') == None):
        return Response(status=400)
    else:
        try:
            result = invoice_manager.insert_invoice(data.get('user_id'), data.get('total'))
            return jsonify(id=result[0], user_id=result[1], purchase_date=result[2], total=result[3])
        except Exception as ex:
            return jsonify(message=str(ex)), 400
        
def get_invoice_by_user_id(user_id):
    try:
        result = invoice_manager.get_invoice_by_user_id(user_id)
        print(f"Result: {result}")
        user_invoices = [tuple(row) for row in result]
        return jsonify(user_invoices)
    except Exception as ex:
        return jsonify(message=str(ex)), 400


# ---------------------------- User controls -------------------------------------

def register_user():
    data = request.get_json()  # data is empty
    if(data.get('username') == None or data.get('password') == None):
        return Response(status=400)
    else:
        result = db_manager.insert_user(data.get('username'), data.get('password'), data.get('role'))
        print(f"\n register result: {result} \n")

        user_id = result[0]

        token = jwt_manager.encode({'id':user_id})
        return jsonify(token=token)

def login_user():
    data = request.get_json()  # data is empty
    if(data.get('username') == None or data.get('password') == None):
        return Response(status=400)
    else:
        result = db_manager.get_user(data.get('username'), data.get('password'))
        if(result == None):
            return Response(status=400)
        else:
            user_id = result[0]
            token = jwt_manager.encode({'id':user_id})
            return jsonify(token=token)


def find_user_id_with_token():
    try:
        token = request.headers.get('Authorization') 
        if(token is not None):
            test = token.replace("Bearer ","")
            print(f"test: {test}")
            decoded = jwt_manager.decode(test)
            if decoded is None:
                return Response(status=403)
            
            user_id = decoded['id']
            print(f"\n User id decoded: {user_id} \n")

            user = db_manager.get_user_by_id(user_id)
            return user_id
        else:
            return Response(status=403)
    except Exception as e:
        return Response(status=500)

def get_user_info():
    user_id = find_user_id_with_token()
    user = db_manager.get_user_by_id(user_id)
    return jsonify(id=user_id, username=user[1], user_role=user[3])


# ---------------------------- Role verification -------------------------------------

def get_role():
    user_id = find_user_id_with_token()
    user = db_manager.get_user_by_id(user_id)
    role = user[3]
    return role