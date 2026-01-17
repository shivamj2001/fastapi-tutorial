# DeclarativeBase is the modern (SQLAlchemy 2.0+) way to define a 
# "registry" that tracks all your database tables.
from sqlalchemy.orm import DeclarativeBase

# 1. We create a class named 'Base' that inherits from DeclarativeBase.
# 2. Every model you create later (like User) will inherit from THIS 'Base' class.

class Base(DeclarativeBase):
    # 'pass' just means we aren't adding any custom behavior yet.
    # This class serves as a shared base for all your database models.
    pass