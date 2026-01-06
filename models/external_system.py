"""
File: models/external_system.py
External System Model - Hệ thống bên ngoài
"""

from datetime import datetime
from typing import Optional


class ExternalSystem:
    """
    Model hệ thống bên ngoài
    Phục vụ chức năng: Manager - Quản lý hệ thống ngoài
    
    Types: Payment, CreditCheck, ExchangeRate, Other
    Status: Active, Inactive, Maintenance
    """
    
    def __init__(
        self,
        system_id: int,
        system_name: str,
        system_type: str,
        api_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        status: str = 'Active',
        description: Optional[str] = None,
        last_checked: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.system_id = system_id
        self.system_name = system_name
        self.system_type = system_type
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.status = status
        self.description = description
        self.last_checked = last_checked
        self.created_at = created_at
        self.updated_at = updated_at
    
    def is_active(self) -> bool:
        """Kiểm tra hệ thống có đang hoạt động không"""
        return self.status == 'Active'
    
    def is_maintenance(self) -> bool:
        """Kiểm tra hệ thống có đang bảo trì không"""
        return self.status == 'Maintenance'
    
    def get_type_display(self) -> str:
        """Lấy tên hiển thị loại hệ thống"""
        type_map = {
            'Payment': 'Thanh toán',
            'CreditCheck': 'Tra cứu tín dụng',
            'ExchangeRate': 'Tỷ giá',
            'Other': 'Khác'
        }
        return type_map.get(self.system_type, self.system_type)
    
    def get_status_display(self) -> str:
        """Lấy tên hiển thị trạng thái"""
        status_map = {
            'Active': 'Hoạt động',
            'Inactive': 'Ngừng hoạt động',
            'Maintenance': 'Bảo trì'
        }
        return status_map.get(self.status, self.status)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'system_id': self.system_id,
            'system_name': self.system_name,
            'system_type': self.system_type,
            'api_endpoint': self.api_endpoint,
            'api_key': self.api_key,
            'status': self.status,
            'description': self.description,
            'last_checked': self.last_checked.isoformat() if self.last_checked else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self) -> str:
        return f"ExternalSystem(id={self.system_id}, name='{self.system_name}', type='{self.system_type}', status='{self.status}')"
    
    def __str__(self) -> str:
        return f"{self.system_name} ({self.get_type_display()}) - {self.get_status_display()}"
