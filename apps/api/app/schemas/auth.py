"""Authentication request and response schemas (DESIGN.md §23)."""

from pydantic import BaseModel, EmailStr, Field

from app.schemas.user import UserResponse


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, description="Argon2id hashed plaintext password")
    name: str = Field(min_length=1, max_length=120)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MessageResponse(BaseModel):
    message: str
    status: str = "ok"
