from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    role: str
    review: list["Review"] = Relationship(back_populates="user")

class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    product: list["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str
    price: float
    category_id: int = Field(foreign_key="category.id")
    category: Category = Relationship(back_populates="product")
    review: list["Review"] = Relationship(back_populates="product")

class Review(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    rating: float

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates='review')

    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="review")

