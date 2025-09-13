"""
Hotel Management System - Reservation Model
Handles room reservations, check-in/check-out processes.
"""

from sqlalchemy import Column, Date, DateTime, Integer, Text, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import BaseModel
import enum
from datetime import date, datetime

class ReservationStatusEnum(str, enum.Enum):
    """Reservation status enumeration."""
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"

class Reservation(BaseModel):
    """Reservation model for room bookings."""
    __tablename__ = "reservations"
    
    guest_id = Column(UUID(as_uuid=True), ForeignKey("guests.id"), nullable=False)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False)
    checkin_date = Column(Date, nullable=False)
    checkout_date = Column(Date, nullable=False)
    actual_checkin = Column(DateTime(timezone=True))
    actual_checkout = Column(DateTime(timezone=True))
    adults = Column(Integer, nullable=False, default=1)
    children = Column(Integer, default=0)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(ReservationStatusEnum), default=ReservationStatusEnum.CONFIRMED, nullable=False)
    special_requests = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    guest = relationship("Guest", back_populates="reservations")
    room = relationship("Room", back_populates="reservations")
    created_by_user = relationship("User", back_populates="created_reservations")
    payments = relationship("Payment", back_populates="reservation")
    orders = relationship("Order", back_populates="reservation")
    
    def __repr__(self):
        return f"<Reservation(guest='{self.guest.full_name if self.guest else 'Unknown'}', room='{self.room.room_number if self.room else 'Unknown'}', status='{self.status}')>"
    
    @property
    def nights(self) -> int:
        """Calculate number of nights."""
        return (self.checkout_date - self.checkin_date).days
    
    @property
    def is_active(self) -> bool:
        """Check if reservation is currently active."""
        return self.status in [ReservationStatusEnum.CONFIRMED, ReservationStatusEnum.CHECKED_IN]
    
    @property
    def is_current(self) -> bool:
        """Check if guest is currently checked in."""
        return self.status == ReservationStatusEnum.CHECKED_IN
    
    @property
    def can_checkin(self) -> bool:
        """Check if guest can check in."""
        today = date.today()
        return (
            self.status == ReservationStatusEnum.CONFIRMED and
            self.checkin_date <= today and
            self.actual_checkin is None
        )
    
    @property
    def can_checkout(self) -> bool:
        """Check if guest can check out."""
        return (
            self.status == ReservationStatusEnum.CHECKED_IN and
            self.actual_checkout is None
        )
    
    def checkin(self, checkin_time: datetime = None):
        """Process guest check-in."""
        if not self.can_checkin:
            raise ValueError("Cannot check in: reservation not eligible")
        
        self.actual_checkin = checkin_time or datetime.now()
        self.status = ReservationStatusEnum.CHECKED_IN
        
        # Update room status
        if self.room:
            from .room import RoomStatusEnum
            self.room.status = RoomStatusEnum.OCCUPIED
    
    def checkout(self, checkout_time: datetime = None):
        """Process guest check-out."""
        if not self.can_checkout:
            raise ValueError("Cannot check out: reservation not eligible")
        
        self.actual_checkout = checkout_time or datetime.now()
        self.status = ReservationStatusEnum.CHECKED_OUT
        
        # Update room status
        if self.room:
            from .room import RoomStatusEnum
            self.room.status = RoomStatusEnum.CLEANING
    
    def cancel(self):
        """Cancel reservation."""
        if self.status == ReservationStatusEnum.CHECKED_IN:
            raise ValueError("Cannot cancel: guest is already checked in")
        
        self.status = ReservationStatusEnum.CANCELLED
        
        # Update room status if needed
        if self.room and self.room.status.value == "occupied":
            from .room import RoomStatusEnum
            self.room.status = RoomStatusEnum.AVAILABLE
    
    def calculate_total_amount(self) -> float:
        """Calculate total amount based on room type and nights."""
        if self.room and self.room.room_type:
            base_amount = float(self.room.room_type.base_price) * self.nights
            return base_amount
        return 0.0
    
    def get_stay_summary(self) -> dict:
        """Get reservation stay summary."""
        return {
            "reservation_id": str(self.id),
            "guest_name": self.guest.full_name if self.guest else "Unknown",
            "room_number": self.room.room_number if self.room else "Unknown",
            "checkin_date": self.checkin_date,
            "checkout_date": self.checkout_date,
            "nights": self.nights,
            "adults": self.adults,
            "children": self.children,
            "total_amount": float(self.total_amount),
            "status": self.status.value
        }

