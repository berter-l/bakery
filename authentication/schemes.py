from ninja import ModelSchema, Schema, FilterSchema, Field
from pydantic import BaseModel, field_validator
from ninja.errors import ValidationError
from pydantic import EmailStr


class UserLoginSchema(Schema):
    name: str
    password: str


class TokenUpdateSchema(Schema):
    refresh_token: str


class TokenSchema(Schema):
    access_token: str
    refresh_token: str


class RegistrationSchema(Schema):
    username: str
    email: EmailStr
    password: str
    password_confirmation: str


class ProfileSchema(Schema):
    username: str
    balance: float
    email: EmailStr
    


