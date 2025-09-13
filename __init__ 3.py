"""
Hotel Management System - Models Package
Imports all database models and sets up relationships.
"""

from .base import BaseModel, TimestampMixin
from .user import User, UserRoleEnum
from .room import Room, RoomType, RoomStatusEnum
from .guest import Guest, IDTypeEnum
from .reservation import Reservation, ReservationStatusEnum
from .fnb import Outlet, ItemCategory, Item, OutletTypeEnum
from .order import Order, OrderLine, OrderTypeEnum, OrderStatusEnum, PaymentMethodEnum, PaymentStatusEnum
from .payment import Payment, AuditLog, PaymentMethodEnum as PaymentMethodEnumPayment, PaymentTypeEnum, PaymentStatusEnum as PaymentStatusEnumPayment, ActionEnum

# Import the base for creating tables
from ..core.database import Base

# All models for easy import
__all__ = [
    "BaseModel",
    "TimestampMixin",
    "User",
    "UserRoleEnum",
    "Room",
    "RoomType", 
    "RoomStatusEnum",
    "Guest",
    "IDTypeEnum",
    "Reservation",
    "ReservationStatusEnum",
    "Outlet",
    "ItemCategory",
    "Item",
    "OutletTypeEnum",
    "Order",
    "OrderLine",
    "OrderTypeEnum",
    "OrderStatusEnum",
    "PaymentMethodEnum",
    "PaymentStatusEnum",
    "Payment",
    "AuditLog",
    "PaymentTypeEnum",
    "ActionEnum",
    "Base"
]

