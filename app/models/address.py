# 'ForeignKey' is the tool used to create a link to another table.
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from app.db.base import Base

# This class represents a single 'row' in your 'addresses' table.
class Address(Base):
    # 1. The name of the table in the database.
    __tablename__ = "addresses"

    # 2. The unique ID for each specific address entry.
    id: Mapped[int] = mapped_column(primary_key=True)

    # 3. A column to store the email string.
    email: Mapped[str] = mapped_column(String)

    # 4. THE LINK (Foreign Key):
    # This column stores the 'id' of the user who owns this address.
    # If User #5 is deleted, this link helps the database maintain "Referential Integrity."
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # 5. RELATIONSHIP:
    # This sets up a relationship to the User model, allowing easy access to the user who owns this address.
    user = relationship("User", back_populates="addresses")