"""
Hotel Management System - Guest and Reservation Schemas
Pydantic models for guest and reservation-related API requests and responses.
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from ..models.guest import IDTypeEnum
from ..models.reservation import ReservationStatusEnum

class GuestBase(BaseModel):
    """Base guest schema."""
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: str
    address: Optional[str] = None
    nationality: Optional[str] = None
    id_type: Optional[IDTypeEnum] = None
    id_number: Optional[str] = None
    date_of_birth: Optional[date] = None

class GuestCreate(GuestBase):
    """Schema for creating a guest."""
    
    @validator('phone')
    def validate_phone(cls, v):
        if len(v) < 10:
            raise ValueError('Phone number must be at least 10 characters')
        return v

class GuestUpdate(BaseModel):
    """Schema for updating guest information."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    nationality: Optional[str] = None
    id_type: Optional[IDTypeEnum] = None
    id_number: Optional[str] = None
    date_of_birth: Optional[date] = None

class GuestResponse(GuestBase):
    """Schema for guest response."""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ReservationBase(BaseModel):
    """Base reservation schema."""
    checkin_date: date
    checkout_date: date
    adults: int = 1
    children: int = 0
    special_requests: Optional[str] = None

class ReservationCreate(ReservationBase):
    """Schema for creating a reservation."""
    guest_id: str
    room_id: str
    
    @validator('checkout_date')
    def validate_dates(cls, v, values):
        if 'checkin_date' in values and v <= values['checkin_date']:
            raise ValueError('Checkout date must be after checkin date')
        return v
    
    @validator('adults')
    def validate_adults(cls, v):
        if v <= 0:
            raise ValueError('Number of adults must be greater than 0')
        return v
    
    @validator('children')
    def validate_children(cls, v):
        if v < 0:
            raise ValueError('Number of children cannot be negative')
        return v

class ReservationUpdate(BaseModel):
    """Schema for updating a reservation."""
    checkin_date: Optional[date] = None
    checkout_date: Optional[date] = None
    adults: Optional[int] = None
    children: Optional[int] = None
    special_requests: Optional[str] = None
    status: Optional[ReservationStatusEnum] = None

class ReservationCheckin(BaseModel):
    """Schema for guest check-in."""
    checkin_time: Optional[datetime] = None

class ReservationCheckout(BaseModel):
    """Schema for guest check-out."""
    checkout_time: Optional[datetime] = None

class ReservationResponse(ReservationBase):
    """Schema for reservation response."""
    id: str
    guest_id: str
    room_id: str
    actual_checkin: Optional[datetime] = None
    actual_checkout: Optional[datetime] = None
    total_amount: Decimal
    status: ReservationStatusEnum
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Nested objects
    guest: GuestResponse
    room: "RoomResponse"
    
    class Config:
        from_attributes = True

class ReservationSummary(BaseModel):
    """Schema for reservation summary."""
    id: str
    guest_name: str
    room_number: str
    checkin_date: date
    checkout_date: date
    nights: int
    adults: int
    children: int
    total_amount: float
    status: str

# Import here to avoid circular imports
from .room import RoomResponse
ReservationResponse.model_rebuild()

