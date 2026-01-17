# 'Mapped' allows us to use Python types (like int, str) to define column types.
# 'mapped_column' is the modern way to define database constraints (like primary keys).
# 'relationship' creates the link between this table and other tables.
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from app.db.base import Base # Inheriting from the Base we created earlier

# This class represents a single 'row' in your PostgreSQL 'users' table.
class User(Base):
    # 1. The actual name of the table inside the database.
    __tablename__ = "users"

    # 2. Defines 'id' as the Primary Key (Unique identifier for every user).
    # 'Mapped[int]' tells Python it's an integer; 'mapped_column' tells SQL it's a PK.
    id: Mapped[int] = mapped_column(primary_key=True)

    # 3. Maps the 'name' attribute to a VARCHAR (String) column in SQL.
    name: Mapped[str] = mapped_column(String)

    # 4. Maps the 'age' attribute to an INTEGER column in SQL.
    age: Mapped[int] = mapped_column(Integer)

    # 5. Relationship logic (Foreign Key link).
    # This doesn't exist as a physical column in the 'users' table. 
    # Instead, it's a "virtual" property that allows you to access a user's addresses like: my_user.addresses.
    # 'back_populates' ensures that if you change an address, the user object updates too.
    addresses = relationship("Address", back_populates="user")

