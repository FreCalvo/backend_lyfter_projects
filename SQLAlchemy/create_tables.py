
# ------------ Imports ----------------------
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey


# ------------ Connecting ----------------------
DB_URI = 'postgresql://postgres:FreCalvo90@localhost:5432/SQLAlchemy'
        # dialect+driver://username:password@host:port/database
        # 'postgresql://postgres:'FreCalvo90'@localhost:5432/SQLAlchemy'
engine = create_engine(DB_URI, echo=True)


# ------------ Metadata ----------------------
metadata_obj = MetaData()


# ------------ Define Tables ----------------------
user_table = Table(
		"users",
		metadata_obj,
		Column("id", Integer, primary_key=True),
		Column("name", String(30)),
		Column("full_name", String),)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False), 
    Column("email_address", String, nullable=False),)

cars_table = Table(
    "cars",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=True),
    Column("brand", String, nullable=False),)



# ------------ Persisting our Tables ----------------------
if __name__ == "__main__":
    metadata_obj.create_all(engine)
    print("All tables created (if they did not).")