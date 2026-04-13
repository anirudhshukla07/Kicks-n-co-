from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    created_at: datetime

    model_config = {'from_attributes': True}


class AuthResponse(BaseModel):
    message: str
    user: UserResponse
