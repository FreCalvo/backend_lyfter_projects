# -------------------------------- Imports ---------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import insert, select, update, delete
from sqlalchemy.sql import func

# -------------------------------- Metadata ---------------------------------------------
metadata_obj = MetaData()

# -------------------------------- Tables Creation ---------------------------------------------
user_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String(30)),
    Column("password", String),
    Column("role", String)
)

product_table = Table(
    "products",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("price", Integer),
    Column("quantity", Integer),
    Column("entry_date", DateTime(timezone=True), server_default=func.now())
)

invoice_table = Table(
    "invoices",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", (ForeignKey("users.id"))),
    Column("purchase_date", DateTime(timezone=True), server_default=func.now()),
    Column("total", Integer),
)

# -------------------------------- Variables Managers ---------------------------------------------

class DB_Manager:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:FreCalvo90@localhost:5432/authorization', echo=True)
        metadata_obj.create_all(self.engine)
        
    def insert_user(self, username, password, role):
        stmt = insert(user_table).returning(user_table.c.id).values(username=username, password=password, role=role)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.all()[0]

    def get_user(self, username, password):
        stmt = select(user_table).where(user_table.c.username == username).where(user_table.c.password == password)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users = result.all()
            if(len(users)==0):
                return None
            else:
                return users[0]

    def get_user_by_id(self, user_id):
        stmt = select(user_table).where(user_table.c.id == user_id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users = result.all()
            print(users)
            if(len(users)==0):
                return None
            else:
                return users[0]
            

class ProductManager:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:FreCalvo90@localhost:5432/authorization', echo=True)
        metadata_obj.create_all(self.engine)

    def insert_product(self, name, price, quantity):
        insert_query = insert(product_table).returning(product_table.c.id, product_table.c.name, product_table.c.price, product_table.c.quantity, product_table.c.entry_date).values(name=name, price=price, quantity=quantity)
        with self.engine.connect() as conn:
            result = conn.execute(insert_query)
            conn.commit()
        return result.all()[0]
    
    def get_all_products(self):
        select_query = select(product_table)
        with self.engine.connect() as conn:
            result = conn.execute(select_query)
        return result.all()
    
    def get_product_by_name(self, name):
        get_by_name_query = select(product_table).where(product_table.c.name == name)
        with self.engine.connect() as conn:
            result = conn.execute(get_by_name_query)
        return result.all()
    

    def update_product_by_name(self, product_to_update, name, price, quantity):
        update_by_name_query = update(product_table).where(product_table.c.name == product_to_update).returning(product_table.c.id, product_table.c.name, product_table.c.price, product_table.c.quantity).values(name=name, price=price, quantity=quantity)
        with self.engine.connect() as conn:
            result = conn.execute(update_by_name_query)
            conn.commit()
        return result.all()[0]
    
    def delete_product_by_name(self, product_to_delete):
        delete_by_name_query = delete(product_table).where(product_table.c.name == product_to_delete)
        with self.engine.connect() as conn:
            result = conn.execute(delete_by_name_query)
            conn.commit()


class InvoiceManager:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:FreCalvo90@localhost:5432/authorization', echo=True)
        metadata_obj.create_all(self.engine)

    def insert_invoice(self, user_id, total):
        insert_query = insert(invoice_table).returning(invoice_table.c.id,invoice_table.c.user_id, invoice_table.c.purchase_date, invoice_table.c.total).values(user_id=user_id, total=total)
        with self.engine.connect() as conn:
            result = conn.execute(insert_query)
            conn.commit()
        return result.all()[0]
    
    def get_invoice_by_user_id(self, user_id):
        get_by_user_id_query = select(invoice_table).where(invoice_table.c.user_id == user_id)
        with self.engine.connect() as conn:
            result = conn.execute(get_by_user_id_query)
        return result.all()
            
