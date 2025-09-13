"""
Hotel Management System - Guest Model
Handles guest information and customer management.
"""

from sqlalchemy import Column, String, Date, Text, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class IDTypeEnum(str, enum.Enum):
    """ID type enumeration."""
    PASSPORT = "passport"
    NATIONAL_ID = "national_id"
    DRIVING_LICENSE = "driving_license"

class Guest(BaseModel):
    """Guest model for customer information."""
    __tablename__ = "guests"
    
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), index=True)
    phone = Column(String(20), nullable=False, index=True)
    address = Column(Text)
    nationality = Column(String(50))
    id_type = Column(Enum(IDTypeEnum))
    id_number = Column(String(50))
    date_of_birth = Column(Date)
    
    # Relationships
    reservations = relationship("Reservation", back_populates="guest")
    orders = relationship("Order", back_populates="guest")
    
    def __repr__(self):
        return f"<Guest(name='{self.full_name}', phone='{self.phone}')>"
    
    @property
    def full_name(self) -> str:
        """Get guest's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def display_name(self) -> str:
        """Get display name for UI."""
        return self.full_name
    
    def get_contact_info(self) -> dict:
        """Get guest contact information."""
        return {
            "name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address
        }
    
    def get_identification(self) -> dict:
        """Get guest identification information."""
        return {
            "id_type": self.id_type.value if self.id_type else None,
            "id_number": self.id_number,
            "nationality": self.nationality,
            "date_of_birth": self.date_of_birth
        }

