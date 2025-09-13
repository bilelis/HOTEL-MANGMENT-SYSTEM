"""
Hotel Management System - Analytics Router
Handles dashboard KPIs and analytics endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import date, datetime, timedelta
from typing import List
from ..core.database import get_db
from ..core.security import get_current_user
from ..models import *
from ..schemas.analytics import *
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/revenue-today", response_model=RevenueResponse)
async def get_revenue_today(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    📊 Revenue Today - Get today's total revenue breakdown.
    """
    today = date.today()
    
    # Get total revenue for today
    total_revenue_query = db.query(func.sum(Payment.amount)).filter(
        func.date(Payment.created_at) == today,
        Payment.status == PaymentStatusEnumPayment.COMPLETED
    ).scalar() or 0
    
    # Get room revenue for today
    room_revenue_query = db.query(func.sum(Payment.amount)).filter(
        func.date(Payment.created_at) == today,
        Payment.payment_type == PaymentTypeEnum.ROOM_CHARGE,
        Payment.status == PaymentStatusEnumPayment.COMPLETED
    ).scalar() or 0
    
    # Get F&B revenue for today
    fnb_revenue_query = db.query(func.sum(Payment.amount)).filter(
        func.date(Payment.created_at) == today,
        Payment.payment_type == PaymentTypeEnum.FNB_CHARGE,
        Payment.status == PaymentStatusEnumPayment.COMPLETED
    ).scalar() or 0
    
    return RevenueResponse(
        total_revenue=float(total_revenue_query),
        room_revenue=float(room_revenue_query),
        fnb_revenue=float(fnb_revenue_query),
        date=today
    )

