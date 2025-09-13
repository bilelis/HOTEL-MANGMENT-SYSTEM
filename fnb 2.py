"""
Hotel Management System - F&B Schemas
Pydantic models for food & beverage operations API requests and responses.
"""

from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from ..models.fnb import OutletTypeEnum
from ..models.order import OrderTypeEnum, OrderStatusEnum, PaymentMethodEnum, PaymentStatusEnum

class OutletBase(BaseModel):
    """Base outlet schema."""
    name: str
    type: OutletTypeEnum
    location: Optional[str] = None
    description: Optional[str] = None
    operating_hours: Optional[Dict[str, Any]] = None
    is_active: bool = True

class OutletCreate(OutletBase):
    """Schema for creating an outlet."""
    pass

class OutletUpdate(BaseModel):
    """Schema for updating an outlet."""
    name: Optional[str] = None
    type: Optional[OutletTypeEnum] = None
    location: Optional[str] = None
    description: Optional[str] = None
    operating_hours: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class OutletResponse(OutletBase):
    """Schema for outlet response."""
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ItemCategoryBase(BaseModel):
    """Base item category schema."""
    name: str
    description: Optional[str] = None

class ItemCategoryCreate(ItemCategoryBase):
    """Schema for creating an item category."""
    outlet_id: Optional[str] = None

class ItemCategoryUpdate(BaseModel):
    """Schema for updating an item category."""
    name: Optional[str] = None
    description: Optional[str] = None
    outlet_id: Optional[str] = None

class ItemCategoryResponse(ItemCategoryBase):
    """Schema for item category response."""
    id: str
    outlet_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ItemBase(BaseModel):
    """Base item schema."""
    name: str
    description: Optional[str] = None
    price: Decimal
    cost: Optional[Decimal] = None
    is_available: bool = True
    preparation_time: Optional[int] = None
    allergens: List[str] = []
    dietary_info: List[str] = []
    image_url: Optional[str] = None

class ItemCreate(ItemBase):
    """Schema for creating an item."""
    category_id: Optional[str] = None
    outlet_id: str
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v

class ItemUpdate(BaseModel):
    """Schema for updating an item."""
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    price: Optional[Decimal] = None
    cost: Optional[Decimal] = None
    is_available: Optional[bool] = None
    preparation_time: Optional[int] = None
    allergens: Optional[List[str]] = None
    dietary_info: Optional[List[str]] = None
    image_url: Optional[str] = None

class ItemResponse(ItemBase):
    """Schema for item response."""
    id: str
    category_id: Optional[str] = None
    outlet_id: str
    created_at: datetime
    updated_at: datetime
    
    # Nested objects
    category: Optional[ItemCategoryResponse] = None
    outlet: OutletResponse
    
    class Config:
        from_attributes = True

class OrderLineBase(BaseModel):
    """Base order line schema."""
    item_id: str
    quantity: int
    special_instructions: Optional[str] = None

class OrderLineCreate(OrderLineBase):
    """Schema for creating an order line."""
    
    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than 0')
        return v

class OrderLineResponse(BaseModel):
    """Schema for order line response."""
    id: str
    item_id: str
    quantity: int
    unit_price: Decimal
    line_total: Decimal
    special_instructions: Optional[str] = None
    
    # Nested objects
    item: ItemResponse
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    """Base order schema."""
    table_number: Optional[str] = None
    order_type: OrderTypeEnum = OrderTypeEnum.DINE_IN
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    """Schema for creating an order."""
    outlet_id: str
    guest_id: Optional[str] = None
    reservation_id: Optional[str] = None
    order_lines: List[OrderLineCreate] = []

class OrderUpdate(BaseModel):
    """Schema for updating an order."""
    table_number: Optional[str] = None
    order_type: Optional[OrderTypeEnum] = None
    status: Optional[OrderStatusEnum] = None
    notes: Optional[str] = None

class OrderAddItem(BaseModel):
    """Schema for adding item to order."""
    item_id: str
    quantity: int
    special_instructions: Optional[str] = None

class OrderPayment(BaseModel):
    """Schema for processing order payment."""
    payment_method: PaymentMethodEnum

class OrderResponse(OrderBase):
    """Schema for order response."""
    id: str
    order_number: str
    outlet_id: str
    guest_id: Optional[str] = None
    reservation_id: Optional[str] = None
    status: OrderStatusEnum
    subtotal: Decimal
    tax_amount: Decimal
    service_charge: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    payment_method: Optional[PaymentMethodEnum] = None
    payment_status: PaymentStatusEnum
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Nested objects
    outlet: OutletResponse
    order_lines: List[OrderLineResponse] = []
    
    class Config:
        from_attributes = True

class OrderSummary(BaseModel):
    """Schema for order summary."""
    order_number: str
    outlet: str
    guest: str
    table_number: Optional[str] = None
    order_type: str
    status: str
    subtotal: float
    tax_amount: float
    service_charge: float
    discount_amount: float
    total_amount: float
    payment_status: str
    items_count: int
    created_at: str

