"""
File: 13_credit_officer_controller_FIXED.py
Credit Officer Controller - FIXED VERSION
Thêm method get_statistics() để lấy TOÀN BỘ applications
"""

from typing import Tuple, Optional, List
from services.credit_service import CreditService
from models.credit_application import CreditApplication


class CreditOfficerController:
    """Credit Officer Controller - FIXED"""
    
    def __init__(self, credit_service: CreditService):
        self.credit_service = credit_service
        self.current_user = None
        self.current_employee = None
    
    def set_current_user(self, user: dict, employee):
        """Set current logged in user"""
        self.current_user = user
        self.current_employee = employee
    
    def create_application(self, customer_id: int, product_id: int, 
                          requested_amount: str, requested_term: int, 
                          purpose: str) -> Tuple[bool, Optional[int], str]:
        """UC03.1: Tạo hồ sơ vay"""
        if not self.current_employee:
            return False, None, "Chưa đăng nhập"
        
        return self.credit_service.create_loan_application(
            customer_id=customer_id,
            product_id=product_id,
            requested_amount=requested_amount,
            requested_term=requested_term,
            purpose=purpose,
            assigned_officer_id=self.current_employee.employee_id
        )
    
    def start_review(self, application_id: int) -> Tuple[bool, str]:
        """UC03.2: Bắt đầu thẩm định"""
        if not self.current_employee:
            return False, "Chưa đăng nhập"
        
        return self.credit_service.start_assessment(
            application_id=application_id,
            officer_id=self.current_employee.employee_id
        )
    
    def complete_assessment(self, application_id: int, cic_score: int,
                          risk_level: str, recommended_amount: str,
                          recommended_rate: str, notes: str = "") -> Tuple[bool, str]:
        """UC03.2: Hoàn thành thẩm định"""
        return self.credit_service.complete_assessment(
            application_id=application_id,
            cic_score=cic_score,
            risk_level=risk_level,
            recommended_amount=recommended_amount,
            recommended_rate=recommended_rate,
            notes=notes
        )
    
    def approve_application(self, application_id: int, 
                           notes: str = "") -> Tuple[bool, str]:
        """UC03.3: Phê duyệt hồ sơ"""
        if not self.current_employee:
            return False, "Chưa đăng nhập"
        
        return self.credit_service.approve_application(
            application_id=application_id,
            approver_id=self.current_employee.employee_id,
            notes=notes
        )
    
    def reject_application(self, application_id: int, 
                          rejection_reason: str) -> Tuple[bool, str]:
        """UC03.8: Từ chối hồ sơ"""
        if not self.current_employee:
            return False, "Chưa đăng nhập"
        
        return self.credit_service.reject_application(
            application_id=application_id,
            approver_id=self.current_employee.employee_id,
            rejection_reason=rejection_reason
        )
    
    def disburse_loan(self, application_id: int, 
                     disbursement_method: str = "BankTransfer") -> Tuple[bool, str]:
        """UC03.4: Giải ngân"""
        if not self.current_employee:
            return False, "Chưa đăng nhập"
        
        return self.credit_service.disburse_loan(
            application_id=application_id,
            disbursed_by=self.current_employee.employee_id,
            disbursement_method=disbursement_method
        )
    
    def get_application_details(self, application_id: int) -> Optional[CreditApplication]:
        """Lấy chi tiết hồ sơ"""
        return self.credit_service.get_application_details(application_id)
    
    def get_applications_by_status(self, status: str) -> List[CreditApplication]:
        """Lấy danh sách hồ sơ theo trạng thái"""
        return self.credit_service.get_applications_by_status(status)
    
    def get_my_applications(self) -> List[CreditApplication]:
        """Lấy danh sách hồ sơ của officer hiện tại"""
        if not self.current_employee:
            return []
        
        return self.credit_service.get_my_applications(self.current_employee.employee_id)
    
    def get_all_applications(self) -> List[CreditApplication]:
        """Lấy tất cả hồ sơ"""
        return self.credit_service.get_all_applications()
    
    def get_statistics(self) -> dict:
        """
        CRITICAL FIX: Lấy thống kê TOÀN BỘ hồ sơ
        (Không chỉ của officer hiện tại)
        """
        return self.credit_service.get_statistics()
    
    def get_my_statistics(self) -> dict:
        """Lấy thống kê hồ sơ của officer hiện tại"""
        if not self.current_employee:
            return {
                'total': 0,
                'pending': 0,
                'under_review': 0,
                'approved': 0,
                'rejected': 0,
                'disbursed': 0
            }
        
        return self.credit_service.get_officer_statistics(self.current_employee.employee_id)