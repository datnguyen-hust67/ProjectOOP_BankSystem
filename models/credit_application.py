"""
File: models/credit_application.py
Credit Application Model - Hồ sơ vay
"""

from datetime import datetime, date
from typing import Optional
from decimal import Decimal


class CreditApplication:
    """
    Model hồ sơ vay
    Phục vụ chức năng: Nhân viên tín dụng
    
    Trạng thái:
    - Pending: Chờ thẩm định
    - UnderReview: Đang thẩm định
    - Approved: Đã duyệt
    - Rejected: Từ chối
    - Disbursed: Đã giải ngân
    - Completed: Hoàn thành
    - Cancelled: Hủy bỏ
    """
    
    def __init__(
        self,
        application_id: int,
        application_number: str,
        customer_id: int,
        product_id: int,
        requested_amount: Decimal,
        requested_term: int,
        purpose: Optional[str] = None,
        status: str = 'Pending',
        assigned_officer_id: Optional[int] = None,
        reviewed_by: Optional[int] = None,
        approved_by: Optional[int] = None,
        application_date: Optional[datetime] = None,
        review_date: Optional[datetime] = None,
        approval_date: Optional[datetime] = None,
        disbursement_date: Optional[datetime] = None,
        notes: Optional[str] = None,
        rejection_reason: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        # Thông tin mở rộng (từ JOIN)
        customer_name: Optional[str] = None,
        customer_phone: Optional[str] = None,
        customer_credit_score: Optional[int] = None,
        product_name: Optional[str] = None,
        officer_name: Optional[str] = None,
        reviewer_name: Optional[str] = None,
        approver_name: Optional[str] = None
    ):
        self.application_id = application_id
        self.application_number = application_number
        self.customer_id = customer_id
        self.product_id = product_id
        self.requested_amount = requested_amount
        self.requested_term = requested_term
        self.purpose = purpose
        self.status = status
        self.assigned_officer_id = assigned_officer_id
        self.reviewed_by = reviewed_by
        self.approved_by = approved_by
        self.application_date = application_date
        self.review_date = review_date
        self.approval_date = approval_date
        self.disbursement_date = disbursement_date
        self.notes = notes
        self.rejection_reason = rejection_reason
        self.created_at = created_at
        self.updated_at = updated_at
        # Extended info
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_credit_score = customer_credit_score
        self.product_name = product_name
        self.officer_name = officer_name
        self.reviewer_name = reviewer_name
        self.approver_name = approver_name
    
    def is_pending(self) -> bool:
        """Kiểm tra hồ sơ đang chờ xử lý"""
        return self.status == 'Pending'
    
    def is_under_review(self) -> bool:
        """Kiểm tra hồ sơ đang thẩm định"""
        return self.status == 'UnderReview'
    
    def is_approved(self) -> bool:
        """Kiểm tra hồ sơ đã được duyệt"""
        return self.status == 'Approved'
    
    def is_rejected(self) -> bool:
        """Kiểm tra hồ sơ bị từ chối"""
        return self.status == 'Rejected'
    
    def can_review(self) -> bool:
        """Kiểm tra có thể thẩm định không"""
        return self.status in ['Pending', 'UnderReview']
    
    def can_approve(self) -> bool:
        """Kiểm tra có thể phê duyệt không"""
        return self.status == 'UnderReview' and self.reviewed_by is not None
    
    def can_disburse(self) -> bool:
        """Kiểm tra có thể giải ngân không"""
        return self.status == 'Approved'
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'application_id': self.application_id,
            'application_number': self.application_number,
            'customer_id': self.customer_id,
            'product_id': self.product_id,
            'requested_amount': float(self.requested_amount),
            'requested_term': self.requested_term,
            'purpose': self.purpose,
            'status': self.status,
            'assigned_officer_id': self.assigned_officer_id,
            'reviewed_by': self.reviewed_by,
            'approved_by': self.approved_by,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'review_date': self.review_date.isoformat() if self.review_date else None,
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'disbursement_date': self.disbursement_date.isoformat() if self.disbursement_date else None,
            'notes': self.notes,
            'rejection_reason': self.rejection_reason,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_credit_score': self.customer_credit_score,
            'product_name': self.product_name,
            'officer_name': self.officer_name
        }
    
    def __repr__(self) -> str:
        return f"CreditApp(id={self.application_id}, number='{self.application_number}', status='{self.status}')"
