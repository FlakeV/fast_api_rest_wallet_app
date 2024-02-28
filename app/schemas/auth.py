from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserBase(BaseModel):
    username: str = Field(description="Username", min_length=3, max_length=20)
    email: EmailStr = Field(description="Email")
    phone: PhoneNumber = Field(description="Phone", default="+79999999999")


class UserAdd(UserBase):
    password: str = Field(description="Password", min_length=8)


class User(UserBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
