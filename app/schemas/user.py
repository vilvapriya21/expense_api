from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=30
    )
    password: str = Field(
        ..., min_length=8, max_length=72
    )


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str