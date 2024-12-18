from flask import request, jsonify
from data_base import PgManager


db_manager = PgManager(
    db_name='postgres', user='postgres', password='FreCalvo90', host='localhost')

# -----Users Management-----

def create_user_post():
    new_user = request.get_json()
    name = new_user['name']
    email = new_user['email']
    username = new_user['username']
    password = new_user['password']
    birth_date = new_user['birth_date']
    account_status = new_user['account_status']

    try:
        new_created_user = db_manager.execute_query_one('INSERT INTO lyfter_car_rental.users(name, email, username, password, birth_date, account_status) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *',
                    (name, email, username, password, birth_date, account_status))
        db_manager.close_connection()
        return jsonify(new_created_user)
    except Exception as ex:
        return jsonify(message=str(ex)), 400


def update_user_status_put(user_id):
    updated_user = request.get_json()
    account_status = updated_user['status']

    try:
        update_query = '''
            UPDATE lyfter_car_rental.users 
            SET account_status = %s 
            WHERE id = %s
            RETURNING *;
        '''
        updated_user = db_manager.execute_query_one(update_query, (account_status, user_id))
        db_manager.close_connection()
        if not updated_user:
            return jsonify(message="User not found"), 404
        return jsonify(updated_user)
    except Exception as ex:
        # En caso de error, retornar el mensaje de error
        return jsonify(message=str(ex)), 400


def list_users_get():
    try:
        filters = request.args
        
        query = "SELECT * FROM lyfter_car_rental.users WHERE TRUE"
        params = []

        if 'username' in filters:
            query += " AND username = %s"
            params.append(filters['username'])

        if 'email' in filters:
            query += " AND email = %s"
            params.append(filters['email'])

        if 'account_status' in filters:
            query += " AND account_status = %s"
            params.append(filters['account_status'])

        if 'name' in filters:
            query += " AND name ILIKE %s"
            params.append(f"%{filters['name']}%")

        if 'birth_date' in filters:
            query += " AND birth_date = %s"
            params.append(filters['birth_date'])

        users = db_manager.execute_query_all(query, tuple(params))
        
        if not users:
            return jsonify(message="No users found matching the criteria."), 404

        return jsonify(users=users), 200

    except Exception as ex:
        return jsonify(message=str(ex)), 400


# -----Cars Management-----

def create_car_post():
    new_car = request.get_json()
    brand = new_car['brand']
    model = new_car['model']
    year_of_manufacture = new_car['year_of_manufacture']
    status = new_car['status']

    print(brand, model, year_of_manufacture, status)

    try:
        new_created_car = db_manager.execute_query_one('INSERT INTO lyfter_car_rental.cars(brand, model, year_of_manufacture, status) VALUES (%s, %s, %s, %s) RETURNING *',
                (brand, model, year_of_manufacture, status))
        db_manager.close_connection()
        return jsonify(new_created_car)
    except Exception as ex:
        return jsonify(message=str(ex)), 400


def update_car_status_put(car_id):
    db_manager.create_connection()
    updated_car = request.get_json()
    status = updated_car['status']

    try:
        updated_car = db_manager.execute_query_one('''
            UPDATE lyfter_car_rental.cars 
            SET status = %s 
            WHERE id = %s
            RETURNING *;
        ''', (status, car_id))
        db_manager.close_connection()
        if not updated_car:
            return jsonify(message="Car not found"), 404
        return jsonify(updated_car)
    except Exception as ex:
        return jsonify(message=str(ex)), 400
    

def list_cars_get():
    try:
        filters = request.args
        
        query = "SELECT * FROM lyfter_car_rental.cars WHERE TRUE"
        params = []

        if 'brand' in filters:
            query += " AND brand = %s"
            params.append(filters['brand'])

        if 'model' in filters:
            query += " AND model = %s"
            params.append(filters['model'])

        if 'year_of_manufacture' in filters:
            query += " AND year_of_manufacture = %s"
            params.append(filters['year_of_manufacture'])

        if 'status' in filters:
            query += " AND status = %s"
            params.append(filters['status'])

        cars = db_manager.execute_query_all(query, tuple(params))
        
        if not cars:
            return jsonify(message="No cars found matching the criteria."), 404

        return jsonify(users=cars), 200

    except Exception as ex:
        return jsonify(message=str(ex)), 400


