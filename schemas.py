from pydantic import BaseModel
from typing import Optional


class ItemBase(BaseModel):
    name: str
    price: float


class ItemCreate(ItemBase):
    name: str
    price: float


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None


class ItemOut(ItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    item_id: int
    quantity: int
    status: Optional[str] = "pending"


class OrderCreate(OrderBase):
    pass


class OrderOut(OrderBase):
    id: int

    class Config:
        from_attributes = True


class SaleBase(BaseModel):
    order_id: int
    total: float


class SaleOut(SaleBase):
    id: int

    class Config:
        from_attributes = True
