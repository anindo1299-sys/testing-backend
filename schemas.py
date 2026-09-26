from sqlmodel import SQLModel
from pydantic import BaseModel


class UserBase(SQLModel):
    username: str
    role: str = "customer"

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: int

class CategoryBase(SQLModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryPublic(CategoryBase):
    id: int

class ReviewBase(SQLModel):
    text: str
    rating: float

class ReviewCreate(ReviewBase):
    user_id: int
    product_id: int

class ReviewPublic(ReviewBase):
    id: int
    user: UserPublic


class ProductBase(SQLModel):
    name: str
    description: str
    price: float

class ProductCreate(ProductBase):
    category_id: int

class ProductPublic(ProductBase):
    id: int
    category:CategoryPublic
    review: list[ReviewPublic] = []

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
