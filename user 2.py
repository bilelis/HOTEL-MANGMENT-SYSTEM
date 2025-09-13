"""
Hotel Management System - User Model
Handles user authentication and role-based access control.
"""

from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class UserRoleEnum(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "admin"
    RECEPTIONIST = "receptionist"
    CASHIER = "cashier"

class User(BaseModel):
    """User model for authentication and authorization."""
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRoleEnum), nullable=False)
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    created_reservations = relationship("Reservation", back_populates="created_by_user")
    created_orders = relationship("Order", back_populates="created_by_user")
    processed_payments = relationship("Payment", back_populates="processed_by_user")
    audit_logs = relationship("AuditLog", back_populates="changed_by_user")
    
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"
    
    @property
    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.role == UserRoleEnum.ADMIN
    
    @property
    def is_receptionist(self) -> bool:
        """Check if user is receptionist."""
        return self.role == UserRoleEnum.RECEPTIONIST
    
    @property
    def is_cashier(self) -> bool:
        """Check if user is cashier."""
        return self.role == UserRoleEnum.CASHIER
    
    def can_access_reception(self) -> bool:
        """Check if user can access reception features."""
        return self.role in [UserRoleEnum.ADMIN, UserRoleEnum.RECEPTIONIST]
    
    def can_access_fnb(self) -> bool:
        """Check if user can access F&B features."""
        return self.role in [UserRoleEnum.ADMIN, UserRoleEnum.CASHIER]

