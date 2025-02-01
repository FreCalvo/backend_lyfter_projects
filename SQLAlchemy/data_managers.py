

# ------------ Imports ----------------------

from sqlalchemy import create_engine, Table
from sqlalchemy.exc import SQLAlchemyError
from create_tables import user_table, address_table, cars_table  # Import tables


# ------------ Connecting ----------------------
DB_URI = 'postgresql://postgres:FreCalvo90@localhost:5432/SQLAlchemy'
        # dialect+driver://username:password@host:port/database
        # 'postgresql://postgres:'FreCalvo90'@localhost:5432/SQLAlchemy'
engine = create_engine(DB_URI, echo=True)

# ------------ Classes to manage data ----------------------
class UserManager:
    def create_user(self, name, full_name):
        with engine.connect() as connection:
            try:
                insert_query = user_table.insert().values(name=name, full_name=full_name)
                connection.execute(insert_query)
                print(f"User {name} added.")
            except SQLAlchemyError as error:
                print(f"Error adding new user: {error}")
            connection.commit()

    def update_user(self, user_id, name=None, full_name=None):
        with engine.connect() as connection:
            try:
                update_query = user_table.update().where(user_table.c.id == user_id)
                if name:
                    update_query = update_query.values(name=name)
                if full_name:
                    update_query = update_query.values(full_name=full_name)
                connection.execute(update_query)
                print(f"User with ID {user_id} updated.")
            except SQLAlchemyError as error:
                print(f"Error updating user: {error}")
            connection.commit()

    def delete_user(self, user_id):
        with engine.connect() as connection:
            try:
                delete_query = user_table.delete().where(user_table.c.id == user_id)
                connection.execute(delete_query)
                print(f"User with ID: {user_id} deleted.")
            except SQLAlchemyError as error:
                print(f"Error deleting user: {error}")
            connection.commit()

    def get_all_users(self):
        with engine.connect() as connection:
            try:
                select_query = user_table.select()
                users = connection.execute(select_query).fetchall()
                return users
            except SQLAlchemyError as error:
                print(f"Error getting users: {error}")
            connection.commit()

class CarManager:
    def create_car(self,brand, user_id=None):
        with engine.connect() as connection:
            try:
                insert_query = cars_table.insert().values(brand=brand, user_id=user_id)
                connection.execute(insert_query)
                print(f"User {brand} added.")
            except SQLAlchemyError as error:
                print(f"Error adding new car: {error}")
            connection.commit()
    
    def update_car(self, car_id, user_id=None, brand=None):
        with engine.connect() as connection:
            try:
                update_query = cars_table.update().where(cars_table.c.id == car_id)
                if user_id:
                    update_query = update_query.values(user_id=user_id)
                if brand:
                    update_query = update_query.values(brand=brand)
                connection.execute(update_query)
                print(f"Car with ID {car_id} updated.")
            except SQLAlchemyError as error:
                print(f"Error updating car: {error}")
            connection.commit()

    def delete_car(self, car_id):
        with engine.connect() as connection:
            try:
                delete_query = cars_table.delete().where(cars_table.c.id == car_id)
                connection.execute(delete_query)
                print(f"Car with ID: {car_id} deleted.")
            except SQLAlchemyError as error:
                print(f"Error deleting car: {error}")
            connection.commit()

    def get_all_cars(self):
        with engine.connect() as connection:
            try:
                select_query = cars_table.select()
                cars = connection.execute(select_query).fetchall()
                return cars
            except SQLAlchemyError as error:
                print(f"Error getting cars: {error}")
            connection.commit()

class AddressManager:
    def create_address(self, user_id, email_address):
        with engine.connect() as connection:
            try:
                insert_query = address_table.insert().values(user_id=user_id, email_address=email_address)
                connection.execute(insert_query)
                print(f"Email address {email_address} added.")
            except SQLAlchemyError as error:
                print(f"Error adding new address: {error}")
            connection.commit()
    
    def update_address(self, address_id, user_id=None, email_address=None):
        with engine.connect() as connection:
            try:
                update_query = address_table.update().where(address_table.c.id == address_id)
                if user_id:
                    update_query = update_query.values(user_id=user_id)
                if email_address:
                    update_query = update_query.values(email_address=email_address)
                connection.execute(update_query)
                print(f"Address with ID {user_id} updated.")
            except SQLAlchemyError as error:
                print(f"Error updating address: {error}")
            connection.commit()

    def delete_address(self, address_id):
        with engine.connect() as connection:
            try:
                delete_query = address_table.delete().where(address_table.c.id == address_id)
                connection.execute(delete_query)
                print(f"Address with ID: {address_id} deleted.")
            except SQLAlchemyError as error:
                print(f"Error deleting address: {error}")
            connection.commit()

    def get_all_addresses(self):
        with engine.connect() as connection:
            try:
                select_query = address_table.select()
                addresses = connection.execute(select_query).fetchall()
                return addresses
            except SQLAlchemyError as error:
                print(f"Error getting addresses: {error}")
            connection.commit()