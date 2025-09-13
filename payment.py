"""
Hotel Management System - Payment and Audit Models
Handles financial transactions and audit logging.
"""

from sqlalchemy import Column, String, Text, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import BaseModel
import enum

class PaymentMethodEnum(str, enum.Enum):
    """Payment method enumeration."""
    CASH = "cash"
    CARD = "card"
    MOBILE_PAYMENT = "mobile_payment"
    BANK_TRANSFER = "bank_transfer"

class PaymentTypeEnum(str, enum.Enum):
    """Payment type enumeration."""
    ROOM_CHARGE = "room_charge"
    FNB_CHARGE = "fnb_charge"
    DEPOSIT = "deposit"
    REFUND = "refund"

class PaymentStatusEnum(str, enum.Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class Payment(BaseModel):
    """Payment model for financial transactions."""
    __tablename__ = "payments"
    
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    reservation_id = Column(UUID(as_uuid=True), ForeignKey("reservations.id"))
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(Enum(PaymentMethodEnum), nullable=False)
    payment_type = Column(Enum(PaymentTypeEnum), nullable=False)
    transaction_id = Column(String(100))
    status = Column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.COMPLETED, nullable=False)
    processed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    order = relationship("Order", back_populates="payments")
    reservation = relationship("Reservation", back_populates="payments")
    processed_by_user = relationship("User", back_populates="processed_payments")
    
    def __repr__(self):
        return f"<Payment(amount={self.amount}, type='{self.payment_type}', status='{self.status}')>"
    
    @property
    def is_completed(self) -> bool:
        """Check if payment is completed."""
        return self.status == PaymentStatusEnum.COMPLETED
    
    @property
    def is_room_charge(self) -> bool:
        """Check if payment is for room charges."""
        return self.payment_type == PaymentTypeEnum.ROOM_CHARGE
    
    @property
    def is_fnb_charge(self) -> bool:
        """Check if payment is for F&B charges."""
        return self.payment_type == PaymentTypeEnum.FNB_CHARGE
    
    def get_payment_details(self) -> dict:
        """Get payment details for display."""
        return {
            "id": str(self.id),
            "amount": float(self.amount),
            "payment_method": self.payment_method.value,
            "payment_type": self.payment_type.value,
            "status": self.status.value,
            "transaction_id": self.transaction_id,
            "processed_by": self.processed_by_user.full_name if self.processed_by_user else "System",
            "created_at": self.created_at.isoformat(),
            "order_number": self.order.order_number if self.order else None,
            "reservation_id": str(self.reservation_id) if self.reservation_id else None
        }

class ActionEnum(str, enum.Enum):
    """Audit action enumeration."""
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

class AuditLog(BaseModel):
    """Audit log model for tracking changes."""
    __tablename__ = "audit_logs"
    
    table_name = Column(String(50), nullable=False)
    record_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(Enum(ActionEnum), nullable=False)
    old_values = Column(JSONB)
    new_values = Column(JSONB)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    changed_by_user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog(table='{self.table_name}', action='{self.action}', record_id='{self.record_id}')>"
    
    def get_audit_details(self) -> dict:
        """Get audit log details."""
        return {
            "id": str(self.id),
            "table_name": self.table_name,
            "record_id": str(self.record_id),
            "action": self.action.value,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "changed_by": self.changed_by_user.full_name if self.changed_by_user else "System",
            "changed_at": self.created_at.isoformat()
        }

