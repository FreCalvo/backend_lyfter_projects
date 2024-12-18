from flask import Flask, request
from data_base import PgManager
import controller as c

app = Flask(__name__)

db_manager = PgManager(
    db_name='postgres', user='postgres', password='FreCalvo90', host='localhost')

# ---------------User functions--------------------

@app.route('/users', methods=['GET', 'POST'])
def users_tasks():
    if request.method == 'POST':
        return c.create_user_post()
    if request.method == 'GET':
        return c.list_users_get()

@app.route('/users/<user_id>', methods=['PUT'])
def update_user_status(user_id):
    if request.method == 'PUT':
        return c.update_user_status_put(user_id)
    

# ---------------Car functions--------------------

@app.route('/cars', methods=['GET', 'POST'])
def cars_tasks():
    if request.method == 'POST':
        return c.create_car_post()
    if request.method == 'GET':
        return c.list_cars_get()

@app.route('/cars/<car_id>', methods=['PUT'])
def update_car_status(car_id):
    if request.method == 'PUT':
        return c.update_car_status_put(car_id)


# ---------------Car_rental functions--------------------
@app.route('/rentals', methods=['GET','POST'])
def car_rentals():
    if request.method == 'POST':
        return c.create_rental_post()
    if request.method == 'GET':
        return c.list_rentals_get()

@app.route('/rentals/<rental_id>/return', methods=['PUT'])
def return_car(rental_id):
    return c.return_car_put(rental_id)

@app.route('/rentals/<rental_id>', methods=['PUT'])
def update_rental_status(rental_id):
    if request.method == 'PUT':
        return c.update_rental_status_put(rental_id)


if __name__ == '__main__':
    app.run(debug=True)
