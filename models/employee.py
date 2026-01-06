"""
File: models/employee.py
Employee Model - Quản lý thông tin nhân viên
"""

from datetime import datetime, date
from typing import Optional


class Employee:
    """
    Model nhân viên
    Phục vụ chức năng: Quản lý người dùng (Manager)
    """
    
    def __init__(
        self,
        employee_id: int,
        user_id: int,
        full_name: str,
        date_of_birth: Optional[date] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        department: Optional[str] = None,  # Phòng ban
        position: Optional[str] = None,    # Chức vụ
        salary: Optional[float] = None,    # Mức lương
        hire_date: Optional[date] = None,
        manager_id: Optional[int] = None,
        status: str = 'Active',
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        address: Optional[str] = None,
        identity_number: Optional[str] = None,
        hometown: Optional[str] = None,
        username: Optional[str] = None,  # From Users table
        role_name: Optional[str] = None   # From Roles table
    ):
        self.employee_id = employee_id
        self.user_id = user_id
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.email = email
        self.department = department
        self.position = position
        self.salary = salary
        self.hire_date = hire_date
        self.manager_id = manager_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.address = address
        self.identity_number = identity_number
        self.hometown = hometown
        self.username = username
        self.role_name = role_name
    
    def is_active(self) -> bool:
        """Kiểm tra nhân viên có đang hoạt động không"""
        return self.status == 'Active' and self.deleted_at is None
    
    def is_locked(self) -> bool:
        """Kiểm tra tài khoản có bị khóa không"""
        return self.status == 'Locked'
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'employee_id': self.employee_id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'phone': self.phone,
            'email': self.email,
            'department': self.department,
            'position': self.position,
            'salary': float(self.salary) if self.salary else None,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'manager_id': self.manager_id,
            'status': self.status,
            'address': self.address,
            'identity_number': self.identity_number,
            'hometown': self.hometown,
            'username': self.username,
            'role_name': self.role_name
        }
    
    def __repr__(self) -> str:
        return f"Employee(id={self.employee_id}, name='{self.full_name}', position='{self.position}')"