@router.get("/occupancy-rate", response_model=OccupancyRateResponse)
async def get_occupancy_rate(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    🏨 Occupancy Rate - Get current room occupancy statistics.
    """
    today = date.today()
    
    # Get room counts by status
    room_counts = db.query(
        Room.status,
        func.count(Room.id).label('count')
    ).group_by(Room.status).all()
    
    # Initialize counts
    total_rooms = 0
    occupied_rooms = 0
    available_rooms = 0
    maintenance_rooms = 0
    cleaning_rooms = 0
    
    # Process room counts
    for status, count in room_counts:
        total_rooms += count
        if status == RoomStatusEnum.OCCUPIED:
            occupied_rooms = count
        elif status == RoomStatusEnum.AVAILABLE:
            available_rooms = count
        elif status == RoomStatusEnum.MAINTENANCE:
            maintenance_rooms = count
        elif status == RoomStatusEnum.CLEANING:
            cleaning_rooms = count
    
    # Calculate occupancy rate (excluding maintenance rooms)
    operational_rooms = total_rooms - maintenance_rooms
    occupancy_rate = (occupied_rooms / operational_rooms * 100) if operational_rooms > 0 else 0
    
    return OccupancyRateResponse(
        total_rooms=total_rooms,
        occupied_rooms=occupied_rooms,
        available_rooms=available_rooms,
        maintenance_rooms=maintenance_rooms,
        cleaning_rooms=cleaning_rooms,
        occupancy_rate=round(occupancy_rate, 2),
        date=today
    )

@router.get("/top-items-sold", response_model=TopItemsResponse)
async def get_top_items_sold(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    🍔 Top 5 Items Sold - Get most sold items with quantities & revenue.
    """
    today = date.today()
    
    # Query top 5 items sold today
    top_items = db.query(
        Item.id,
        Item.name,
        Outlet.name.label('outlet_name'),
        func.sum(OrderLine.quantity).label('quantity_sold'),
        func.sum(OrderLine.line_total).label('revenue')
    ).join(
        OrderLine, Item.id == OrderLine.item_id
    ).join(
        Order, OrderLine.order_id == Order.id
    ).join(
        Outlet, Item.outlet_id == Outlet.id
    ).filter(
        func.date(Order.created_at) == today,
        Order.status.in_([OrderStatusEnum.SERVED, OrderStatusEnum.PAID])
    ).group_by(
        Item.id, Item.name, Outlet.name
    ).order_by(
        func.sum(OrderLine.quantity).desc()
    ).limit(5).all()
    
    items = [
        TopItemSold(
            item_id=str(item.id),
            item_name=item.name,
            outlet_name=item.outlet_name,
            quantity_sold=int(item.quantity_sold),
            revenue=float(item.revenue)
        )
        for item in top_items
    ]
    
    return TopItemsResponse(items=items, date=today)

@router.get("/guest-spending", response_model=GuestSpendingResponse)
async def get_guest_spending(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    👤 Guest Spending - Get ranking of guests by total spending.
    """
    today = date.today()
    
    # Query guest spending for today
    guest_spending = db.query(
        Guest.id,
        Guest.first_name,
        Guest.last_name,
        Room.room_number,
        func.sum(Payment.amount).label('total_spending'),
        func.sum(
            func.case(
                (Payment.payment_type == PaymentTypeEnum.ROOM_CHARGE, Payment.amount),
                else_=0
            )
        ).label('room_charges'),
        func.sum(
            func.case(
                (Payment.payment_type == PaymentTypeEnum.FNB_CHARGE, Payment.amount),
                else_=0
            )
        ).label('fnb_charges')
    ).join(
        Reservation, Guest.id == Reservation.guest_id
    ).join(
        Room, Reservation.room_id == Room.id
    ).outerjoin(
        Payment, or_(
            Payment.reservation_id == Reservation.id,
            and_(
                Payment.order_id.in_(
                    db.query(Order.id).filter(Order.guest_id == Guest.id)
                )
            )
        )
    ).filter(
        func.date(Payment.created_at) == today,
        Payment.status == PaymentStatusEnumPayment.COMPLETED,
        Reservation.status == ReservationStatusEnum.CHECKED_IN
    ).group_by(
        Guest.id, Guest.first_name, Guest.last_name, Room.room_number
    ).order_by(
        func.sum(Payment.amount).desc()
    ).limit(10).all()
    
    guests = [
        GuestSpending(
            guest_id=str(guest.id),
            guest_name=f"{guest.first_name} {guest.last_name}",
            room_number=guest.room_number,
            total_spending=float(guest.total_spending or 0),
            room_charges=float(guest.room_charges or 0),
            fnb_charges=float(guest.fnb_charges or 0)
        )
        for guest in guest_spending
    ]
    
    return GuestSpendingResponse(guests=guests, date=today)

@router.get("/revenue-split", response_model=RevenueSplitResponse)
async def get_revenue_split(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    💰 Revenue Split (Rooms vs F&B) - Pie chart comparing revenue sources.
    """
    today = date.today()
    
    # Get revenue by payment type
    revenue_split = db.query(
        Payment.payment_type,
        func.sum(Payment.amount).label('amount')
    ).filter(
        func.date(Payment.created_at) == today,
        Payment.status == PaymentStatusEnumPayment.COMPLETED
    ).group_by(Payment.payment_type).all()
    
    total_revenue = sum(float(item.amount) for item in revenue_split)
    
    split_items = []
    for item in revenue_split:
        amount = float(item.amount)
        percentage = (amount / total_revenue * 100) if total_revenue > 0 else 0
        
        category = "Rooms" if item.payment_type == PaymentTypeEnum.ROOM_CHARGE else "F&B"
        
        split_items.append(RevenueSplitItem(
            category=category,
            amount=amount,
            percentage=round(percentage, 2)
        ))
    
    return RevenueSplitResponse(
        total_revenue=total_revenue,
        split=split_items,
        date=today
    )

@router.get("/arpr", response_model=ARPRResponse)
async def get_average_revenue_per_room(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    📈 Average Revenue per Room (ARPR) - Calculate ARPR for today.
    """
    today = date.today()
    
    # Get total room revenue for today
    room_revenue = db.query(func.sum(Payment.amount)).filter(
        func.date(Payment.created_at) == today,
        Payment.payment_type == PaymentTypeEnum.ROOM_CHARGE,
        Payment.status == PaymentStatusEnumPayment.COMPLETED
    ).scalar() or 0
    
    # Get number of occupied rooms
    occupied_rooms = db.query(func.count(Room.id)).filter(
        Room.status == RoomStatusEnum.OCCUPIED
    ).scalar() or 0
    
    # Calculate ARPR
    arpr = (float(room_revenue) / occupied_rooms) if occupied_rooms > 0 else 0
    
    return ARPRResponse(
        arpr=round(arpr, 2),
        total_revenue=float(room_revenue),
        occupied_rooms=occupied_rooms,
        date=today
    )

@router.get("/dashboard-kpis", response_model=DashboardKPIs)
async def get_dashboard_kpis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all dashboard KPIs in a single request for efficiency.
    """
    # Get all KPIs
    revenue_today = await get_revenue_today(db, current_user)
    occupancy_rate = await get_occupancy_rate(db, current_user)
    top_items = await get_top_items_sold(db, current_user)
    guest_spending = await get_guest_spending(db, current_user)
    revenue_split = await get_revenue_split(db, current_user)
    arpr = await get_average_revenue_per_room(db, current_user)
    
    return DashboardKPIs(
        revenue_today=revenue_today,
        occupancy_rate=occupancy_rate,
        top_items=top_items,
        guest_spending=guest_spending,
        revenue_split=revenue_split,
        arpr=arpr
    )

@router.get("/outlet-performance", response_model=OutletPerformanceResponse)
async def get_outlet_performance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get outlet performance analytics.
    """
    today = date.today()
    
    outlet_performance = db.query(
        Outlet.id,
        Outlet.name,
        Outlet.type,
        func.count(Order.id).label('total_orders'),
        func.sum(Order.total_amount).label('total_revenue'),
        func.avg(Order.total_amount).label('average_order_value')
    ).outerjoin(
        Order, Outlet.id == Order.outlet_id
    ).filter(
        or_(
            Order.id.is_(None),
            and_(
                func.date(Order.created_at) == today,
                Order.status.in_([OrderStatusEnum.SERVED, OrderStatusEnum.PAID])
            )
        )
    ).group_by(
        Outlet.id, Outlet.name, Outlet.type
    ).all()
    
    outlets = [
        OutletPerformance(
            outlet_id=str(outlet.id),
            outlet_name=outlet.name,
            outlet_type=outlet.type.value,
            total_orders=int(outlet.total_orders or 0),
            total_revenue=float(outlet.total_revenue or 0),
            average_order_value=float(outlet.average_order_value or 0)
        )
        for outlet in outlet_performance
    ]
    
    return OutletPerformanceResponse(outlets=outlets, date=today)

