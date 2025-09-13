"""
Hotel Management System - Order Models
Handles F&B orders, order lines, and transaction processing.
"""

from sqlalchemy import Column, String, Integer, Text, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import BaseModel
import enum
from datetime import datetime

class OrderTypeEnum(str, enum.Enum):
    """Order type enumeration."""
    DINE_IN = "dine_in"
    TAKEAWAY = "takeaway"
    ROOM_SERVICE = "room_service"
    DELIVERY = "delivery"

class OrderStatusEnum(str, enum.Enum):
    """Order status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    SERVED = "served"
    PAID = "paid"
    CANCELLED = "cancelled"

class PaymentMethodEnum(str, enum.Enum):
    """Payment method enumeration."""
    CASH = "cash"
    CARD = "card"
    ROOM_CHARGE = "room_charge"
    MOBILE_PAYMENT = "mobile_payment"

class PaymentStatusEnum(str, enum.Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PAID = "paid"
    REFUNDED = "refunded"

class Order(BaseModel):
    """Order model for F&B transactions."""
    __tablename__ = "orders"
    
    order_number = Column(String(20), unique=True, nullable=False, index=True)
    outlet_id = Column(UUID(as_uuid=True), ForeignKey("outlets.id"), nullable=False)
    guest_id = Column(UUID(as_uuid=True), ForeignKey("guests.id"))  # NULL if walk-in customer
    reservation_id = Column(UUID(as_uuid=True), ForeignKey("reservations.id"))  # Link to guest stay if applicable
    table_number = Column(String(10))
    order_type = Column(Enum(OrderTypeEnum), default=OrderTypeEnum.DINE_IN, nullable=False)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING, nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False, default=0)
    tax_amount = Column(DECIMAL(10, 2), nullable=False, default=0)
    service_charge = Column(DECIMAL(10, 2), default=0)
    discount_amount = Column(DECIMAL(10, 2), default=0)
    total_amount = Column(DECIMAL(10, 2), nullable=False, default=0)
    payment_method = Column(Enum(PaymentMethodEnum))
    payment_status = Column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING, nullable=False)
    notes = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    outlet = relationship("Outlet", back_populates="orders")
    guest = relationship("Guest", back_populates="orders")
    reservation = relationship("Reservation", back_populates="orders")
    created_by_user = relationship("User", back_populates="created_orders")
    order_lines = relationship("OrderLine", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order")
    
    def __repr__(self):
        return f"<Order(order_number='{self.order_number}', total={self.total_amount}, status='{self.status}')>"
    
    @property
    def is_paid(self) -> bool:
        """Check if order is paid."""
        return self.payment_status == PaymentStatusEnum.PAID
    
    @property
    def is_pending(self) -> bool:
        """Check if order is pending."""
        return self.status == OrderStatusEnum.PENDING
    
    @property
    def is_completed(self) -> bool:
        """Check if order is completed."""
        return self.status in [OrderStatusEnum.SERVED, OrderStatusEnum.PAID]
    
    @property
    def can_be_modified(self) -> bool:
        """Check if order can be modified."""
        return self.status in [OrderStatusEnum.PENDING, OrderStatusEnum.CONFIRMED]
    
    def calculate_totals(self):
        """Calculate order totals based on order lines."""
        self.subtotal = sum(float(line.line_total) for line in self.order_lines)
        
        # Calculate tax (10% of subtotal)
        self.tax_amount = self.subtotal * 0.10
        
        # Calculate total
        self.total_amount = self.subtotal + self.tax_amount + float(self.service_charge or 0) - float(self.discount_amount or 0)
    
    def add_item(self, item, quantity: int, special_instructions: str = None):
        """Add item to order."""
        if not self.can_be_modified:
            raise ValueError("Cannot modify order: order is not in modifiable state")
        
        # Check if item already exists in order
        existing_line = next((line for line in self.order_lines if line.item_id == item.id), None)
        
        if existing_line:
            existing_line.quantity += quantity
            existing_line.line_total = existing_line.quantity * existing_line.unit_price
        else:
            order_line = OrderLine(
                order_id=self.id,
                item_id=item.id,
                quantity=quantity,
                unit_price=item.price,
                line_total=item.price * quantity,
                special_instructions=special_instructions
            )
            self.order_lines.append(order_line)
        
        self.calculate_totals()
    
    def remove_item(self, item_id: str):
        """Remove item from order."""
        if not self.can_be_modified:
            raise ValueError("Cannot modify order: order is not in modifiable state")
        
        self.order_lines = [line for line in self.order_lines if str(line.item_id) != item_id]
        self.calculate_totals()
    
    def confirm_order(self):
        """Confirm the order."""
        if self.status != OrderStatusEnum.PENDING:
            raise ValueError("Can only confirm pending orders")
        
        self.status = OrderStatusEnum.CONFIRMED
    
    def mark_as_preparing(self):
        """Mark order as being prepared."""
        if self.status != OrderStatusEnum.CONFIRMED:
            raise ValueError("Can only mark confirmed orders as preparing")
        
        self.status = OrderStatusEnum.PREPARING
    
    def mark_as_ready(self):
        """Mark order as ready for pickup/serving."""
        if self.status != OrderStatusEnum.PREPARING:
            raise ValueError("Can only mark preparing orders as ready")
        
        self.status = OrderStatusEnum.READY
    
    def mark_as_served(self):
        """Mark order as served."""
        if self.status != OrderStatusEnum.READY:
            raise ValueError("Can only mark ready orders as served")
        
        self.status = OrderStatusEnum.SERVED
    
    def process_payment(self, payment_method: PaymentMethodEnum):
        """Process payment for the order."""
        if self.payment_status == PaymentStatusEnum.PAID:
            raise ValueError("Order is already paid")
        
        self.payment_method = payment_method
        self.payment_status = PaymentStatusEnum.PAID
        self.status = OrderStatusEnum.PAID
    
    def cancel_order(self):
        """Cancel the order."""
        if self.status in [OrderStatusEnum.SERVED, OrderStatusEnum.PAID]:
            raise ValueError("Cannot cancel served or paid orders")
        
        self.status = OrderStatusEnum.CANCELLED
    
    def get_order_summary(self) -> dict:
        """Get order summary for display."""
        return {
            "order_number": self.order_number,
            "outlet": self.outlet.name if self.outlet else "Unknown",
            "guest": self.guest.full_name if self.guest else "Walk-in",
            "table_number": self.table_number,
            "order_type": self.order_type.value,
            "status": self.status.value,
            "subtotal": float(self.subtotal),
            "tax_amount": float(self.tax_amount),
            "service_charge": float(self.service_charge),
            "discount_amount": float(self.discount_amount),
            "total_amount": float(self.total_amount),
            "payment_status": self.payment_status.value,
            "items_count": len(self.order_lines),
            "created_at": self.created_at.isoformat()
        }

class OrderLine(BaseModel):
    """Order line model for individual items in an order."""
    __tablename__ = "order_lines"
    
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(8, 2), nullable=False)
    line_total = Column(DECIMAL(10, 2), nullable=False)
    special_instructions = Column(Text)
    
    # Relationships
    order = relationship("Order", back_populates="order_lines")
    item = relationship("Item", back_populates="order_lines")
    
    def __repr__(self):
        return f"<OrderLine(item='{self.item.name if self.item else 'Unknown'}', quantity={self.quantity}, total={self.line_total})>"
    
    def calculate_line_total(self):
        """Calculate line total based on quantity and unit price."""
        self.line_total = self.quantity * self.unit_price
    
    def get_line_details(self) -> dict:
        """Get order line details."""
        return {
            "item_name": self.item.name if self.item else "Unknown",
            "quantity": self.quantity,
            "unit_price": float(self.unit_price),
            "line_total": float(self.line_total),
            "special_instructions": self.special_instructions
        }

