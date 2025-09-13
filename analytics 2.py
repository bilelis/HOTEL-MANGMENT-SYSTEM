"""
Hotel Management System - Analytics Schemas
Pydantic models for analytics and dashboard KPI responses.
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date, datetime
from decimal import Decimal

class RevenueResponse(BaseModel):
    """Schema for revenue analytics."""
    total_revenue: float
    room_revenue: float
    fnb_revenue: float
    date: date

class OccupancyRateResponse(BaseModel):
    """Schema for occupancy rate analytics."""
    total_rooms: int
    occupied_rooms: int
    available_rooms: int
    maintenance_rooms: int
    cleaning_rooms: int
    occupancy_rate: float
    date: date

class TopItemSold(BaseModel):
    """Schema for top sold item."""
    item_id: str
    item_name: str
    outlet_name: str
    quantity_sold: int
    revenue: float

class TopItemsResponse(BaseModel):
    """Schema for top items sold analytics."""
    items: List[TopItemSold]
    date: date

class GuestSpending(BaseModel):
    """Schema for guest spending."""
    guest_id: str
    guest_name: str
    room_number: Optional[str] = None
    total_spending: float
    room_charges: float
    fnb_charges: float

class GuestSpendingResponse(BaseModel):
    """Schema for guest spending analytics."""
    guests: List[GuestSpending]
    date: date

class RevenueSplitItem(BaseModel):
    """Schema for revenue split item."""
    category: str
    amount: float
    percentage: float

class RevenueSplitResponse(BaseModel):
    """Schema for revenue split analytics."""
    total_revenue: float
    split: List[RevenueSplitItem]
    date: date

class ARPRResponse(BaseModel):
    """Schema for Average Revenue Per Room."""
    arpr: float
    total_revenue: float
    occupied_rooms: int
    date: date

class DashboardKPIs(BaseModel):
    """Schema for dashboard KPIs summary."""
    revenue_today: RevenueResponse
    occupancy_rate: OccupancyRateResponse
    top_items: TopItemsResponse
    guest_spending: GuestSpendingResponse
    revenue_split: RevenueSplitResponse
    arpr: ARPRResponse

class DateRangeFilter(BaseModel):
    """Schema for date range filtering."""
    start_date: date
    end_date: date

class RevenueByDateResponse(BaseModel):
    """Schema for revenue by date range."""
    dates: List[date]
    room_revenue: List[float]
    fnb_revenue: List[float]
    total_revenue: List[float]

class OutletPerformance(BaseModel):
    """Schema for outlet performance."""
    outlet_id: str
    outlet_name: str
    outlet_type: str
    total_orders: int
    total_revenue: float
    average_order_value: float

class OutletPerformanceResponse(BaseModel):
    """Schema for outlet performance analytics."""
    outlets: List[OutletPerformance]
    date: date

class HourlyRevenue(BaseModel):
    """Schema for hourly revenue breakdown."""
    hour: int
    revenue: float
    orders_count: int

class HourlyRevenueResponse(BaseModel):
    """Schema for hourly revenue analytics."""
    hourly_data: List[HourlyRevenue]
    date: date

class PaymentMethodBreakdown(BaseModel):
    """Schema for payment method breakdown."""
    payment_method: str
    amount: float
    percentage: float
    transaction_count: int

class PaymentMethodResponse(BaseModel):
    """Schema for payment method analytics."""
    breakdown: List[PaymentMethodBreakdown]
    total_amount: float
    date: date

class RoomTypePerformance(BaseModel):
    """Schema for room type performance."""
    room_type_id: str
    room_type_name: str
    total_bookings: int
    total_revenue: float
    occupancy_rate: float
    average_rate: float

class RoomTypePerformanceResponse(BaseModel):
    """Schema for room type performance analytics."""
    room_types: List[RoomTypePerformance]
    date: date

