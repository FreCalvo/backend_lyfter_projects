# ------------ Imports ----------------------
from data_managers import UserManager, CarManager, AddressManager


# ------------ Instance classes ----------------------
user_manager = UserManager()
car_manager = CarManager()
address_manager = AddressManager()


# ------------ Run queries ----------------------

user_manager.create_user("Fredy", "Fredy Calvo")


car_manager.create_car("VW")


address_manager.create_address(1, "fredy.calvo@mail.com")


users = user_manager.get_all_users()
print("Users:", users)


cars = car_manager.get_all_cars()
print("Cars:", cars)


car_manager.update_car(3,user_id=2)


car_manager.delete_car(2)
