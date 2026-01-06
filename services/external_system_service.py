"""
File: services/external_system_service.py
External System Service - Business logic hệ thống ngoài
"""

from typing import List, Optional, Tuple
from repositories.external_system_repository import ExternalSystemRepository
from models.external_system import ExternalSystem


class ExternalSystemService:
    """
    Service xử lý nghiệp vụ hệ thống ngoài
    Phục vụ: Manager - Quản lý hệ thống ngoài
    """
    
    def __init__(self, system_repo: ExternalSystemRepository):
        self.system_repo = system_repo
    
    def get_all_systems(self) -> List[ExternalSystem]:
        """Lấy tất cả hệ thống"""
        return self.system_repo.get_all()
    
    def get_active_systems(self) -> List[ExternalSystem]:
        """Lấy các hệ thống đang hoạt động"""
        return self.system_repo.get_active_systems()
    
    def get_system_details(self, system_id: int) -> Optional[ExternalSystem]:
        """Lấy chi tiết hệ thống"""
        return self.system_repo.get_by_id(system_id)
    
    def add_system(
        self,
        system_name: str,
        system_type: str,
        api_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        description: Optional[str] = None
    ) -> Tuple[bool, Optional[int], str]:
        """
        Thêm hệ thống mới
        
        Returns: (success, system_id, message)
        """
        # Validation
        if not system_name or system_name.strip() == '':
            return False, None, "Tên hệ thống không được để trống"
        
        if system_type not in ['Payment', 'CreditCheck', 'ExchangeRate', 'Other']:
            return False, None, "Loại hệ thống không hợp lệ"
        
        try:
            system_id = self.system_repo.create(
                system_name=system_name.strip(),
                system_type=system_type,
                api_endpoint=api_endpoint,
                api_key=api_key,
                description=description
            )
            
            if system_id:
                return True, system_id, f"Thêm hệ thống {system_name} thành công"
            else:
                return False, None, "Lỗi khi thêm hệ thống"
                
        except Exception as e:
            return False, None, f"Lỗi: {str(e)}"
    
    def update_system(
        self,
        system_id: int,
        system_name: Optional[str] = None,
        system_type: Optional[str] = None,
        api_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        status: Optional[str] = None,
        description: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Cập nhật hệ thống
        
        Returns: (success, message)
        """
        # Validation
        if system_type and system_type not in ['Payment', 'CreditCheck', 'ExchangeRate', 'Other']:
            return False, "Loại hệ thống không hợp lệ"
        
        if status and status not in ['Active', 'Inactive', 'Maintenance']:
            return False, "Trạng thái không hợp lệ"
        
        try:
            success = self.system_repo.update(
                system_id=system_id,
                system_name=system_name,
                system_type=system_type,
                api_endpoint=api_endpoint,
                api_key=api_key,
                status=status,
                description=description
            )
            
            if success:
                return True, "Cập nhật hệ thống thành công"
            else:
                return False, "Không tìm thấy hệ thống hoặc không có thay đổi"
                
        except Exception as e:
            return False, f"Lỗi cập nhật: {str(e)}"
    
    def delete_system(self, system_id: int) -> Tuple[bool, str]:
        """
        Xóa hệ thống
        
        Returns: (success, message)
        """
        try:
            success = self.system_repo.delete(system_id)
            
            if success:
                return True, "Xóa hệ thống thành công"
            else:
                return False, "Không thể xóa hệ thống"
                
        except Exception as e:
            return False, f"Lỗi xóa: {str(e)}"
    
    def check_system_connection(self, system_id: int) -> Tuple[bool, str]:
        """
        Kiểm tra kết nối hệ thống
        (Giả lập - thực tế cần gọi API)
        
        Returns: (success, message)
        """
        system = self.system_repo.get_by_id(system_id)
        if not system:
            return False, "Không tìm thấy hệ thống"
        
        # TODO: Thực hiện kiểm tra kết nối thật
        # Hiện tại chỉ cập nhật LastChecked
        
        try:
            self.system_repo.update_last_checked(system_id)
            return True, f"Hệ thống {system.system_name} hoạt động bình thường"
        except Exception as e:
            return False, f"Lỗi kết nối: {str(e)}"
    
    def get_statistics(self) -> dict:
        """Lấy thống kê hệ thống"""
        all_systems = self.get_all_systems()
        
        stats = {
            'total': len(all_systems),
            'active': 0,
            'inactive': 0,
            'maintenance': 0,
            'by_type': {
                'Payment': 0,
                'CreditCheck': 0,
                'ExchangeRate': 0,
                'Other': 0
            }
        }
        
        for system in all_systems:
            if system.status == 'Active':
                stats['active'] += 1
            elif system.status == 'Inactive':
                stats['inactive'] += 1
            elif system.status == 'Maintenance':
                stats['maintenance'] += 1
            
            stats['by_type'][system.system_type] += 1
        
        return stats
