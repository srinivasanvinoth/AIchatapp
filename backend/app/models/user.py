from pydantic import BaseModel, EmailStr, Field


class UserSignup(BaseModel):
    login_id: str = Field(min_length=4, max_length=50)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    login_id: str
    password: str


class UserResponse(BaseModel):
    user_id: str
    login_id: str
    first_name: str
    last_name: str
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
