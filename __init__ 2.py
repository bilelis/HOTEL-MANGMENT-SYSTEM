"""
Hotel Management System - Schemas Package
Imports all Pydantic schemas for API validation.
"""

from .user import (
    UserBase, UserCreate, UserUpdate, UserChangePassword, 
    UserResponse, UserLogin, Token, TokenData
)
from .room import (
    RoomTypeBase, RoomTypeCreate, RoomTypeUpdate, RoomTypeResponse,
    RoomBase, RoomCreate, RoomUpdate, RoomStatusUpdate, RoomResponse,
    RoomAvailabilityCheck, RoomOccupancyResponse
)
from .guest import (
    GuestBase, GuestCreate, GuestUpdate, GuestResponse,
    ReservationBase, ReservationCreate, ReservationUpdate,
    ReservationCheckin, ReservationCheckout, ReservationResponse,
    ReservationSummary
)
from .fnb import (
    OutletBase, OutletCreate, OutletUpdate, OutletResponse,
    ItemCategoryBase, ItemCategoryCreate, ItemCategoryUpdate, ItemCategoryResponse,
    ItemBase, ItemCreate, ItemUpdate, ItemResponse,
    OrderLineBase, OrderLineCreate, OrderLineResponse,
    OrderBase, OrderCreate, OrderUpdate, OrderAddItem, OrderPayment,
    OrderResponse, OrderSummary
)
from .analytics import (
    RevenueResponse, OccupancyRateResponse, TopItemSold, TopItemsResponse,
    GuestSpending, GuestSpendingResponse, RevenueSplitItem, RevenueSplitResponse,
    ARPRResponse, DashboardKPIs, DateRangeFilter, RevenueByDateResponse,
    OutletPerformance, OutletPerformanceResponse, HourlyRevenue, HourlyRevenueResponse,
    PaymentMethodBreakdown, PaymentMethodResponse, RoomTypePerformance, RoomTypePerformanceResponse
)

__all__ = [
    # User schemas
    "UserBase", "UserCreate", "UserUpdate", "UserChangePassword",
    "UserResponse", "UserLogin", "Token", "TokenData",
    
    # Room schemas
    "RoomTypeBase", "RoomTypeCreate", "RoomTypeUpdate", "RoomTypeResponse",
    "RoomBase", "RoomCreate", "RoomUpdate", "RoomStatusUpdate", "RoomResponse",
    "RoomAvailabilityCheck", "RoomOccupancyResponse",
    
    # Guest and Reservation schemas
    "GuestBase", "GuestCreate", "GuestUpdate", "GuestResponse",
    "ReservationBase", "ReservationCreate", "ReservationUpdate",
    "ReservationCheckin", "ReservationCheckout", "ReservationResponse",
    "ReservationSummary",
    
    # F&B schemas
    "OutletBase", "OutletCreate", "OutletUpdate", "OutletResponse",
    "ItemCategoryBase", "ItemCategoryCreate", "ItemCategoryUpdate", "ItemCategoryResponse",
    "ItemBase", "ItemCreate", "ItemUpdate", "ItemResponse",
    "OrderLineBase", "OrderLineCreate", "OrderLineResponse",
    "OrderBase", "OrderCreate", "OrderUpdate", "OrderAddItem", "OrderPayment",
    "OrderResponse", "OrderSummary",
    
    # Analytics schemas
    "RevenueResponse", "OccupancyRateResponse", "TopItemSold", "TopItemsResponse",
    "GuestSpending", "GuestSpendingResponse", "RevenueSplitItem", "RevenueSplitResponse",
    "ARPRResponse", "DashboardKPIs", "DateRangeFilter", "RevenueByDateResponse",
    "OutletPerformance", "OutletPerformanceResponse", "HourlyRevenue", "HourlyRevenueResponse",
    "PaymentMethodBreakdown", "PaymentMethodResponse", "RoomTypePerformance", "RoomTypePerformanceResponse"
]

