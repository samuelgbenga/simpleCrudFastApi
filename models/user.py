from sqlalchemy import Integer, String, Table, Column

from config.database import meta

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('password', String(100), nullable=False)
)