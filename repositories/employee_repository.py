"""
File: repositories/employee_repository.py
Employee Repository - Truy vấn dữ liệu nhân viên
Phục vụ nghiệp vụ: Quản lý người dùng (Manager)
"""

from typing import List, Optional, Tuple
from datetime import date
import pyodbc
from models.employee import Employee


class EmployeeRepository:
    """Repository cho quản lý nhân viên"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
    
    def _get_connection(self):
        """Tạo kết nối database"""
        return pyodbc.connect(self.connection_string)
    
    def _row_to_employee(self, row) -> Employee:
        """Convert database row to Employee object"""
        return Employee(
            employee_id=row[0],
            user_id=row[1],
            full_name=row[2],
            date_of_birth=row[3],
            phone=row[4],
            email=row[5],
            department=row[6],
            position=row[7],
            salary=float(row[8]) if row[8] else None,
            hire_date=row[9],
            manager_id=row[10],
            status=row[11],
            created_at=row[12],
            updated_at=row[13],
            deleted_at=row[14],
            address=row[15],
            identity_number=row[16],
            hometown=row[17],
            username=row[18] if len(row) > 18 else None,
            role_name=row[19] if len(row) > 19 else None
        )
    
    # ================================================
    # UC05.1: HIỂN THỊ DANH SÁCH NHÂN VIÊN
    # ================================================
    def get_all(self, include_deleted: bool = False) -> List[Employee]:
        """
        Lấy danh sách tất cả nhân viên
        Hỗ trợ: Hiển thị danh sách nhân viên (UC05.1)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT NV.MaNhanVien, NV.MaNguoiDung, NV.HoTen, NV.NgaySinh, NV.SoDienThoai, NV.Email,
                   NV.PhongBan, NV.ChucVu, NV.MucLuong, NV.NgayVaoLam, NV.MaQuanLy, NV.TrangThai,
                   NV.NgayTao, NV.NgayCapNhat, NV.NgayXoa, NV.DiaChi, NV.SoCMND, NV.QueQuan,
                   ND.TenDangNhap, VT.TenVaiTro
            FROM NhanVien NV
            INNER JOIN NguoiDung ND ON NV.MaNguoiDung = ND.MaNguoiDung
            INNER JOIN VaiTro VT ON ND.MaVaiTro = VT.MaVaiTro
        """
        
        if not include_deleted:
            query += " WHERE NV.NgayXoa IS NULL"
        
        query += " ORDER BY NV.HoTen"
        
        cursor.execute(query)
        employees = [self._row_to_employee(row) for row in cursor.fetchall()]
        
        conn.close()
        return employees
    
    def get_paginated(self, page: int = 1, page_size: int = 20) -> Tuple[List[Employee], int]:
        """
        Lấy danh sách nhân viên có phân trang
        Hỗ trợ: UC05.1 - Phân trang nếu dữ liệu quá lớn
        
        Returns:
            (employees, total_count)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM NhanVien WHERE NgayXoa IS NULL")
        total_count = cursor.fetchone()[0]
        
        # Get paginated data
        offset = (page - 1) * page_size
        query = """
            SELECT NV.MaNhanVien, NV.MaNguoiDung, NV.HoTen, NV.NgaySinh, NV.SoDienThoai, NV.Email,
                   NV.PhongBan, NV.ChucVu, NV.MucLuong, NV.NgayVaoLam, NV.MaQuanLy, NV.TrangThai,
                   NV.NgayTao, NV.NgayCapNhat, NV.NgayXoa, NV.DiaChi, NV.SoCMND, NV.QueQuan,
                   ND.TenDangNhap, VT.TenVaiTro
            FROM NhanVien NV
            INNER JOIN NguoiDung ND ON NV.MaNguoiDung = ND.MaNguoiDung
            INNER JOIN VaiTro VT ON ND.MaVaiTro = VT.MaVaiTro
            WHERE NV.NgayXoa IS NULL
            ORDER BY NV.HoTen
            OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
        """
        
        cursor.execute(query, (offset, page_size))
        employees = [self._row_to_employee(row) for row in cursor.fetchall()]
        
        conn.close()
        return employees, total_count
    
    # ================================================
    # UC05.3: TÌM KIẾM NHÂN VIÊN
    # ================================================
    def search(self, keyword: str) -> List[Employee]:
        """
        Tìm kiếm nhân viên theo từ khóa
        Hỗ trợ: UC05.3 - Tìm kiếm nhân viên
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT NV.MaNhanVien, NV.MaNguoiDung, NV.HoTen, NV.NgaySinh, NV.SoDienThoai, NV.Email,
                   NV.PhongBan, NV.ChucVu, NV.MucLuong, NV.NgayVaoLam, NV.MaQuanLy, NV.TrangThai,
                   NV.NgayTao, NV.NgayCapNhat, NV.NgayXoa, NV.DiaChi, NV.SoCMND, NV.QueQuan,
                   ND.TenDangNhap, VT.TenVaiTro
            FROM NhanVien NV
            INNER JOIN NguoiDung ND ON NV.MaNguoiDung = ND.MaNguoiDung
            INNER JOIN VaiTro VT ON ND.MaVaiTro = VT.MaVaiTro
            WHERE NV.NgayXoa IS NULL
              AND (NV.HoTen LIKE ? 
                   OR NV.Email LIKE ? 
                   OR NV.SoDienThoai LIKE ?
                   OR NV.PhongBan LIKE ?
                   OR NV.ChucVu LIKE ?)
            ORDER BY NV.HoTen
        """
        
        search_param = f'%{keyword}%'
        cursor.execute(query, (search_param, search_param, search_param, search_param, search_param))
        employees = [self._row_to_employee(row) for row in cursor.fetchall()]
        
        conn.close()
        return employees
    
    # ================================================
    # UC05.4: XEM HỒ SƠ NHÂN VIÊN
    # ================================================
    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        """
        Lấy thông tin chi tiết nhân viên
        Hỗ trợ: UC05.4 - Xem hồ sơ nhân viên
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT NV.MaNhanVien, NV.MaNguoiDung, NV.HoTen, NV.NgaySinh, NV.SoDienThoai, NV.Email,
                   NV.PhongBan, NV.ChucVu, NV.MucLuong, NV.NgayVaoLam, NV.MaQuanLy, NV.TrangThai,
                   NV.NgayTao, NV.NgayCapNhat, NV.NgayXoa, NV.DiaChi, NV.SoCMND, NV.QueQuan,
                   ND.TenDangNhap, VT.TenVaiTro
            FROM NhanVien NV
            INNER JOIN NguoiDung ND ON NV.MaNguoiDung = ND.MaNguoiDung
            INNER JOIN VaiTro VT ON ND.MaVaiTro = VT.MaVaiTro
            WHERE NV.MaNhanVien = ? AND NV.NgayXoa IS NULL
        """
        
        cursor.execute(query, (employee_id,))
        row = cursor.fetchone()
        
        employee = self._row_to_employee(row) if row else None
        conn.close()
        return employee
    
    # ================================================
    # UC05.2: THÊM NHÂN VIÊN MỚI (CÓ PHÂN CHỨC VỤ + LƯƠNG)
    # ================================================
    def create(
        self, 
        user_id: int,
        full_name: str,
        email: str,
        phone: str,
        department: str,
        position: str,      # Chức vụ - QUAN TRỌNG
        salary: float,      # Mức lương - QUAN TRỌNG
        date_of_birth: Optional[date] = None,
        address: Optional[str] = None,
        identity_number: Optional[str] = None,
        hometown: Optional[str] = None,
        manager_id: Optional[int] = None
    ) -> Optional[int]:
        """
        Tạo nhân viên mới
        Hỗ trợ: UC05.2 - Thêm nhân viên mới (có phân chức vụ + mức lương)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO NhanVien (
                MaNguoiDung, HoTen, Email, SoDienThoai, PhongBan, ChucVu, MucLuong,
                NgaySinh, DiaChi, SoCMND, QueQuan, MaQuanLy, 
                TrangThai, NgayVaoLam
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, N'KichHoat', CAST(GETDATE() AS DATE))
        """
        
        try:
            cursor.execute(query, (
                user_id, full_name, email, phone, department, position, salary,
                date_of_birth, address, identity_number, hometown, manager_id
            ))
            conn.commit()
            
            # Get inserted ID
            cursor.execute("SELECT @@IDENTITY")
            employee_id = cursor.fetchone()[0]
            
            conn.close()
            return int(employee_id)
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    # ================================================
    # UC05.5: CHỈNH SỬA THÔNG TIN NHÂN VIÊN
    # ================================================
    def update(
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
    ) -> bool:
        """
        Cập nhật thông tin nhân viên
        Hỗ trợ: UC05.5 - Chỉnh sửa thông tin nhân viên
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        updates = []
        params = []
        
        if full_name is not None:
            updates.append("HoTen = ?")
            params.append(full_name)
        if email is not None:
            updates.append("Email = ?")
            params.append(email)
        if phone is not None:
            updates.append("SoDienThoai = ?")
            params.append(phone)
        if department is not None:
            updates.append("PhongBan = ?")
            params.append(department)
        if position is not None:
            updates.append("ChucVu = ?")
            params.append(position)
        if salary is not None:
            updates.append("MucLuong = ?")
            params.append(salary)
        if date_of_birth is not None:
            updates.append("NgaySinh = ?")
            params.append(date_of_birth)
        if address is not None:
            updates.append("DiaChi = ?")
            params.append(address)
        if identity_number is not None:
            updates.append("SoCMND = ?")
            params.append(identity_number)
        if hometown is not None:
            updates.append("QueQuan = ?")
            params.append(hometown)
        if manager_id is not None:
            updates.append("MaQuanLy = ?")
            params.append(manager_id)
        
        if not updates:
            return False
        
        updates.append("NgayCapNhat = GETDATE()")
        params.append(employee_id)
        
        query = f"UPDATE NhanVien SET {', '.join(updates)} WHERE MaNhanVien = ?"
        
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
    
    # ================================================
    # UC05.6: PHÂN QUYỀN (GÁN ROLE)
    # ================================================
    def change_role(self, user_id: int, new_role_id: int) -> bool:
        """
        Thay đổi quyền của nhân viên
        Hỗ trợ: UC05.6 - Phân quyền và thay đổi quyền hạn
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "UPDATE NguoiDung SET MaVaiTro = ?, NgayCapNhat = GETDATE() WHERE MaNguoiDung = ?"
        
        try:
            cursor.execute(query, (new_role_id, user_id))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    # ================================================
    # UC05.7: KHÓA/MỞ TÀI KHOẢN
    # ================================================
    def lock_account(self, employee_id: int) -> bool:
        """
        Khóa tài khoản nhân viên
        Hỗ trợ: UC05.7 - Khóa tài khoản
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE NhanVien 
            SET TrangThai = N'BiKhoa', NgayCapNhat = GETDATE()
            WHERE MaNhanVien = ?
        """
        
        # Also update NguoiDung table
        query2 = """
            UPDATE NguoiDung 
            SET KichHoat = 0, NgayCapNhat = GETDATE()
            WHERE MaNguoiDung = (SELECT MaNguoiDung FROM NhanVien WHERE MaNhanVien = ?)
        """
        
        try:
            cursor.execute(query, (employee_id,))
            cursor.execute(query2, (employee_id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    def unlock_account(self, employee_id: int) -> bool:
        """
        Mở khóa tài khoản nhân viên
        Hỗ trợ: UC05.7 - Mở khóa tài khoản
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE NhanVien 
            SET TrangThai = N'KichHoat', NgayCapNhat = GETDATE()
            WHERE MaNhanVien = ?
        """
        
        query2 = """
            UPDATE NguoiDung 
            SET KichHoat = 1, NgayCapNhat = GETDATE()
            WHERE MaNguoiDung = (SELECT MaNguoiDung FROM NhanVien WHERE MaNhanVien = ?)
        """
        
        try:
            cursor.execute(query, (employee_id,))
            cursor.execute(query2, (employee_id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    def soft_delete(self, employee_id: int) -> bool:
        """
        Soft delete nhân viên (đánh dấu xóa, không xóa thật)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE NhanVien 
            SET TrangThai = N'KhongKichHoat', NgayXoa = GETDATE(), NgayCapNhat = GETDATE()
            WHERE MaNhanVien = ?
        """
        
        try:
            cursor.execute(query, (employee_id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    # ================================================
    # THỐNG KÊ
    # ================================================
    def count_by_status(self, status: Optional[str] = None) -> int:
        """Đếm nhân viên theo trạng thái"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if status:
            query = "SELECT COUNT(*) FROM NhanVien WHERE TrangThai = ? AND NgayXoa IS NULL"
            cursor.execute(query, (status,))
        else:
            query = "SELECT COUNT(*) FROM NhanVien WHERE NgayXoa IS NULL"
            cursor.execute(query)
        
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def count_by_department(self, department: str) -> int:
        """Đếm nhân viên theo phòng ban"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) FROM NhanVien WHERE PhongBan = ? AND NgayXoa IS NULL"
        cursor.execute(query, (department,))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count