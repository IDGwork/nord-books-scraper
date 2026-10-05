from decimal import Decimal

from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(min_length=1)
    availability: int = Field(ge=0)
    upc: str = Field(pattern=r"^[0-9a-f]{16}$")
    price_excl_tax: Decimal = Field(ge=0, decimal_places=2)
    tax: Decimal = Field(ge=0, decimal_places=2)
