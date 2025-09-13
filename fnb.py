"""
Hotel Management System - Food & Beverage Models
Handles outlets, menu categories, and items for restaurant/bar operations.
"""

from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, Enum, ARRAY, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import BaseModel
import enum

class OutletTypeEnum(str, enum.Enum):
    """Outlet type enumeration."""
    RESTAURANT = "restaurant"
    BAR = "bar"
    CAFE = "cafe"
    ROOM_SERVICE = "room_service"

class Outlet(BaseModel):
    """Outlet model for F&B locations."""
    __tablename__ = "outlets"
    
    name = Column(String(100), nullable=False)
    type = Column(Enum(OutletTypeEnum), nullable=False)
    location = Column(String(100))
    description = Column(Text)
    operating_hours = Column(JSONB)  # Store opening/closing times for each day
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    categories = relationship("ItemCategory", back_populates="outlet")
    items = relationship("Item", back_populates="outlet")
    orders = relationship("Order", back_populates="outlet")
    
    def __repr__(self):
        return f"<Outlet(name='{self.name}', type='{self.type}')>"
    
    @property
    def is_restaurant(self) -> bool:
        """Check if outlet is a restaurant."""
        return self.type == OutletTypeEnum.RESTAURANT
    
    @property
    def is_bar(self) -> bool:
        """Check if outlet is a bar."""
        return self.type == OutletTypeEnum.BAR
    
    @property
    def is_cafe(self) -> bool:
        """Check if outlet is a café."""
        return self.type == OutletTypeEnum.CAFE
    
    @property
    def is_room_service(self) -> bool:
        """Check if outlet is room service."""
        return self.type == OutletTypeEnum.ROOM_SERVICE
    
    def get_operating_hours(self, day: str = None) -> dict:
        """Get operating hours for a specific day or all days."""
        if not self.operating_hours:
            return {}
        
        if day:
            return self.operating_hours.get(day.lower(), {})
        return self.operating_hours

class ItemCategory(BaseModel):
    """Item category model for menu organization."""
    __tablename__ = "item_categories"
    
    name = Column(String(50), nullable=False)
    description = Column(Text)
    outlet_id = Column(UUID(as_uuid=True), ForeignKey("outlets.id"))
    
    # Relationships
    outlet = relationship("Outlet", back_populates="categories")
    items = relationship("Item", back_populates="category")
    
    def __repr__(self):
        return f"<ItemCategory(name='{self.name}', outlet='{self.outlet.name if self.outlet else 'None'}')>"

class Item(BaseModel):
    """Menu item model."""
    __tablename__ = "items"
    
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category_id = Column(UUID(as_uuid=True), ForeignKey("item_categories.id"))
    outlet_id = Column(UUID(as_uuid=True), ForeignKey("outlets.id"), nullable=False)
    price = Column(DECIMAL(8, 2), nullable=False)
    cost = Column(DECIMAL(8, 2))  # Cost price for profit calculation
    is_available = Column(Boolean, default=True, nullable=False)
    preparation_time = Column(Integer)  # in minutes
    allergens = Column(ARRAY(String), default=[])
    dietary_info = Column(ARRAY(String), default=[])  # vegetarian, vegan, gluten-free, etc.
    image_url = Column(String(255))
    
    # Relationships
    category = relationship("ItemCategory", back_populates="items")
    outlet = relationship("Outlet", back_populates="items")
    order_lines = relationship("OrderLine", back_populates="item")
    
    def __repr__(self):
        return f"<Item(name='{self.name}', price={self.price}, outlet='{self.outlet.name if self.outlet else 'None'}')>"
    
    @property
    def profit_margin(self) -> float:
        """Calculate profit margin percentage."""
        if self.cost and self.cost > 0:
            return float(((self.price - self.cost) / self.cost) * 100)
        return 0.0
    
    @property
    def profit_amount(self) -> float:
        """Calculate profit amount per item."""
        if self.cost:
            return float(self.price - self.cost)
        return float(self.price)
    
    def has_allergen(self, allergen: str) -> bool:
        """Check if item contains specific allergen."""
        return allergen.lower() in [a.lower() for a in (self.allergens or [])]
    
    def is_dietary_compatible(self, dietary_requirement: str) -> bool:
        """Check if item meets dietary requirement."""
        return dietary_requirement.lower() in [d.lower() for d in (self.dietary_info or [])]
    
    def get_item_details(self) -> dict:
        """Get comprehensive item details."""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "cost": float(self.cost) if self.cost else None,
            "is_available": self.is_available,
            "preparation_time": self.preparation_time,
            "allergens": self.allergens or [],
            "dietary_info": self.dietary_info or [],
            "category": self.category.name if self.category else None,
            "outlet": self.outlet.name if self.outlet else None,
            "profit_margin": float(self.profit_margin),
            "image_url": self.image_url
        }

