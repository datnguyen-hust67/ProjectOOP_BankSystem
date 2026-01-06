"""
File: services/credit_service.py
Credit Service - Business logic xử lý tín dụng
"""

from typing import List, Optional, Tuple
from decimal import Decimal
from datetime import datetime
from repositories.credit_application_repository import CreditApplicationRepository
from models.credit_application import CreditApplication


class CreditService:
    """
    Service xử lý nghiệp vụ tín dụng
    Phục vụ: Nhân viên tín dụng
    """

    def __init__(self, credit_application_repository):
        self.credit_repo = credit_application_repository 
    
    def create_loan_application(self, customer_id: int, product_id: int,
                           requested_amount: str, requested_term: int,
                           purpose: str, assigned_officer_id: int) -> Tuple[bool, Optional[int], str]:
        """UC03.1: Tạo hồ sơ vay - SIMPLIFIED"""
        try:
            # Validate amount
            try:
                amount = float(requested_amount)
                if amount <= 0:
                    return False, None, "Số tiền vay phải lớn hơn 0"
            except (ValueError, TypeError):
                return False, None, "Số tiền vay không hợp lệ"
            
            # Validate term
            try:
                term = int(requested_term)
                if term <= 0:
                    return False, None, "Kỳ hạn phải lớn hơn 0"
            except (ValueError, TypeError):
                return False, None, "Kỳ hạn không hợp lệ"
            
            # Validate purpose
            if not purpose or not purpose.strip():
                return False, None, "Vui lòng nhập mục đích vay"
            
            # Create application
            return self.credit_repo.create_application(
                customer_id=customer_id,
                product_id=product_id,
                requested_amount=Decimal(requested_amount),
                requested_term=term,
                purpose=purpose.strip(),
                assigned_officer_id=assigned_officer_id
            )
            
        except Exception as e:
            return False, None, f"Lỗi: {str(e)}"
    
    # ================================================
    # UC03.2: THẨM ĐỊNH VÀ CHẤM ĐIỂM
    # ================================================
    def start_assessment(
        self,
        application_id: int,
        officer_id: int
    ) -> Tuple[bool, str]:
        """
        Bắt đầu thẩm định hồ sơ vay
        Chuyển trạng thái: Pending → UnderReview
        
        Returns: (success, message)
        """
        # Kiểm tra hồ sơ tồn tại
        app = self.credit_repo.get_by_id(application_id)
        if not app:
            return False, "Không tìm thấy hồ sơ"
        
        # Kiểm tra trạng thái
        if not app.can_review():
            return False, f"Hồ sơ đang ở trạng thái {app.status}, không thể thẩm định"
        
        # Bắt đầu thẩm định
        try:
            success = self.credit_repo.start_review(application_id, officer_id)
            
            if success:
                return True, "Bắt đầu thẩm định hồ sơ thành công"
            else:
                return False, "Không thể bắt đầu thẩm định"
                
        except Exception as e:
            return False, f"Lỗi thẩm định: {str(e)}"
    
    def complete_assessment(
        self,
        application_id: int,
        cic_score: int,
        risk_level: str,
        recommended_amount: Decimal,
        recommended_rate: Decimal,
        notes: str
    ) -> Tuple[bool, str]:
        """
        Hoàn tất thẩm định
        Ghi nhận kết quả CIC và đề xuất
        
        Returns: (success, message)
        """
        # TODO: Lưu vào bảng CreditAssessment
        # Hiện tại chỉ cập nhật notes trong CreditApplications
        
        return True, "Hoàn tất thẩm định. Hồ sơ đã sẵn sàng để phê duyệt."
    
    # ================================================
    # UC03.3: PHÊ DUYỆT KHOẢN VAY
    # ================================================
    def approve_application(
        self,
        application_id: int,
        approver_id: int,
        notes: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Phê duyệt hồ sơ vay
        Chuyển trạng thái: UnderReview → Approved
        
        Returns: (success, message)
        """
        # Kiểm tra hồ sơ
        app = self.credit_repo.get_by_id(application_id)
        if not app:
            return False, "Không tìm thấy hồ sơ"
        
        # Kiểm tra điều kiện phê duyệt
        if not app.can_approve():
            return False, f"Hồ sơ đang ở trạng thái {app.status}, không thể phê duyệt"
        
        # Phê duyệt
        try:
            success = self.credit_repo.approve(application_id, approver_id, notes)
            
            if success:
                return True, f"Phê duyệt hồ sơ {app.application_number} thành công"
            else:
                return False, "Không thể phê duyệt hồ sơ"
                
        except Exception as e:
            return False, f"Lỗi phê duyệt: {str(e)}"
    
    # ================================================
    # UC03.8: TỪ CHỐI KHOẢN VAY
    # ================================================
    def reject_application(
        self,
        application_id: int,
        approver_id: int,
        rejection_reason: str
    ) -> Tuple[bool, str]:
        """
        Từ chối hồ sơ vay
        
        Returns: (success, message)
        """
        # Validation
        if not rejection_reason or rejection_reason.strip() == '':
            return False, "Lý do từ chối không được để trống"
        
        # Kiểm tra hồ sơ
        app = self.credit_repo.get_by_id(application_id)
        if not app:
            return False, "Không tìm thấy hồ sơ"
        
        # Từ chối
        try:
            success = self.credit_repo.reject(
                application_id, 
                approver_id, 
                rejection_reason.strip()
            )
            
            if success:
                return True, f"Từ chối hồ sơ {app.application_number} thành công"
            else:
                return False, "Không thể từ chối hồ sơ"
                
        except Exception as e:
            return False, f"Lỗi từ chối: {str(e)}"
    
    # ================================================
    # UC03.4: GIẢI NGÂN
    # ================================================
    def disburse_loan(
        self,
        application_id: int,
        disbursed_by: int,
        disbursement_method: str = 'Chuyển khoản'
    ) -> Tuple[bool, str]:
        """
        Giải ngân khoản vay
        Chuyển trạng thái: Approved → Disbursed
        Tạo bản ghi Loan và PaymentSchedule
        
        Returns: (success, message)
        """
        # Kiểm tra hồ sơ
        app = self.credit_repo.get_by_id(application_id)
        if not app:
            return False, "Không tìm thấy hồ sơ"
        
        # Kiểm tra điều kiện giải ngân
        if not app.can_disburse():
            return False, f"Hồ sơ đang ở trạng thái {app.status}, không thể giải ngân"
        
        # Giải ngân
        try:
            success = self.credit_repo.mark_disbursed(application_id)
            
            if success:
                # TODO: Tạo bản ghi Loan và PaymentSchedule
                return True, f"Giải ngân hồ sơ {app.application_number} thành công"
            else:
                return False, "Không thể giải ngân"
                
        except Exception as e:
            return False, f"Lỗi giải ngân: {str(e)}"
    
    # ================================================
    # TRUY VẤN HỒ SƠ
    # ================================================
    def get_application_details(self, application_id: int) -> Optional[CreditApplication]:
        """Lấy chi tiết hồ sơ"""
        return self.credit_repo.get_by_id(application_id)
    
    def get_applications_by_status(self, status: str) -> List[CreditApplication]:
        """Lấy danh sách hồ sơ theo trạng thái"""
        return self.credit_repo.get_by_status(status)
    
    def get_my_applications(self, officer_id: int) -> List[CreditApplication]:
        """Lấy danh sách hồ sơ của nhân viên"""
        return self.credit_repo.get_by_officer(officer_id)
    
    def get_all_applications(self) -> List[CreditApplication]:
        """Lấy tất cả hồ sơ"""
        return self.credit_repo.get_all()
    
    # ================================================
    # THỐNG KÊ
    # ================================================
    def get_statistics(self) -> dict:
        """Lấy thống kê hồ sơ"""
        return {
            'total': self.credit_repo.count_by_status(),
            'pending': self.credit_repo.count_by_status('Pending'),
            'under_review': self.credit_repo.count_by_status('UnderReview'),
            'approved': self.credit_repo.count_by_status('Approved'),
            'rejected': self.credit_repo.count_by_status('Rejected'),
            'disbursed': self.credit_repo.count_by_status('Disbursed')
        }
    
    def get_officer_statistics(self, officer_id: int) -> dict:
        """Lấy thống kê của một nhân viên"""
        applications = self.get_my_applications(officer_id)
        
        stats = {
            'total': len(applications),
            'pending': 0,
            'under_review': 0,
            'approved': 0,
            'rejected': 0,
            'disbursed': 0
        }
        
        for app in applications:
            if app.status == 'Pending':
                stats['pending'] += 1
            elif app.status == 'UnderReview':
                stats['under_review'] += 1
            elif app.status == 'Approved':
                stats['approved'] += 1
            elif app.status == 'Rejected':
                stats['rejected'] += 1
            elif app.status == 'Disbursed':
                stats['disbursed'] += 1
        
        return stats
