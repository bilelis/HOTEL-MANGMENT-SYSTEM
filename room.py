"""
Hotel Management System - Room Models
Handles room types, individual rooms, and room management.
"""

from sqlalchemy import Column, String, Integer, Text, ForeignKey, Enum, ARRAY, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import BaseModel
import enum

class RoomStatusEnum(str, enum.Enum):
    """Room status enumeration."""
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"
    CLEANING = "cleaning"

class RoomType(BaseModel):
    """Room type model defining categories of rooms."""
    __tablename__ = "room_types"
    
    name = Column(String(50), nullable=False)
    description = Column(Text)
    base_price = Column(DECIMAL(10, 2), nullable=False)
    max_occupancy = Column(Integer, nullable=False)
    amenities = Column(ARRAY(String), default=[])
    
    # Relationships
    rooms = relationship("Room", back_populates="room_type")
    
    def __repr__(self):
        return f"<RoomType(name='{self.name}', base_price={self.base_price})>"

class Room(BaseModel):
    """Individual room model."""
    __tablename__ = "rooms"
    
    room_number = Column(String(10), unique=True, nullable=False, index=True)
    room_type_id = Column(UUID(as_uuid=True), ForeignKey("room_types.id"), nullable=False)
    floor_number = Column(Integer, nullable=False)
    status = Column(Enum(RoomStatusEnum), default=RoomStatusEnum.AVAILABLE, nullable=False)
    description = Column(Text)
    
    # Relationships
    room_type = relationship("RoomType", back_populates="rooms")
    reservations = relationship("Reservation", back_populates="room")
    
    def __repr__(self):
        return f"<Room(room_number='{self.room_number}', status='{self.status}')>"
    
    @property
    def is_available(self) -> bool:
        """Check if room is available for booking."""
        return self.status == RoomStatusEnum.AVAILABLE
    
    @property
    def is_occupied(self) -> bool:
        """Check if room is currently occupied."""
        return self.status == RoomStatusEnum.OCCUPIED
    
    def set_status(self, status: RoomStatusEnum):
        """Set room status with validation."""
        if isinstance(status, str):
            status = RoomStatusEnum(status)
        self.status = status

