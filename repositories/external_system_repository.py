"""
File: repositories/external_system_repository.py
External System Repository - Truy vấn hệ thống bên ngoài
Phục vụ nghiệp vụ: Manager - Quản lý hệ thống ngoài
"""

from typing import List, Optional
from datetime import datetime
import pyodbc
from models.external_system import ExternalSystem


class ExternalSystemRepository:
    """Repository cho quản lý hệ thống bên ngoài"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
    
    def _get_connection(self):
        """Tạo kết nối database"""
        return pyodbc.connect(self.connection_string)
    
    def _row_to_system(self, row) -> ExternalSystem:
        """Convert database row to ExternalSystem object"""
        return ExternalSystem(
            system_id=row[0],
            system_name=row[1],
            system_type=row[2],
            api_endpoint=row[3],
            api_key=row[4],
            status=row[5],
            description=row[6],
            last_checked=row[7],
            created_at=row[8],
            updated_at=row[9]
        )
    
    def get_all(self) -> List[ExternalSystem]:
        """Lấy tất cả hệ thống"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT MaHeThong, TenHeThong, LoaiHeThong, DiaChiAPI, KhoaAPI,
                   TrangThai, MoTa, KiemTraCuoi, NgayTao, NgayCapNhat
            FROM HeThongNgoai
            ORDER BY TenHeThong
        """
        
        cursor.execute(query)
        systems = [self._row_to_system(row) for row in cursor.fetchall()]
        
        conn.close()
        return systems
    
    def get_by_id(self, system_id: int) -> Optional[ExternalSystem]:
        """Lấy hệ thống theo ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT MaHeThong, TenHeThong, LoaiHeThong, DiaChiAPI, KhoaAPI,
                   TrangThai, MoTa, KiemTraCuoi, NgayTao, NgayCapNhat
            FROM HeThongNgoai
            WHERE MaHeThong = ?
        """
        
        cursor.execute(query, (system_id,))
        row = cursor.fetchone()
        
        system = self._row_to_system(row) if row else None
        conn.close()
        return system
    
    def get_by_type(self, system_type: str) -> List[ExternalSystem]:
        """Lấy hệ thống theo loại"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT MaHeThong, TenHeThong, LoaiHeThong, DiaChiAPI, KhoaAPI,
                   TrangThai, MoTa, KiemTraCuoi, NgayTao, NgayCapNhat
            FROM HeThongNgoai
            WHERE LoaiHeThong = ?
            ORDER BY TenHeThong
        """
        
        cursor.execute(query, (system_type,))
        systems = [self._row_to_system(row) for row in cursor.fetchall()]
        
        conn.close()
        return systems
    
    def get_active_systems(self) -> List[ExternalSystem]:
        """Lấy các hệ thống đang hoạt động"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT MaHeThong, TenHeThong, LoaiHeThong, DiaChiAPI, KhoaAPI,
                   TrangThai, MoTa, KiemTraCuoi, NgayTao, NgayCapNhat
            FROM HeThongNgoai
            WHERE TrangThai = N'KichHoat'
            ORDER BY TenHeThong
        """
        
        cursor.execute(query)
        systems = [self._row_to_system(row) for row in cursor.fetchall()]
        
        conn.close()
        return systems
    
    def create(
        self,
        system_name: str,
        system_type: str,
        api_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        description: Optional[str] = None
    ) -> Optional[int]:
        """Tạo hệ thống mới"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO HeThongNgoai (
                TenHeThong, LoaiHeThong, DiaChiAPI, KhoaAPI, MoTa, TrangThai
            )
            VALUES (?, ?, ?, ?, ?, N'KichHoat')
        """
        
        try:
            cursor.execute(query, (system_name, system_type, api_endpoint, api_key, description))
            conn.commit()
            
            cursor.execute("SELECT @@IDENTITY")
            system_id = int(cursor.fetchone()[0])
            
            conn.close()
            return system_id
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    def update(
        self,
        system_id: int,
        system_name: Optional[str] = None,
        system_type: Optional[str] = None,
        api_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        status: Optional[str] = None,
        description: Optional[str] = None
    ) -> bool:
        """Cập nhật hệ thống"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if system_name is not None:
            updates.append("TenHeThong = ?")
            params.append(system_name)
        if system_type is not None:
            updates.append("LoaiHeThong = ?")
            params.append(system_type)
        if api_endpoint is not None:
            updates.append("DiaChiAPI = ?")
            params.append(api_endpoint)
        if api_key is not None:
            updates.append("KhoaAPI = ?")
            params.append(api_key)
        if status is not None:
            updates.append("TrangThai = ?")
            params.append(status)
        if description is not None:
            updates.append("MoTa = ?")
            params.append(description)
        
        if not updates:
            return False
        
        updates.append("NgayCapNhat = GETDATE()")
        params.append(system_id)
        
        query = f"UPDATE HeThongNgoai SET {', '.join(updates)} WHERE MaHeThong = ?"
        
        try:
            cursor.execute(query, params)
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    def update_last_checked(self, system_id: int) -> bool:
        """Cập nhật thời gian kiểm tra cuối"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "UPDATE HeThongNgoai SET KiemTraCuoi = GETDATE() WHERE MaHeThong = ?"
        
        try:
            cursor.execute(query, (system_id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    def delete(self, system_id: int) -> bool:
        """Xóa hệ thống"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM HeThongNgoai WHERE MaHeThong = ?"
        
        try:
            cursor.execute(query, (system_id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    def count_by_type(self, system_type: Optional[str] = None) -> int:
        """Đếm số hệ thống theo loại"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if system_type:
            query = "SELECT COUNT(*) FROM HeThongNgoai WHERE LoaiHeThong = ?"
            cursor.execute(query, (system_type,))
        else:
            query = "SELECT COUNT(*) FROM HeThongNgoai"
            cursor.execute(query)
        
        count = cursor.fetchone()[0]
        conn.close()
        return count