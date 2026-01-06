"""
File: services/employee_service.py
Employee Service - Business logic quản lý nhân viên
"""

from typing import List, Optional, Tuple
from datetime import date
from repositories.employee_repository import EmployeeRepository
from models.employee import Employee


class EmployeeService:
    """
    Service xử lý nghiệp vụ quản lý nhân viên
    Phục vụ: Manager - Quản lý người dùng
    """
    
    def __init__(self, employee_repo: EmployeeRepository):
        self.employee_repo = employee_repo
    
    # ================================================
    # UC05.1: HIỂN THỊ DANH SÁCH NHÂN VIÊN
    # ================================================
    def get_all_employees(self, include_deleted: bool = False) -> List[Employee]:
        """Lấy danh sách tất cả nhân viên"""
        return self.employee_repo.get_all(include_deleted)
    
    def get_employees_paginated(self, page: int = 1, page_size: int = 20) -> Tuple[List[Employee], int, int]:
        """
        Lấy danh sách phân trang
        Returns: (employees, total_count, total_pages)
        """
        employees, total = self.employee_repo.get_paginated(page, page_size)
        total_pages = (total + page_size - 1) // page_size
        return employees, total, total_pages
    
    # ================================================
    # UC05.2: THÊM NHÂN VIÊN MỚI (CÓ PHÂN CHỨC VỤ + LƯƠNG)
    # ================================================
    def add_employee(
        self,
        user_id: int,
        full_name: str,
        email: str,
        phone: str,
        department: str,
        position: str,      
        salary: float,      
        date_of_birth: Optional[date] = None,
        address: Optional[str] = None,
        identity_number: Optional[str] = None,
        hometown: Optional[str] = None,
        manager_id: Optional[int] = None
    ) -> Tuple[bool, Optional[int], str]:
        """
        Thêm nhân viên mới
        Validates: Email, Phone, Salary > 0, Position not empty
        
        Returns: (success, employee_id, message)
        """
        # Validation
        if not email or '@' not in email:
            return False, None, "Email không hợp lệ"
        
        if not phone or len(phone) < 10:
            return False, None, "Số điện thoại không hợp lệ"
        
        if not position or position.strip() == '':
            return False, None, "Chức vụ không được để trống"
        
        if salary <= 0:
            return False, None, "Mức lương phải lớn hơn 0"
        
        if not department or department.strip() == '':
            return False, None, "Phòng ban không được để trống"
        
        # Create employee
        try:
            employee_id = self.employee_repo.create(
                user_id=user_id,
                full_name=full_name,
                email=email,
                phone=phone,
                department=department,
                position=position,
                salary=salary,
                date_of_birth=date_of_birth,
                address=address,
                identity_number=identity_number,
                hometown=hometown,
                manager_id=manager_id
            )
            
            if employee_id:
                return True, employee_id, f"Thêm nhân viên {full_name} thành công"
            else:
                return False, None, "Lỗi khi thêm nhân viên"
                
        except Exception as e:
            return False, None, f"Lỗi: {str(e)}"
    
    # ================================================
    # UC05.3: TÌM KIẾM NHÂN VIÊN
    # ================================================
    def search_employees(self, keyword: str) -> Tuple[bool, List[Employee], str]:
        """
        Tìm kiếm nhân viên theo từ khóa
        
        Returns: (success, employees, message)
        """
        if not keyword or keyword.strip() == '':
            return False, [], "Vui lòng nhập từ khóa tìm kiếm"
        
        try:
            employees = self.employee_repo.search(keyword.strip())
            
            if employees:
                return True, employees, f"Tìm thấy {len(employees)} nhân viên"
            else:
                return True, [], "Không tìm thấy dữ liệu"
                
        except Exception as e:
            return False, [], f"Lỗi tìm kiếm: {str(e)}"
    
    # ================================================
    # UC05.4: XEM HỒ SƠ NHÂN VIÊN
    # ================================================
    def get_employee_details(self, employee_id: int) -> Optional[Employee]:
        """Lấy thông tin chi tiết nhân viên"""
        return self.employee_repo.get_by_id(employee_id)
    
    # ================================================
    # UC05.5: CHỈNH SỬA THÔNG TIN NHÂN VIÊN
    # ================================================
    def update_employee(
        self,
        employee_id: int,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        department: Optional[str] = None,
        position: Optional[str] = None,
        salary: Optional[float] = None,
        date_of_birth: Optional[date] = None,
        address: Optional[str] = None,
        identity_number: Optional[str] = None,
        hometown: Optional[str] = None,
        manager_id: Optional[int] = None
    ) -> Tuple[bool, str]:
        """
        Cập nhật thông tin nhân viên
        
        Returns: (success, message)
        """
        # Validation
        if email and '@' not in email:
            return False, "Email không hợp lệ"
        
        if phone and len(phone) < 10:
            return False, "Số điện thoại không hợp lệ"
        
        if salary is not None and salary <= 0:
            return False, "Mức lương phải lớn hơn 0"
        
        try:
            success = self.employee_repo.update(
                employee_id=employee_id,
                full_name=full_name,
                email=email,
                phone=phone,
                department=department,
                position=position,
                salary=salary,
                date_of_birth=date_of_birth,
                address=address,
                identity_number=identity_number,
                hometown=hometown,
                manager_id=manager_id
            )
            
            if success:
                return True, "Cập nhật thông tin thành công"
            else:
                return False, "Không tìm thấy nhân viên hoặc không có thay đổi"
                
        except Exception as e:
            return False, f"Lỗi cập nhật: {str(e)}"
    
    # ================================================
    # UC05.6: PHÂN QUYỀN (GÁN ROLE)
    # ================================================
    def change_employee_role(self, user_id: int, new_role_id: int) -> Tuple[bool, str]:
        """
        Thay đổi quyền của nhân viên
        
        Returns: (success, message)
        """
        try:
            success = self.employee_repo.change_role(user_id, new_role_id)
            
            if success:
                return True, "Phân quyền thành công. Nhân viên cần đăng nhập lại để quyền có hiệu lực."
            else:
                return False, "Không thể thay đổi quyền"
                
        except Exception as e:
            return False, f"Lỗi phân quyền: {str(e)}"
    
    # ================================================
    # UC05.7: KHÓA/MỞ TÀI KHOẢN
    # ================================================
    def lock_employee_account(self, employee_id: int) -> Tuple[bool, str]:
        """
        Khóa tài khoản nhân viên
        
        Returns: (success, message)
        """
        try:
            success = self.employee_repo.lock_account(employee_id)
            
            if success:
                return True, "Khóa tài khoản thành công"
            else:
                return False, "Không thể khóa tài khoản"
                
        except Exception as e:
            return False, f"Lỗi khóa tài khoản: {str(e)}"
    
    def unlock_employee_account(self, employee_id: int) -> Tuple[bool, str]:
        """
        Mở khóa tài khoản nhân viên
        
        Returns: (success, message)
        """
        try:
            success = self.employee_repo.unlock_account(employee_id)
            
            if success:
                return True, "Mở khóa tài khoản thành công"
            else:
                return False, "Không thể mở khóa tài khoản"
                
        except Exception as e:
            return False, f"Lỗi mở khóa: {str(e)}"
    
    def delete_employee(self, employee_id: int) -> Tuple[bool, str]:
        """
        Xóa nhân viên (soft delete)
        
        Returns: (success, message)
        """
        try:
            success = self.employee_repo.soft_delete(employee_id)
            
            if success:
                return True, "Xóa nhân viên thành công"
            else:
                return False, "Không thể xóa nhân viên"
                
        except Exception as e:
            return False, f"Lỗi xóa nhân viên: {str(e)}"
    
    # ================================================
    # THỐNG KÊ
    # ================================================
    def get_statistics(self) -> dict:
        """Lấy thống kê nhân viên"""
        return {
            'total': self.employee_repo.count_by_status(),
            'active': self.employee_repo.count_by_status('Active'),
            'locked': self.employee_repo.count_by_status('Locked'),
            'inactive': self.employee_repo.count_by_status('Inactive')
        }
