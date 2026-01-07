from pydantic import BaseModel, field_validator

class UserCreate(BaseModel):
    name: str
    age: int

    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Age must be positive")
        return v
