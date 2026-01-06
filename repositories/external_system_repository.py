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
            SELECT SystemID, SystemName, SystemType, APIEndpoint, APIKey,
                   Status, Description, LastChecked, CreatedAt, UpdatedAt
            FROM ExternalSystems
            ORDER BY SystemName
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
            SELECT SystemID, SystemName, SystemType, APIEndpoint, APIKey,
                   Status, Description, LastChecked, CreatedAt, UpdatedAt
            FROM ExternalSystems
            WHERE SystemID = ?
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
            SELECT SystemID, SystemName, SystemType, APIEndpoint, APIKey,
                   Status, Description, LastChecked, CreatedAt, UpdatedAt
            FROM ExternalSystems
            WHERE SystemType = ?
            ORDER BY SystemName
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
            SELECT SystemID, SystemName, SystemType, APIEndpoint, APIKey,
                   Status, Description, LastChecked, CreatedAt, UpdatedAt
            FROM ExternalSystems
            WHERE Status = 'Active'
            ORDER BY SystemName
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
            INSERT INTO ExternalSystems (
                SystemName, SystemType, APIEndpoint, APIKey, Description, Status
            )
            VALUES (?, ?, ?, ?, ?, 'Active')
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
            updates.append("SystemName = ?")
            params.append(system_name)
        if system_type is not None:
            updates.append("SystemType = ?")
            params.append(system_type)
        if api_endpoint is not None:
            updates.append("APIEndpoint = ?")
            params.append(api_endpoint)
        if api_key is not None:
            updates.append("APIKey = ?")
            params.append(api_key)
        if status is not None:
            updates.append("Status = ?")
            params.append(status)
        if description is not None:
            updates.append("Description = ?")
            params.append(description)
        
        if not updates:
            return False
        
        updates.append("UpdatedAt = GETDATE()")
        params.append(system_id)
        
        query = f"UPDATE ExternalSystems SET {', '.join(updates)} WHERE SystemID = ?"
        
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
        
        query = "UPDATE ExternalSystems SET LastChecked = GETDATE() WHERE SystemID = ?"
        
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
        
        query = "DELETE FROM ExternalSystems WHERE SystemID = ?"
        
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
            query = "SELECT COUNT(*) FROM ExternalSystems WHERE SystemType = ?"
            cursor.execute(query, (system_type,))
        else:
            query = "SELECT COUNT(*) FROM ExternalSystems"
            cursor.execute(query)
        
        count = cursor.fetchone()[0]
        conn.close()
        return count
