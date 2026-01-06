"""
File: controllers/external_system_controller.py
External System Controller - Điều khiển hệ thống ngoài
"""

from typing import Optional, Tuple
from services.external_system_service import ExternalSystemService


class ExternalSystemController:
    """
    Controller cho Manager - Quản lý hệ thống ngoài
    Xử lý tương tác giữa View và Service
    """
    
    def __init__(self, system_service: ExternalSystemService):
        self.system_service = system_service
        self.current_user = None
    
    def set_current_user(self, user):
        """Set user hiện tại"""
        self.current_user = user
    
    def get_all_systems(self):
        """Lấy tất cả hệ thống"""
        return self.system_service.get_all_systems()
    
    def get_active_systems(self):
        """Lấy hệ thống đang hoạt động"""
        return self.system_service.get_active_systems()
    
    def get_system_details(self, system_id: int):
        """Lấy chi tiết hệ thống"""
        return self.system_service.get_system_details(system_id)
    
    def add_system(
        self,
        system_name: str,
        system_type: str,
        api_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        description: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Thêm hệ thống mới"""
        success, system_id, message = self.system_service.add_system(
            system_name,
            system_type,
            api_endpoint,
            api_key,
            description
        )
        return success, message
    
    def update_system(
        self,
        system_id: int,
        **kwargs
    ) -> Tuple[bool, str]:
        """Cập nhật hệ thống"""
        return self.system_service.update_system(system_id, **kwargs)
    
    def delete_system(self, system_id: int) -> Tuple[bool, str]:
        """Xóa hệ thống"""
        return self.system_service.delete_system(system_id)
    
    def check_connection(self, system_id: int) -> Tuple[bool, str]:
        """Kiểm tra kết nối"""
        return self.system_service.check_system_connection(system_id)
    
    def get_statistics(self):
        """Lấy thống kê"""
        return self.system_service.get_statistics()