# -----Car_rental Management-----

# Funtcion verifies user is active and car is available before creating Rental.
def create_rental_post():
    new_rental = request.get_json()
    user_id = new_rental['user_id']
    car_id = new_rental['car_id']
    rental_status = new_rental['rental_status']

    print(user_id, car_id, rental_status)

    try:
        user_verification = db_manager.execute_query_one('''
            SELECT * 
            FROM lyfter_car_rental.users 
            WHERE id = %s AND account_status = 'active'
        ''', (user_id,))

        if not user_verification:
            return jsonify(message="User not found or not active."), 404
        
        car_verification = db_manager.execute_query_one('''
            SELECT * 
            FROM lyfter_car_rental.cars 
            WHERE id = %s AND status = 'available'
        ''', (car_id,))

        if not car_verification:
            return jsonify(message="Car not found or not available."), 404

        new_created_rental = db_manager.execute_query_one('INSERT INTO lyfter_car_rental.car_rentals (user_id, car_id, rental_status) VALUES (%s, %s, %s) RETURNING *',
                    (user_id, car_id, rental_status))
        
        db_manager.execute_query_all('''
            UPDATE lyfter_car_rental.cars 
            SET status = 'rented' 
            WHERE id = %s
        ''', (car_id,))

        db_manager.close_connection()
        return jsonify(new_created_rental)
    except Exception as ex:
        return jsonify(message=str(ex)), 400

# Function verifies rental is active, returns car to available and sets rental status to completed
def return_car_put(rental_id):
    try:
        rental_id = int(rental_id)
        print(f"Converted rental_id to integer: {rental_id}")

        rental = db_manager.execute_query_one('''
            SELECT * 
            FROM lyfter_car_rental.car_rentals 
            WHERE rental_id = %s AND rental_status = 'active'
        ''', (rental_id,))

        if not rental:
            return jsonify(message="Rental not found or already completed."), 404

        car_id = rental[2]

        if not rental_id:
            return jsonify(message="Rental ID is invalid."), 400

        db_manager.execute_query_all('''
            UPDATE lyfter_car_rental.cars 
            SET status = 'available' 
            WHERE id = %s
        ''', (car_id,))

        db_manager.execute_query_all('''
            UPDATE lyfter_car_rental.car_rentals
            SET rental_status = 'completed' 
            WHERE rental_id = %s
        ''', (rental_id,)) 

        db_manager.close_connection()
        return jsonify(message="Car returned successfully and rental completed."), 200

    except Exception as ex:
        print(f"Error: {ex}")  # Imprimir detalles del error
        return jsonify(message=str(ex)), 400


def update_rental_status_put(rental_id):
    updated_rental = request.get_json()
    rental_status = updated_rental['rental_status']

    try:
        updated_rental = db_manager.execute_query_one('''
            UPDATE lyfter_car_rental.car_rentals
            SET rental_status = %s 
            WHERE rental_id = %s
            RETURNING *;
        ''', (rental_status, rental_id))
        db_manager.close_connection()
        if not updated_rental:
            return jsonify(message="Rental not found"), 404
        return jsonify(updated_rental)
    except Exception as ex:
        return jsonify(message=str(ex)), 400


def list_rentals_get():
    try:
        filters = request.args
        
        query = "SELECT * FROM lyfter_car_rental.car_rentals WHERE TRUE"
        params = []

        if 'user_id' in filters:
            query += " AND user_id = %s"
            params.append(filters['user_id'])

        if 'car_id' in filters:
            query += " AND car_id = %s"
            params.append(filters['car_id'])

        if 'rental_date' in filters:
            query += " AND rental_date ILIKE = %s"
            params.append(filters['rental_date'])

        if 'rental_status' in filters:
            query += " AND rental_status = %s"
            params.append(filters['rental_status'])

        rentals = db_manager.execute_query_all(query, tuple(params))
        
        if not rentals:
            return jsonify(message="No cars found matching the criteria."), 404

        return jsonify(users=rentals), 200

    except Exception as ex:
        return jsonify(message=str(ex)), 400