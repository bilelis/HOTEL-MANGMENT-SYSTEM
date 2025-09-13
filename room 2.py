"""
Hotel Management System - Room Schemas
Pydantic models for room-related API requests and responses.
"""

from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from ..models.room import RoomStatusEnum

class RoomTypeBase(BaseModel):
    """Base room type schema."""
    name: str
    description: Optional[str] = None
    base_price: Decimal
    max_occupancy: int
    amenities: List[str] = []

class RoomTypeCreate(RoomTypeBase):
    """Schema for creating a room type."""
    
    @validator('base_price')
    def validate_base_price(cls, v):
        if v <= 0:
            raise ValueError('Base price must be greater than 0')
        return v
    
    @validator('max_occupancy')
    def validate_max_occupancy(cls, v):
        if v <= 0:
            raise ValueError('Max occupancy must be greater than 0')
        return v

class RoomTypeUpdate(BaseModel):
    """Schema for updating a room type."""
    name: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[Decimal] = None
    max_occupancy: Optional[int] = None
    amenities: Optional[List[str]] = None

class RoomTypeResponse(RoomTypeBase):
    """Schema for room type response."""
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    """Base room schema."""
    room_number: str
    floor_number: int
    status: RoomStatusEnum = RoomStatusEnum.AVAILABLE
    description: Optional[str] = None

class RoomCreate(RoomBase):
    """Schema for creating a room."""
    room_type_id: str
    
    @validator('floor_number')
    def validate_floor_number(cls, v):
        if v <= 0:
            raise ValueError('Floor number must be greater than 0')
        return v

class RoomUpdate(BaseModel):
    """Schema for updating a room."""
    room_number: Optional[str] = None
    room_type_id: Optional[str] = None
    floor_number: Optional[int] = None
    status: Optional[RoomStatusEnum] = None
    description: Optional[str] = None

class RoomStatusUpdate(BaseModel):
    """Schema for updating room status."""
    status: RoomStatusEnum

class RoomResponse(RoomBase):
    """Schema for room response."""
    id: str
    room_type_id: str
    room_type: RoomTypeResponse
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class RoomAvailabilityCheck(BaseModel):
    """Schema for checking room availability."""
    checkin_date: datetime
    checkout_date: datetime
    room_type_id: Optional[str] = None
    
    @validator('checkout_date')
    def validate_dates(cls, v, values):
        if 'checkin_date' in values and v <= values['checkin_date']:
            raise ValueError('Checkout date must be after checkin date')
        return v

class RoomOccupancyResponse(BaseModel):
    """Schema for room occupancy statistics."""
    total_rooms: int
    occupied_rooms: int
    available_rooms: int
    maintenance_rooms: int
    cleaning_rooms: int
    occupancy_rate: float

