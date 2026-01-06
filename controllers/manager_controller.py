"""
File: controllers/manager_controller.py
Manager Controller - Điều khiển quản lý người dùng
"""

from typing import Optional, Tuple
from datetime import date
from services.employee_service import EmployeeService


class ManagerController:
    """
    Controller cho Manager - Quản lý người dùng
    Xử lý tương tác giữa View và Service
    """
    
    def __init__(self, employee_service: EmployeeService):
        self.employee_service = employee_service
        self.current_user = None
    
    def set_current_user(self, user):
        """Set user hiện tại"""
        self.current_user = user
    
    # UC05.1: Hiển thị danh sách
    def get_employee_list(self, page: int = 1):
        """Lấy danh sách nhân viên có phân trang"""
        return self.employee_service.get_employees_paginated(page, 20)
    
    def get_all_employees(self):
        """Lấy tất cả nhân viên"""
        return self.employee_service.get_all_employees()
    
    # UC05.2: Thêm nhân viên
    def add_employee(
        self,
        user_id: int,
        full_name: str,
        email: str,
        phone: str,
        department: str,
        position: str,
        salary: str,  # String from UI
        date_of_birth: Optional[date] = None,
        address: Optional[str] = None,
        identity_number: Optional[str] = None,
        hometown: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Thêm nhân viên mới"""
        try:
            # Convert salary to float
            salary_float = float(salary.replace(',', ''))
            
            success, emp_id, message = self.employee_service.add_employee(
                user_id=user_id,
                full_name=full_name,
                email=email,
                phone=phone,
                department=department,
                position=position,
                salary=salary_float,
                date_of_birth=date_of_birth,
                address=address,
                identity_number=identity_number,
                hometown=hometown
            )
            
            return success, message
            
        except ValueError:
            return False, "Mức lương không hợp lệ"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"
    
    # UC05.3: Tìm kiếm
    def search_employees(self, keyword: str):
        """Tìm kiếm nhân viên"""
        success, employees, message = self.employee_service.search_employees(keyword)
        return employees if success else []
    
    # UC05.4: Xem chi tiết
    def get_employee_details(self, employee_id: int):
        """Lấy thông tin chi tiết nhân viên"""
        return self.employee_service.get_employee_details(employee_id)
    
    # UC05.5: Chỉnh sửa
    def update_employee(
        self,
        employee_id: int,
        **kwargs
    ) -> Tuple[bool, str]:
        """Cập nhật thông tin nhân viên"""
        # Convert salary if provided
        if 'salary' in kwargs and kwargs['salary']:
            try:
                kwargs['salary'] = float(str(kwargs['salary']).replace(',', ''))
            except:
                return False, "Mức lương không hợp lệ"
        
        return self.employee_service.update_employee(employee_id, **kwargs)
    
    # UC05.6: Phân quyền
    def change_role(self, user_id: int, new_role_id: int) -> Tuple[bool, str]:
        """Thay đổi quyền nhân viên"""
        return self.employee_service.change_employee_role(user_id, new_role_id)
    
    # UC05.7: Khóa/Mở tài khoản
    def lock_account(self, employee_id: int) -> Tuple[bool, str]:
        """Khóa tài khoản"""
        return self.employee_service.lock_employee_account(employee_id)
    
    def unlock_account(self, employee_id: int) -> Tuple[bool, str]:
        """Mở khóa tài khoản"""
        return self.employee_service.unlock_employee_account(employee_id)
    
    def delete_employee(self, employee_id: int) -> Tuple[bool, str]:
        """Xóa nhân viên"""
        return self.employee_service.delete_employee(employee_id)
    
    # Thống kê
    def get_statistics(self):
        """Lấy thống kê"""
        return self.employee_service.get_statistics()
