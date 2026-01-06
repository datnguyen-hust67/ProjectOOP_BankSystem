"""
File: repositories/credit_application_repository.py
Credit Application Repository - Truy vấn hồ sơ vay
Phục vụ nghiệp vụ: Nhân viên tín dụng
"""

from typing import List, Optional, Tuple
from datetime import datetime
from decimal import Decimal
import pyodbc
from models.credit_application import CreditApplication


class CreditApplicationRepository:
    """Repository cho quản lý hồ sơ vay"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
    
    def _get_connection(self):
        """Tạo kết nối database"""
        return pyodbc.connect(self.connection_string)
    
    def _row_to_application(self, row) -> CreditApplication:
        """Convert database row to CreditApplication object"""
        return CreditApplication(
            application_id=row[0],
            application_number=row[1],
            customer_id=row[2],
            product_id=row[3],
            requested_amount=Decimal(str(row[4])),
            requested_term=row[5],
            purpose=row[6],
            status=row[7],
            assigned_officer_id=row[8],
            reviewed_by=row[9],
            approved_by=row[10],
            application_date=row[11],
            review_date=row[12],
            approval_date=row[13],
            disbursement_date=row[14],
            notes=row[15],
            rejection_reason=row[16],
            created_at=row[17],
            updated_at=row[18],
            customer_name=row[19] if len(row) > 19 else None,
            customer_phone=row[20] if len(row) > 20 else None,
            customer_credit_score=row[21] if len(row) > 21 else None,
            product_name=row[22] if len(row) > 22 else None,
            officer_name=row[23] if len(row) > 23 else None
        )
    
    # ================================================
    # UC03.1: TẠO HỒ SƠ VAY MỚI
    # ================================================
    def create(
        self,
        customer_id: int,
        product_id: int,
        requested_amount: Decimal,
        requested_term: int,
        purpose: str,
        assigned_officer_id: int
    ) -> Tuple[bool, Optional[int], str]:
        """
        Tạo hồ sơ vay mới
        Hỗ trợ: UC03.1 - Tạo hồ sơ vay
        
        Returns:
            (success, application_id, message)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Generate application number
            cursor.execute("SELECT COUNT(*) FROM CreditApplications")
            count = cursor.fetchone()[0]
            app_number = f"APP-{datetime.now().year}-{count + 1:06d}"
            
            query = """
                INSERT INTO CreditApplications (
                    ApplicationNumber, CustomerID, ProductID, RequestedAmount,
                    RequestedTerm, Purpose, Status, AssignedOfficerID, ApplicationDate
                )
                VALUES (?, ?, ?, ?, ?, ?, 'Pending', ?, GETDATE())
            """
            
            cursor.execute(query, (
                app_number, customer_id, product_id, float(requested_amount),
                requested_term, purpose, assigned_officer_id
            ))
            conn.commit()
            
            cursor.execute("SELECT @@IDENTITY")
            app_id = int(cursor.fetchone()[0])
            
            conn.close()
            return True, app_id, f"Tạo hồ sơ {app_number} thành công"
            
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, None, f"Lỗi tạo hồ sơ: {str(e)}"
    
    # ================================================
    # UC03.2: THẨM ĐỊNH VÀ CHẤM ĐIỂM
    # ================================================
    def start_review(self, application_id: int, officer_id: int) -> bool:
        """
        Bắt đầu thẩm định hồ sơ
        Hỗ trợ: UC03.2 - Thẩm định và chấm điểm
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE CreditApplications
            SET Status = 'UnderReview', 
                ReviewedBy = ?,
                ReviewDate = GETDATE(),
                UpdatedAt = GETDATE()
            WHERE ApplicationID = ? AND Status = 'Pending'
        """
        
        try:
            cursor.execute(query, (officer_id, application_id))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    # ================================================
    # UC03.3: PHÊ DUYỆT KHOẢN VAY
    # ================================================
    def approve(self, application_id: int, approver_id: int, notes: Optional[str] = None) -> bool:
        """
        Phê duyệt hồ sơ vay
        Hỗ trợ: UC03.3 - Phê duyệt khoản vay
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE CreditApplications
            SET Status = 'Approved',
                ApprovedBy = ?,
                ApprovalDate = GETDATE(),
                Notes = ?,
                UpdatedAt = GETDATE()
            WHERE ApplicationID = ? AND Status = 'UnderReview'
        """
        
        try:
            cursor.execute(query, (approver_id, notes, application_id))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    # ================================================
    # UC03.8: TỪ CHỐI KHOẢN VAY
    # ================================================
    def reject(self, application_id: int, approver_id: int, rejection_reason: str) -> bool:
        """
        Từ chối hồ sơ vay
        Hỗ trợ: UC03.8 - Từ chối khoản vay (extend từ UC03.3)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE CreditApplications
            SET Status = 'Rejected',
                ApprovedBy = ?,
                ApprovalDate = GETDATE(),
                RejectionReason = ?,
                UpdatedAt = GETDATE()
            WHERE ApplicationID = ?
        """
        
        try:
            cursor.execute(query, (approver_id, rejection_reason, application_id))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    # ================================================
    # UC03.4: GIẢI NGÂN
    # ================================================
    def mark_disbursed(self, application_id: int) -> bool:
        """
        Đánh dấu hồ sơ đã giải ngân
        Hỗ trợ: UC03.4 - Giải ngân
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE CreditApplications
            SET Status = 'Disbursed',
                DisbursementDate = GETDATE(),
                UpdatedAt = GETDATE()
            WHERE ApplicationID = ? AND Status = 'Approved'
        """
        
        try:
            cursor.execute(query, (application_id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    # ================================================
    # TRUY VẤN HỒ SƠ
    # ================================================
    def get_by_id(self, application_id: int) -> Optional[CreditApplication]:
        """Lấy hồ sơ theo ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT CA.ApplicationID, CA.ApplicationNumber, CA.CustomerID, CA.ProductID,
                   CA.RequestedAmount, CA.RequestedTerm, CA.Purpose, CA.Status,
                   CA.AssignedOfficerID, CA.ReviewedBy, CA.ApprovedBy,
                   CA.ApplicationDate, CA.ReviewDate, CA.ApprovalDate, CA.DisbursementDate,
                   CA.Notes, CA.RejectionReason, CA.CreatedAt, CA.UpdatedAt,
                   C.FullName, C.Phone, C.CreditScore,
                   LP.ProductName,
                   E.FullName
            FROM CreditApplications CA
            INNER JOIN Customers C ON CA.CustomerID = C.CustomerID
            INNER JOIN LoanProducts LP ON CA.ProductID = LP.ProductID
            LEFT JOIN Employees E ON CA.AssignedOfficerID = E.EmployeeID
            WHERE CA.ApplicationID = ?
        """
        
        cursor.execute(query, (application_id,))
        row = cursor.fetchone()
        
        app = self._row_to_application(row) if row else None
        conn.close()
        return app
    
    def get_by_status(self, status: str) -> List[CreditApplication]:
        """Lấy danh sách hồ sơ theo trạng thái"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT CA.ApplicationID, CA.ApplicationNumber, CA.CustomerID, CA.ProductID,
                   CA.RequestedAmount, CA.RequestedTerm, CA.Purpose, CA.Status,
                   CA.AssignedOfficerID, CA.ReviewedBy, CA.ApprovedBy,
                   CA.ApplicationDate, CA.ReviewDate, CA.ApprovalDate, CA.DisbursementDate,
                   CA.Notes, CA.RejectionReason, CA.CreatedAt, CA.UpdatedAt,
                   C.FullName, C.Phone, C.CreditScore,
                   LP.ProductName,
                   E.FullName
            FROM CreditApplications CA
            INNER JOIN Customers C ON CA.CustomerID = C.CustomerID
            INNER JOIN LoanProducts LP ON CA.ProductID = LP.ProductID
            LEFT JOIN Employees E ON CA.AssignedOfficerID = E.EmployeeID
            WHERE CA.Status = ?
            ORDER BY CA.ApplicationDate DESC
        """
        
        cursor.execute(query, (status,))
        applications = [self._row_to_application(row) for row in cursor.fetchall()]
        
        conn.close()
        return applications
    
    def get_by_officer(self, officer_id: int) -> List[CreditApplication]:
        """Lấy danh sách hồ sơ của một nhân viên"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT CA.ApplicationID, CA.ApplicationNumber, CA.CustomerID, CA.ProductID,
                   CA.RequestedAmount, CA.RequestedTerm, CA.Purpose, CA.Status,
                   CA.AssignedOfficerID, CA.ReviewedBy, CA.ApprovedBy,
                   CA.ApplicationDate, CA.ReviewDate, CA.ApprovalDate, CA.DisbursementDate,
                   CA.Notes, CA.RejectionReason, CA.CreatedAt, CA.UpdatedAt,
                   C.FullName, C.Phone, C.CreditScore,
                   LP.ProductName,
                   E.FullName
            FROM CreditApplications CA
            INNER JOIN Customers C ON CA.CustomerID = C.CustomerID
            INNER JOIN LoanProducts LP ON CA.ProductID = LP.ProductID
            LEFT JOIN Employees E ON CA.AssignedOfficerID = E.EmployeeID
            WHERE CA.AssignedOfficerID = ?
            ORDER BY CA.ApplicationDate DESC
        """
        
        cursor.execute(query, (officer_id,))
        applications = [self._row_to_application(row) for row in cursor.fetchall()]
        
        conn.close()
        return applications
    
    def get_all(self) -> List[CreditApplication]:
        """Lấy tất cả hồ sơ"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT CA.ApplicationID, CA.ApplicationNumber, CA.CustomerID, CA.ProductID,
                   CA.RequestedAmount, CA.RequestedTerm, CA.Purpose, CA.Status,
                   CA.AssignedOfficerID, CA.ReviewedBy, CA.ApprovedBy,
                   CA.ApplicationDate, CA.ReviewDate, CA.ApprovalDate, CA.DisbursementDate,
                   CA.Notes, CA.RejectionReason, CA.CreatedAt, CA.UpdatedAt,
                   C.FullName, C.Phone, C.CreditScore,
                   LP.ProductName,
                   E.FullName
            FROM CreditApplications CA
            INNER JOIN Customers C ON CA.CustomerID = C.CustomerID
            INNER JOIN LoanProducts LP ON CA.ProductID = LP.ProductID
            LEFT JOIN Employees E ON CA.AssignedOfficerID = E.EmployeeID
            ORDER BY CA.ApplicationDate DESC
        """
        
        cursor.execute(query)
        applications = [self._row_to_application(row) for row in cursor.fetchall()]
        
        conn.close()
        return applications
    
    def count_by_status(self, status: Optional[str] = None) -> int:
        """Đếm số hồ sơ theo trạng thái"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if status:
            query = "SELECT COUNT(*) FROM CreditApplications WHERE Status = ?"
            cursor.execute(query, (status,))
        else:
            query = "SELECT COUNT(*) FROM CreditApplications"
            cursor.execute(query)
        
        count = cursor.fetchone()[0]
        conn.close()
        return count
