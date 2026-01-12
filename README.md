
# 🏦 BANK MANAGEMENT SYSTEM - HỆ THỐNG QUẢN LÝ NGÂN HÀNG

**Sinh viên thực hiện:** Nguyễn Thành Đạt  
**MSSV:** [20223688]  
**Môn học:** Phân tích Thiết kế Hướng Đối tượng  
**Ngày hoàn thành:** 06/01/2026

---

## 📋 MỤC LỤC

1. [Phạm vi công việc](#2-phạm-vi-công-việc)
2. [Kiến trúc hệ thống](#3-kiến-trúc-hệ-thống)
3. [Cơ sở dữ liệu](#4-cơ-sở-dữ-liệu)
4. [Chức năng đã triển khai](#5-chức-năng-đã-triển-khai)
5. [Công nghệ sử dụng](#6-công-nghệ-sử-dụng)
6. [Cấu trúc code](#7-cấu-trúc-code)
7. [Hướng dẫn cài đặt](#8-hướng-dẫn-cài-đặt)
8. [Hướng dẫn sử dụng](#9-hướng-dẫn-sử-dụng)
9. [Đặc điểm nổi bật](#10-đặc-điểm-nổi-bật)

---

## 2. PHẠM VI CÔNG VIỆC

Theo phân công nhóm, em chịu trách nhiệm thiết kế và phát triển **3 đối tượng**:

### ✅ Đối tượng 1: Nhân viên Tín dụng (Credit Officer)
- Tạo hồ sơ vay mới
- Thẩm định hồ sơ
- Phê duyệt hồ sơ
- Giải ngân
- Từ chối hồ sơ
- Dashboard với các biểu đồ thống kê

### ✅ Đối tượng 2: Quản lý Người dùng (Manager - User)
- Hiển thị danh sách nhân viên
- Thêm nhân viên mới (có ChucVu + MucLuong)
- Tìm kiếm nhân viên
- Xem chi tiết hồ sơ
- Chỉnh sửa thông tin
- Gán vai trò
- Khóa/Mở khóa tài khoản
- Export PDF danh sách

### ✅ Đối tượng 3: Quản lý Hệ thống Ngoài (Manager - External System)
- Thêm/Sửa/Xóa đối tác (VNPay, CIC, SBV...)
- Cập nhật trạng thái (KichHoat/KhongKichHoat/BaoTri)
- Export PDF danh sách

---

## 3. KIẾN TRÚC HỆ THỐNG 

### 3.1. Mô hình tổng quan: MVC + Repository Pattern

```
┌─────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                     │
│              (CustomTkinter GUI)                        │
│  - Welcome Screen, Login Screen                        │
│  - Credit Officer Workspace                            │
│  - Manager User Workspace                              │
│  - Manager System Workspace                            │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                   CONTROLLER LAYER                       │
│  - CreditOfficerController                             │
│  - ManagerController                                   │
│  - ExternalSystemController                            │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                   SERVICE LAYER                          │
│              (Business Logic)                           │
│  - CreditService (validation, workflow)                │
│  - EmployeeService (validation, business rules)        │
│  - ExternalSystemService                               │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                   REPOSITORY LAYER                       │
│              (Data Access)                              │
│  - CreditApplicationRepository (SQL queries)           │
│  - EmployeeRepository                                  │
│  - ExternalSystemRepository                            │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                   MODEL LAYER                            │
│  - Employee (class với properties & methods)           │
│  - CreditApplication (class)                           │
│  - ExternalSystem (class)                              │
└─────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                   DATABASE LAYER                         │
│         SQL Server - BankSystemOOP                      │
│              12 Bảng                                    │
└─────────────────────────────────────────────────────────┘
```

### 3.2. Design Patterns được áp dụng

#### A. MVC (Model-View-Controller)
**Tách biệt ba thành phần:**
- **Model:** Đối tượng nghiệp vụ (Employee, CreditApplication, ExternalSystem)
- **View:** Giao diện người dùng (CustomTkinter GUI)
- **Controller:** Xử lý logic điều khiển

#### B. Repository Pattern
**Tách biệt data access:**
- Service không biết SQL queries
- Repository handle tất cả database operations
- Dễ dàng thay đổi database (SQL Server → PostgreSQL)

#### C. Dependency Injection
**Loose coupling:**
```python
# Inject dependencies qua constructor
employee_repo = EmployeeRepository(connection_string)
employee_service = EmployeeService(employee_repo)
manager_ctrl = ManagerController(employee_service)
```

---

## 4. CƠ SỞ DỮ LIỆU

### 4.1. ERD - Sơ đồ quan hệ thực thể

```
┌─────────────┐          ┌──────────────────┐
│   VaiTro    │◄─────────│   NguoiDung      │
└─────────────┘    1:N   └──────────────────┘
                                │ 1
                                │
                                │ 1
                         ┌──────▼──────────┐
                         │   NhanVien      │
                         └─────────────────┘
                                │
                         ┌──────┴──────┐
                         │             │
            MaNhanVienPhuTrach  NguoiThamDinh
                         │             │
                         │             │
                    ┌────▼─────────────▼────┐
     ┌─────────┐    │     HoSoVay          │    ┌──────────────┐
     │KhachHang│────┤                      │────│ SanPhamVay   │
     └─────────┘ N:1└──────────────────────┘1:N └──────────────┘
                                │ 1
                                │
                                │ 1
                         ┌──────▼──────────┐
                         │ThamDinhTinDung  │
                         └─────────────────┘
                                │ 1
                                │
                                │ 1
                         ┌──────▼──────────┐
                         │   KhoanVay      │
                         └─────────────────┘
```

### 4.2. Bảng quan trọng

#### A. NhanVien
```sql
CREATE TABLE NhanVien (
    MaNhanVien INT PRIMARY KEY IDENTITY(1,1),
    MaNguoiDung INT NOT NULL UNIQUE,
    HoTen NVARCHAR(100) NOT NULL,
    NgaySinh DATE,
    SoDienThoai NVARCHAR(15),
    Email NVARCHAR(100),
    PhongBan NVARCHAR(100),
    ChucVu NVARCHAR(100),     
    MucLuong DECIMAL(18,2),         
    NgayVaoLam DATE,
    MaQuanLy INT,
    TrangThai NVARCHAR(20),
    
    CONSTRAINT FK_NhanVien_NguoiDung 
        FOREIGN KEY (MaNguoiDung) REFERENCES NguoiDung(MaNguoiDung),
    CONSTRAINT FK_NhanVien_QuanLy 
        FOREIGN KEY (MaQuanLy) REFERENCES NhanVien(MaNhanVien)
);
```

#### B. HoSoVay
```sql
CREATE TABLE HoSoVay (
    MaHoSo INT PRIMARY KEY IDENTITY(1,1),
    SoHoSo NVARCHAR(50) UNIQUE NOT NULL,
    MaKhachHang INT NOT NULL,
    MaSanPham INT NOT NULL,
    SoTienYeuCau DECIMAL(18,2) NOT NULL,
    KyHanYeuCau INT NOT NULL,
    MucDich NVARCHAR(255),
    TrangThai NVARCHAR(50) DEFAULT N'ChoXuLy',
    
    -- 3 Foreign Keys đến NhanVien (workflow)
    MaNhanVienPhuTrach INT,
    NguoiThamDinh INT,
    NguoiPheDuyet INT,
    
    NgayNop DATETIME DEFAULT GETDATE(),
    NgayThamDinh DATETIME,
    NgayPheDuyet DATETIME,
    NgayGiaiNgan DATETIME,
    
    CONSTRAINT FK_HoSo_KhachHang 
        FOREIGN KEY (MaKhachHang) REFERENCES KhachHang(MaKhachHang),
    CONSTRAINT FK_HoSo_SanPham 
        FOREIGN KEY (MaSanPham) REFERENCES SanPhamVay(MaSanPham),
    CONSTRAINT FK_HoSo_NhanVien 
        FOREIGN KEY (MaNhanVienPhuTrach) REFERENCES NhanVien(MaNhanVien),
    CONSTRAINT FK_HoSo_NguoiThamDinh 
        FOREIGN KEY (NguoiThamDinh) REFERENCES NhanVien(MaNhanVien),
    CONSTRAINT FK_HoSo_NguoiPheDuyet 
        FOREIGN KEY (NguoiPheDuyet) REFERENCES NhanVien(MaNhanVien)
);
```

#### C. HeThongNgoai
```sql
CREATE TABLE HeThongNgoai (
    MaHeThong INT PRIMARY KEY IDENTITY(1,1),
    TenHeThong NVARCHAR(100) NOT NULL,
    LoaiHeThong NVARCHAR(50),
    DiaChiAPI NVARCHAR(255),
    KhoaAPI NVARCHAR(255),
    TrangThai NVARCHAR(20) DEFAULT N'KichHoat',
    MoTa NVARCHAR(500),
    
    CONSTRAINT CK_LoaiHeThong 
        CHECK (LoaiHeThong IN ('ThanhToan', 'KiemTraTinDung', 'TyGia', 'Khac')),
    CONSTRAINT CK_TrangThai 
        CHECK (TrangThai IN (N'KichHoat', N'KhongKichHoat', N'BaoTri'))
);
```

### 4.3. Indexes cho Performance
```sql
-- Tối ưu query
CREATE INDEX IX_NguoiDung_TenDangNhap ON NguoiDung(TenDangNhap);
CREATE INDEX IX_NhanVien_TrangThai ON NhanVien(TrangThai);
CREATE INDEX IX_HoSo_TrangThai ON HoSoVay(TrangThai);
CREATE INDEX IX_HoSo_KhachHang ON HoSoVay(MaKhachHang);
CREATE INDEX IX_KhoanVay_TrangThai ON KhoanVay(TrangThai);
```

### 4.4. Workflow State Machine
```
HoSoVay.TrangThai:

ChoXuLy → DangThamDinh → DaDuyet → DaGiaiNgan → HoanThanh
    ↓                        ↓
  TuChoi                  DaHuy
```

---

## 5. CHỨC NĂNG ĐÃ TRIỂN KHAI

### 5.1. Nhân viên Tín dụng (Credit Officer)

#### Tạo hồ sơ vay mới
**Mô tả:**
- Nhân viên tạo hồ sơ vay cho khách hàng

**Luồng xử lý:**
1. Chọn khách hàng từ dropdown (load từ DB)
2. Chọn sản phẩm vay từ dropdown (load từ DB)
3. Nhập số tiền vay, kỳ hạn, mục đích
4. Hệ thống hiển thị thông tin lãi suất tự động
5. Validate dữ liệu (SoTienYeuCau > 0, KyHanYeuCau > 0)
6. Generate SoHoSo: `APP-YYYY-NNNNNN`
7. INSERT vào database với TrangThai = N'ChoXuLy'

**Code location:**
- View: `bank_app_final_COMPLETE.py` (dòng 510-600)
- Controller: `credit_officer_controller.py` (dòng 25-40)
- Service: `credit_service.py` (dòng 20-60)
- Repository: `credit_application_repository.py` (dòng 25-50)

**SQL query:**
```sql
INSERT INTO HoSoVay 
(SoHoSo, MaKhachHang, MaSanPham, SoTienYeuCau, 
 KyHanYeuCau, MucDich, TrangThai, MaNhanVienPhuTrach, NgayNop)
VALUES (?, ?, ?, ?, ?, ?, N'ChoXuLy', ?, GETDATE())
```

---

#### Thẩm định hồ sơ
**Mô tả:**
- Nhân viên bắt đầu thẩm định hồ sơ đang chờ

**Luồng xử lý:**
1. Hiển thị danh sách hồ sơ TrangThai = N'ChoXuLy'
2. Nhân viên chọn hồ sơ và bấm "Bắt đầu thẩm định"
3. Check TrangThai phải là N'ChoXuLy'
4. UPDATE TrangThai = N'DangThamDinh'
5. SET NguoiThamDinh = current_officer_id
6. SET NgayThamDinh = GETDATE()

**State transition:**
```
ChoXuLy → DangThamDinh
```

**SQL query:**
```sql
UPDATE HoSoVay 
SET TrangThai = N'DangThamDinh', 
    NguoiThamDinh = ?,
    NgayThamDinh = GETDATE(),
    NgayCapNhat = GETDATE()
WHERE MaHoSo = ? AND TrangThai = N'ChoXuLy'
```

---

#### Phê duyệt hồ sơ
**Mô tả:**
- Phê duyệt hồ sơ đã thẩm định

**Luồng xử lý:**
1. Hiển thị danh sách TrangThai = N'DangThamDinh'
2. Nhân viên/Manager chọn hồ sơ và bấm "Phê duyệt"
3. Validate: TrangThai phải là N'DangThamDinh'
4. UPDATE TrangThai = N'DaDuyet'
5. SET NguoiPheDuyet, NgayPheDuyet

**State transition:**
```
DangThamDinh → DaDuyet
```

**SQL query:**
```sql
UPDATE HoSoVay
SET TrangThai = N'DaDuyet',
    NguoiPheDuyet = ?,
    NgayPheDuyet = GETDATE(),
    GhiChu = ?,
    NgayCapNhat = GETDATE()
WHERE MaHoSo = ? AND TrangThai = N'DangThamDinh'
```

---

#### Giải ngân
**Mô tả:**
- Giải ngân cho hồ sơ đã được phê duyệt

**Luồng xử lý:**
1. Hiển thị danh sách TrangThai = N'DaDuyet'
2. Nhân viên chọn và bấm "Giải ngân"
3. Validate: TrangThai = N'DaDuyet'
4. UPDATE TrangThai = N'DaGiaiNgan'
5. SET NgayGiaiNgan
6. INSERT vào bảng KhoanVay (tạo khoản vay chính thức)

**State transition:**
```
DaDuyet → DaGiaiNgan
```

**SQL query:**
```sql
UPDATE HoSoVay
SET TrangThai = N'DaGiaiNgan',
    NgayGiaiNgan = GETDATE(),
    NgayCapNhat = GETDATE()
WHERE MaHoSo = ? AND TrangThai = N'DaDuyet'
```

---

#### Từ chối hồ sơ
**Mô tả:**
- Từ chối hồ sơ không đủ điều kiện

**Luồng xử lý:**
1. Hiển thị danh sách TrangThai = N'DangThamDinh'
2. Nhân viên/Manager chọn và bấm "Từ chối"
3. Input dialog yêu cầu nhập lý do
4. UPDATE TrangThai = N'TuChoi'
5. SET LyDoTuChoi

**State transition:**
```
DangThamDinh → TuChoi
```

**SQL query:**
```sql
UPDATE HoSoVay
SET TrangThai = N'TuChoi',
    NguoiPheDuyet = ?,
    NgayPheDuyet = GETDATE(),
    LyDoTuChoi = ?,
    NgayCapNhat = GETDATE()
WHERE MaHoSo = ?
```

---

#### Dashboard với Biểu đồ
**Mô tả:**
- Thống kê trực quan hồ sơ vay

**Tính năng:**
1. **Cards thống kê:**
   - Tổng số hồ sơ
   - Chờ xử lý (ChoXuLy)
   - Đang thẩm định (DangThamDinh)
   - Đã duyệt (DaDuyet)
   - Đã giải ngân (DaGiaiNgan)
   - Từ chối (TuChoi)

2. **Pie Chart (Matplotlib):**
   - Phân bổ trạng thái theo %
   - Màu sắc phân biệt rõ ràng

3. **Bar Chart (Matplotlib):**
   - Số lượng hồ sơ theo trạng thái
   - Value labels trên mỗi cột

4. **Dynamic Time:**
   - Cập nhật mỗi giây

**Code:**
```python
# Statistics query
SELECT 
    COUNT(*) as TongSo,
    SUM(CASE WHEN TrangThai = N'ChoXuLy' THEN 1 ELSE 0 END) as ChoXuLy,
    SUM(CASE WHEN TrangThai = N'DangThamDinh' THEN 1 ELSE 0 END) as DangThamDinh,
    SUM(CASE WHEN TrangThai = N'DaDuyet' THEN 1 ELSE 0 END) as DaDuyet,
    SUM(CASE WHEN TrangThai = N'DaGiaiNgan' THEN 1 ELSE 0 END) as DaGiaiNgan,
    SUM(CASE WHEN TrangThai = N'TuChoi' THEN 1 ELSE 0 END) as TuChoi
FROM HoSoVay
```

---

### 5.2. Manager - Quản lý Người dùng

#### Hiển thị danh sách nhân viên
**Mô tả:**
- Hiển thị toàn bộ nhân viên trong hệ thống

**Tính năng:**
- Treeview với 7 cột: MaNhanVien, HoTen, Email, PhongBan, **ChucVu**, **MucLuong**, TrangThai
- Sort by MaNhanVien
- Load từ database qua Repository Pattern

**SQL query:**
```sql
SELECT MaNhanVien, HoTen, Email, PhongBan, 
       ChucVu, MucLuong, TrangThai
FROM NhanVien
WHERE NgayXoa IS NULL
ORDER BY MaNhanVien
```

---

#### Thêm nhân viên mới ⭐
**Mô tả:**
- Thêm nhân viên mới **CÓ ChucVu và MucLuong**

**Luồng xử lý:**
1. Hiển thị dialog form scrollable
2. Nhập: TenDangNhap, MatKhau, HoTen, Email, SoDienThoai, PhongBan, **ChucVu**, **MucLuong**
3. Validate:
   - Email có @ không
   - MucLuong > 0
   - Required fields không rỗng
4. **Step 1:** INSERT INTO NguoiDung (TenDangNhap, MatKhau, MaVaiTro)
5. Get MaNguoiDung từ @@IDENTITY
6. **Step 2:** INSERT INTO NhanVien (MaNguoiDung, HoTen, **ChucVu**, **MucLuong**, ...)
7. Reload danh sách

**Validation code:**
```python
# Email validation
if email and '@' not in email:
    return False, "Email không hợp lệ"

# Salary validation
try:
    salary_val = float(salary)
    if salary_val <= 0:
        return False, "Lương phải lớn hơn 0"
except ValueError:
    return False, "Lương không hợp lệ"
```

**SQL queries:**
```sql
-- Step 1: Create User
INSERT INTO NguoiDung (TenDangNhap, MatKhau, MaVaiTro, KichHoat)
VALUES (?, ?, ?, 1);

SELECT @@IDENTITY;

-- Step 2: Create Employee
INSERT INTO NhanVien 
(MaNguoiDung, HoTen, Email, SoDienThoai, PhongBan, 
 ChucVu, MucLuong, NgayVaoLam, TrangThai)
VALUES (?, ?, ?, ?, ?, ?, ?, CAST(GETDATE() AS DATE), N'KichHoat');
```

---

#### Tìm kiếm nhân viên
**Mô tả:**
- Tìm kiếm theo từ khóa

**Tính năng:**
- Search box + button
- Search theo: HoTen, Email, PhongBan
- Hiển thị kết quả trong Treeview

**SQL query:**
```sql
SELECT * FROM NhanVien
WHERE (HoTen LIKE '%' + ? + '%' 
       OR Email LIKE '%' + ? + '%'
       OR PhongBan LIKE '%' + ? + '%')
  AND NgayXoa IS NULL
```

---

#### Xem chi tiết hồ sơ
**Mô tả:**
- Xem thông tin đầy đủ của nhân viên

**Tính năng:**
- Select nhân viên trong Treeview
- Bấm "Xem chi tiết"
- MessageBox hiển thị: MaNhanVien, HoTen, Email, PhongBan, ChucVu, MucLuong, TrangThai

---

#### Chỉnh sửa thông tin
**Mô tả:**
- Sửa thông tin nhân viên

**Luồng xử lý:**
1. Select nhân viên và bấm "Chỉnh sửa"
2. Dialog pre-filled với dữ liệu hiện tại
3. Cho phép sửa: HoTen, Email, SoDienThoai, PhongBan, **ChucVu**, **MucLuong**
4. Validate trước khi UPDATE
5. UPDATE vào database

**SQL query:**
```sql
UPDATE NhanVien
SET HoTen = ?,
    Email = ?,
    SoDienThoai = ?,
    PhongBan = ?,
    ChucVu = ?,
    MucLuong = ?,
    NgayCapNhat = GETDATE()
WHERE MaNhanVien = ?
```

---

#### Gán vai trò
**Mô tả:**
- Integrated trong UC05.2 khi tạo NguoiDung với MaVaiTro

---

#### Khóa/Mở khóa tài khoản
**Mô tả:**
- Toggle trạng thái KichHoat ↔ BiKhoa

**Luồng xử lý:**
1. Select nhân viên
2. Bấm "Khóa/Mở khóa"
3. Check TrangThai hiện tại
4. UPDATE TrangThai = N'BiKhoa' (nếu KichHoat) hoặc N'KichHoat' (nếu BiKhoa)

**SQL query:**
```sql
UPDATE NhanVien
SET TrangThai = CASE 
    WHEN TrangThai = N'KichHoat' THEN N'BiKhoa'
    WHEN TrangThai = N'BiKhoa' THEN N'KichHoat'
END,
NgayCapNhat = GETDATE()
WHERE MaNhanVien = ?
```

---

#### Export PDF - Danh sách Nhân viên
**Mô tả:**
- Export danh sách ra file PDF

**Tính năng:**
1. Get all employees từ database
2. Sort by MaNhanVien
3. Create PDF với ReportLab
4. Landscape A4 format
5. Table với styled header (blue #1f6aa5)
6. Alternating row colors (white/lightgrey)
7. Grid lines
8. Filename: `DanhSachNhanVien_YYYYMMDD_HHMMSS.pdf`

**Code:**
```python
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Create document
doc = SimpleDocTemplate(filename, pagesize=landscape(A4))

# Table data
data = [['Mã NV', 'Họ tên', 'Email', 'Phòng ban', 'Chức vụ', 'Lương', 'Trạng thái']]
for emp in employees:
    data.append([emp.id, emp.name, emp.email, ...])

# Style
table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1f6aa5')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.lightgrey])
]))
```

---

### 5.3. Manager - Quản lý Hệ thống Ngoài

#### Thêm đối tác mới
**Mô tả:**
- Thêm hệ thống đối tác (VNPay, CIC, SBV...)

**Luồng xử lý:**
1. Dialog form với các fields:
   - TenHeThong (required)
   - LoaiHeThong: dropdown (ThanhToan, KiemTraTinDung, TyGia, Khac)
   - DiaChiAPI
   - KhoaAPI
   - MoTa
2. Validate: TenHeThong không rỗng
3. INSERT vào HeThongNgoai

**SQL query:**
```sql
INSERT INTO HeThongNgoai 
(TenHeThong, LoaiHeThong, DiaChiAPI, KhoaAPI, 
 MoTa, TrangThai, NgayTao)
VALUES (?, ?, ?, ?, ?, N'KichHoat', GETDATE())
```

---

#### Cập nhật trạng thái
**Mô tả:**
- Thay đổi trạng thái hệ thống

**Luồng xử lý:**
1. Select hệ thống
2. Bấm "Cập nhật trạng thái"
3. Dialog với radio buttons: KichHoat, KhongKichHoat, BaoTri
4. UPDATE TrangThai

**SQL query:**
```sql
UPDATE HeThongNgoai
SET TrangThai = ?,
    NgayCapNhat = GETDATE()
WHERE MaHeThong = ?
```

---

#### Xóa đối tác
**Mô tả:**
- Xóa hệ thống đối tác

**Luồng xử lý:**
1. Select hệ thống
2. Bấm "Xóa"
3. Confirmation dialog
4. DELETE

**SQL query:**
```sql
DELETE FROM HeThongNgoai WHERE MaHeThong = ?
```

---

#### Export PDF - Danh sách Hệ thống
**Mô tả:**
- Export danh sách đối tác ra PDF

**Tính năng:**
- Tương tự Employee PDF
- Styled header (teal #16a085)
- Table: MaHeThong, TenHeThong, LoaiHeThong, DiaChiAPI, TrangThai
- Filename: `DanhSachHeThong_YYYYMMDD_HHMMSS.pdf`

---

## 6. CÔNG NGHỆ SỬ DỤNG

### 6.1. Backend
- **Python 3.11**
- **PyODBC 5.0.1** - SQL Server connection
- **Decimal** - Xử lý số tiền chính xác

### 6.2. Database
- **SQL Server 2019+**
- **ODBC Driver 18 for SQL Server**

### 6.3. Frontend
- **CustomTkinter 5.2.1** - Modern GUI framework
- **Tkinter** - Base GUI

### 6.4. Visualization
- **Matplotlib 3.8.0** - Charts (Pie, Bar)
- **FigureCanvasTkAgg** - Embed charts in Tkinter

### 6.5. PDF Export
- **ReportLab 4.0.7** - PDF generation
- **reportlab.platypus** - Table layout
- **reportlab.lib.colors** - Styling

### 6.6. Others
- **datetime** - Time handling
- **typing** - Type hints

---

## 7. CẤU TRÚC CODE

```
bank_management_system/
│
├── models/                          # MODEL LAYER
│   ├── employee.py                  # Employee class 
│   ├── credit_application.py        # CreditApplication class 
│   └── external_system.py           # ExternalSystem class
│
├── repositories/                    # REPOSITORY LAYER
│   ├── employee_repository.py       # Employee data access 
│   ├── credit_application_repository.py  # Credit data access 
│   └── external_system_repository.py     # System data access
│
├── services/                        # SERVICE LAYER
│   ├── employee_service.py          # Employee business logic 
│   ├── credit_service.py            # Credit business logic 
│   └── external_system_service.py   # System business logic
│
├── controllers/                     # CONTROLLER LAYER
│   ├── manager_controller.py        # Manager operations 
│   ├── credit_officer_controller.py # Credit operations
│   └── external_system_controller.py # System operations
│
├── bank_app_final.py      # MAIN APP - VIEW LAYER 
├── database_schema.sql              # Database schema
├── sample_data.sql                  # Sample data insert
├── README.md                        # This file
└── requirements.txt                 # Dependencies

TỔNG SỐ DÒNG CODE: ~3,800 dòng
```

### 7.1. Giải thích từng layer (Đầy đủ 3 đối tượng)

Em sẽ giải thích chi tiết từng layer cho cả 3 đối tượng: **Employee** (Manager-User), **CreditApplication** (Credit Officer), và **ExternalSystem** (Manager-System).

---

## A. MODEL LAYER - Các đối tượng nghiệp vụ

### 1. Employee Model (Đối tượng Nhân viên - Manager User)

```python
# models/employee.py
class Employee:
    """
    Đại diện cho một nhân viên trong hệ thống
    
    Responsibilities:
    - Lưu trữ thông tin nhân viên
    - Provide business methods (get_display_name, is_active...)
    - Encapsulation của employee data
    
    Attributes:
        employee_id (int): ID duy nhất
        user_id (int): Liên kết với NguoiDung table (1-1)
        full_name (str): Họ tên đầy đủ
        date_of_birth (date): Ngày sinh
        phone (str): Số điện thoại
        email (str): Email
        department (str): Phòng ban (VD: "Tín dụng", "Kế toán")
        position (str): Chức vụ (VD: "Chuyên viên", "Trưởng phòng")
        salary (Decimal): Lương (VND)
        hire_date (date): Ngày vào làm
        manager_id (int): ID của manager (self-reference)
        status (str): 'KichHoat' hoặc 'BiKhoa'
        created_at (datetime): Ngày tạo record
        updated_at (datetime): Ngày cập nhật cuối
    """
    
    def __init__(self, employee_id, user_id, full_name, date_of_birth,
                 phone, email, department, position, salary, hire_date,
                 manager_id, status, created_at=None, updated_at=None):
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
    
    # Business methods
    def get_display_name(self) -> str:
        """Tên hiển thị kèm chức vụ cho UI"""
        return f"{self.full_name} ({self.position})"
    
    def get_formatted_salary(self) -> str:
        """Format lương với dấu phẩy"""
        return f"{self.salary:,.0f} VND"
    
    def is_active(self) -> bool:
        """Check nhân viên còn active không"""
        return self.status == 'KichHoat'
    
    def years_of_service(self) -> int:
        """Tính số năm công tác"""
        from datetime import date
        return (date.today() - self.hire_date).days // 365
    
    def __repr__(self):
        return f"Employee(id={self.employee_id}, name={self.full_name}, position={self.position})"
```

**Giải thích chi tiết:**
- **Tại sao cần Model:** 
  - Encapsulation: Gom tất cả properties của Employee
  - Type safety: IDE biết được attributes, autocomplete
  - Business methods: `get_display_name()`, `is_active()`, `years_of_service()`
  - Dễ serialize: Convert sang dict/JSON khi cần
  - Reusability: Dùng ở nhiều nơi (View, Service, Controller)

- **Tại sao có Position và Salary:**
  - UC05.2 yêu cầu: "Thêm nhân viên mới có ChucVu + MucLuong"
  - UC05.1 yêu cầu: Hiển thị ChucVu và MucLuong trong danh sách
  - Business need: Quản lý cấp bậc và quỹ lương

---

### 2. CreditApplication Model (Đối tượng Hồ sơ vay - Credit Officer)

```python
# models/credit_application.py
from datetime import datetime
from decimal import Decimal

class CreditApplication:
    """
    Đại diện cho một hồ sơ vay vốn
    
    Responsibilities:
    - Lưu trữ thông tin hồ sơ vay
    - Workflow state validation methods
    - Format display methods
    - Business logic cho state transitions
    
    Attributes:
        application_id (int): ID duy nhất
        application_number (str): Mã hồ sơ (VD: "APP-20260105123045")
        customer_id (int): ID khách hàng
        customer_name (str): Tên khách hàng (denormalized for display)
        product_id (int): ID sản phẩm vay
        product_name (str): Tên sản phẩm vay
        requested_amount (Decimal): Số tiền vay (VND)
        requested_term (int): Kỳ hạn (tháng)
        purpose (str): Mục đích vay
        status (str): Trạng thái workflow
        
        # 3 Officers khác nhau xử lý (Workflow)
        assigned_officer_id (int): Nhân viên được giao
        assigned_officer_name (str): Tên nhân viên được giao
        reviewed_by (int): Nhân viên thẩm định
        reviewer_name (str): Tên người thẩm định
        approved_by (int): Nhân viên phê duyệt
        approver_name (str): Tên người phê duyệt
        
        # Timestamps theo workflow
        application_date (datetime): Ngày nộp hồ sơ
        review_date (datetime): Ngày bắt đầu thẩm định
        approval_date (datetime): Ngày phê duyệt
        disbursement_date (datetime): Ngày giải ngân
        
        rejection_reason (str): Lý do từ chối (nếu có)
    """
    
    def __init__(self, application_id, application_number, customer_id,
                 customer_name, product_id, product_name, requested_amount,
                 requested_term, purpose, status, assigned_officer_id=None,
                 assigned_officer_name=None, reviewed_by=None, reviewer_name=None,
                 approved_by=None, approver_name=None, application_date=None,
                 review_date=None, approval_date=None, disbursement_date=None,
                 rejection_reason=None, created_at=None, updated_at=None):
        
        self.application_id = application_id
        self.application_number = application_number
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.product_id = product_id
        self.product_name = product_name
        self.requested_amount = requested_amount
        self.requested_term = requested_term
        self.purpose = purpose
        self.status = status
        self.assigned_officer_id = assigned_officer_id
        self.assigned_officer_name = assigned_officer_name
        self.reviewed_by = reviewed_by
        self.reviewer_name = reviewer_name
        self.approved_by = approved_by
        self.approver_name = approver_name
        self.application_date = application_date
        self.review_date = review_date
        self.approval_date = approval_date
        self.disbursement_date = disbursement_date
        self.rejection_reason = rejection_reason
        self.created_at = created_at
        self.updated_at = updated_at
    
    # Display methods
    def get_formatted_amount(self) -> str:
        """Format số tiền với dấu phẩy"""
        return f"{self.requested_amount:,.0f} VND"
    
    def get_status_display(self) -> str:
        """Hiển thị status tiếng Việt"""
        status_map = {
            'ChoXuLy': 'Chờ xử lý',
            'DangThamDinh': 'Đang thẩm định',
            'DaDuyet': 'Đã duyệt',
            'TuChoi': 'Từ chối',
            'DaGiaiNgan': 'Đã giải ngân',
            'HoanThanh': 'Hoàn thành',
            'DaHuy': 'Đã hủy'
        }
        return status_map.get(self.status, self.status)
    
    # Workflow state validation methods
    def can_start_review(self) -> bool:
        """UC03.2: Check có thể bắt đầu thẩm định không"""
        return self.status == 'ChoXuLy'
    
    def can_approve(self) -> bool:
        """UC03.3: Check có thể phê duyệt không"""
        return self.status == 'DangThamDinh'
    
    def can_disburse(self) -> bool:
        """UC03.4: Check có thể giải ngân không"""
        return self.status == 'DaDuyet'
    
    def can_reject(self) -> bool:
        """UC03.8: Check có thể từ chối không"""
        return self.status in ['ChoXuLy', 'DangThamDinh']
    
    def get_workflow_history(self) -> str:
        """Lấy lịch sử workflow cho display"""
        history = []
        if self.application_date:
            history.append(f"Tạo: {self.application_date.strftime('%d/%m/%Y')}")
        if self.review_date:
            history.append(f"Thẩm định: {self.review_date.strftime('%d/%m/%Y')}")
        if self.approval_date:
            history.append(f"Phê duyệt: {self.approval_date.strftime('%d/%m/%Y')}")
        if self.disbursement_date:
            history.append(f"Giải ngân: {self.disbursement_date.strftime('%d/%m/%Y')}")
        return " → ".join(history)
    
    def get_days_pending(self) -> int:
        """Số ngày chờ xử lý"""
        if self.application_date:
            return (datetime.now() - self.application_date).days
        return 0
    
    def __repr__(self):
        return f"CreditApplication(id={self.application_id}, number={self.application_number}, status={self.status})"
```

**Giải thích chi tiết:**
- **Tại sao phức tạp hơn Employee:**
  - Workflow phức tạp: 7 trạng thái với rules
  - 3 Officers khác nhau: assigned, reviewed, approved
  - State validation: `can_approve()`, `can_disburse()`
  - Business logic: Không thể skip states

- **Denormalized data (customer_name, product_name):**
  - Performance: Không cần JOIN mỗi lần display
  - Display efficiency: Có tên sẵn để hiển thị

---

### 3. ExternalSystem Model (Đối tượng Hệ thống ngoài - Manager System)

```python
# models/external_system.py
from datetime import datetime

class ExternalSystem:
    """
    Đại diện cho một hệ thống đối tác bên ngoài
    
    Responsibilities:
    - Lưu thông tin kết nối API
    - Security methods (mask API key)
    - Type checking methods
    - Status display methods
    
    Attributes:
        system_id (int): ID duy nhất
        system_name (str): Tên hệ thống (VD: "VNPay", "CIC", "SBV")
        system_type (str): Loại (ThanhToan, KiemTraTinDung, TyGia, Khac)
        api_endpoint (str): URL endpoint
        api_key (str): API key (sensitive data)
        status (str): KichHoat, KhongKichHoat, BaoTri
        description (str): Mô tả chi tiết
        last_sync (datetime): Lần đồng bộ cuối cùng
        created_at (datetime): Ngày tạo
        updated_at (datetime): Ngày cập nhật
    """
    
    def __init__(self, system_id, system_name, system_type, api_endpoint,
                 api_key=None, status='KichHoat', description=None, last_sync=None,
                 created_at=None, updated_at=None):
        
        self.system_id = system_id
        self.system_name = system_name
        self.system_type = system_type
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.status = status
        self.description = description
        self.last_sync = last_sync
        self.created_at = created_at
        self.updated_at = updated_at
    
    # Status checking methods
    def is_active(self) -> bool:
        """Check hệ thống đang active không"""
        return self.status == 'KichHoat'
    
    def is_maintenance(self) -> bool:
        """Check hệ thống đang bảo trì không"""
        return self.status == 'BaoTri'
    
    # Type checking methods
    def is_payment_gateway(self) -> bool:
        """Check có phải payment gateway không"""
        return self.system_type == 'ThanhToan'
    
    def is_credit_check(self) -> bool:
        """Check có phải hệ thống kiểm tra tín dụng không"""
        return self.system_type == 'KiemTraTinDung'
    
    def is_exchange_rate(self) -> bool:
        """Check có phải hệ thống tỷ giá không"""
        return self.system_type == 'TyGia'
    
    # Display methods
    def get_type_display(self) -> str:
        """Hiển thị loại hệ thống tiếng Việt"""
        type_map = {
            'ThanhToan': 'Cổng thanh toán',
            'KiemTraTinDung': 'Kiểm tra tín dụng',
            'TyGia': 'Tỷ giá ngoại tệ',
            'Khac': 'Khác'
        }
        return type_map.get(self.system_type, self.system_type)
    
    def get_status_display(self) -> str:
        """Hiển thị trạng thái tiếng Việt"""
        status_map = {
            'KichHoat': 'Đang hoạt động',
            'KhongKichHoat': 'Ngưng hoạt động',
            'BaoTri': 'Đang bảo trì'
        }
        return status_map.get(self.status, self.status)
    
    # Security method
    def get_masked_api_key(self) -> str:
        """
        Ẩn API key để bảo mật (chỉ hiện 4 ký tự cuối)
        
        Example: "sk_live_1234567890abcdef" → "************cdef"
        """
        if not self.api_key or len(self.api_key) < 4:
            return "****"
        return "*" * (len(self.api_key) - 4) + self.api_key[-4:]
    
    def get_last_sync_display(self) -> str:
        """Hiển thị thời gian sync cuối"""
        if not self.last_sync:
            return "Chưa đồng bộ"
        return self.last_sync.strftime("%d/%m/%Y %H:%M")
    
    def __repr__(self):
        return f"ExternalSystem(id={self.system_id}, name={self.system_name}, type={self.system_type})"
```

**Giải thích chi tiết:**
- **Tại sao cần Security method:**
  - API key là sensitive data
  - Không thể hiển thị trực tiếp trên UI
  - `get_masked_api_key()` protect data

- **Type checking methods:**
  - Business logic khác nhau cho từng type
  - VD: Payment gateway cần validate transaction, Credit check cần CIC score

---

## B. REPOSITORY LAYER - Data Access (SQL Queries)

Repository chịu trách nhiệm **TẤT CẢ** SQL queries. Service và Controller **KHÔNG BAO GIỜ** viết SQL.

### 1. EmployeeRepository (Manager - User Management)

```python
# repositories/employee_repository.py
import pyodbc
from typing import List, Optional, Tuple
from decimal import Decimal
from models.employee import Employee

class EmployeeRepository:
    """
    Repository cho Employee data access
    
    Responsibilities:
    - TẤT CẢ SQL queries cho NhanVien table
    - Mapping DB rows → Employee objects
    - CRUD operations
    - Search operations
    """
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
    
    def _get_connection(self):
        """Helper: Tạo database connection"""
        return pyodbc.connect(self.connection_string)
    
    def _map_to_employee(self, row) -> Employee:
        """
        Helper: Convert DB row → Employee object
        
        Tại sao cần method này:
        - Centralized mapping logic
        - Dễ maintain khi schema thay đổi
        - Type conversion (date, decimal)
        """
        return Employee(
            employee_id=row.MaNhanVien,
            user_id=row.MaNguoiDung,
            full_name=row.HoTen,
            date_of_birth=row.NgaySinh,
            phone=row.SoDienThoai,
            email=row.Email,
            department=row.PhongBan,
            position=row.ChucVu,      
            salary=row.MucLuong,          
            hire_date=row.NgayVaoLam,
            manager_id=row.MaQuanLy,
            status=row.TrangThai,
            created_at=row.NgayTao,
            updated_at=row.NgayCapNhat
        )
    
    def get_all(self) -> List[Employee]:
        """
        UC05.1: Lấy tất cả nhân viên
        
        SQL Query breakdown:
        - SELECT: Tất cả columns cần thiết
        - WHERE NgayXoa IS NULL: Chỉ lấy active records (soft delete)
        - ORDER BY MaNhanVien: Sort theo ID
        
        Returns:
            List[Employee]: Danh sách Employee objects
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                MaNhanVien, MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email,
                PhongBan, ChucVu, MucLuong, NgayVaoLam, MaQuanLy, TrangThai,
                NgayTao, NgayCapNhat
            FROM NhanVien
            WHERE NgayXoa IS NULL
            ORDER BY MaNhanVien
        """)
        
        employees = [self._map_to_employee(row) for row in cursor.fetchall()]
        conn.close()
        return employees
    
    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        """
        UC05.4: Lấy nhân viên theo ID
        
        Returns:
            Optional[Employee]: Employee object hoặc None nếu không tìm thấy
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                MaNhanVien, MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email,
                PhongBan, ChucVu, MucLuong, NgayVaoLam, MaQuanLy, TrangThai,
                NgayTao, NgayCapNhat
            FROM NhanVien
            WHERE MaNhanVien = ? AND NgayXoa IS NULL
        """, (employee_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return self._map_to_employee(row) if row else None
    
    def create(self, user_id: int, full_name: str, email: str, phone: str,
               department: str, position: str, salary: Decimal) -> Tuple[bool, int, str]:
        """
        UC05.2: Tạo nhân viên mới
        
        SQL Query breakdown:
        - INSERT INTO NhanVien: Thêm record mới
        - VALUES: user_id, full_name, position, salary, ...
        - NgayVaoLam: CAST(GETDATE() AS DATE) - Ngày hiện tại
        - TrangThai: N'KichHoat' - Mặc định active
        - NgayTao: GETDATE() - Timestamp
        
        Returns:
            Tuple[bool, int, str]: (success, employee_id, message)
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO NhanVien 
                (MaNguoiDung, HoTen, Email, SoDienThoai, PhongBan, 
                 ChucVu, MucLuong, NgayVaoLam, TrangThai, NgayTao)
                VALUES (?, ?, ?, ?, ?, ?, ?, CAST(GETDATE() AS DATE), N'KichHoat', GETDATE())
            """, (user_id, full_name, email, phone, department, position, salary))
            
            conn.commit()
            
            # Get inserted ID
            cursor.execute("SELECT @@IDENTITY")
            employee_id = int(cursor.fetchone()[0])
            
            conn.close()
            return True, employee_id, "Tạo nhân viên thành công"
            
        except pyodbc.IntegrityError as e:
            return False, 0, f"Lỗi ràng buộc dữ liệu: {str(e)}"
        except Exception as e:
            return False, 0, f"Lỗi: {str(e)}"
    
    def update(self, employee_id: int, full_name: str, email: str, phone: str,
               department: str, position: str, salary: Decimal) -> Tuple[bool, str]:
        """
        UC05.5: Cập nhật thông tin nhân viên
        
        SQL Query:
        - UPDATE NhanVien SET: Cập nhật các fields
        - NgayCapNhat = GETDATE(): Track last modification
        - WHERE MaNhanVien = ?: Chỉ update 1 record
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE NhanVien
                SET HoTen = ?,
                    Email = ?,
                    SoDienThoai = ?,
                    PhongBan = ?,
                    ChucVu = ?,
                    MucLuong = ?,
                    NgayCapNhat = GETDATE()
                WHERE MaNhanVien = ?
            """, (full_name, email, phone, department, position, salary, employee_id))
            
            conn.commit()
            conn.close()
            return True, "Cập nhật thành công"
            
        except Exception as e:
            return False, f"Lỗi: {str(e)}"
    
    def update_status(self, employee_id: int, new_status: str) -> Tuple[bool, str]:
        """
        UC05.7: Cập nhật trạng thái nhân viên (KichHoat/BiKhoa)
        
        Tại sao riêng method này:
        - Status update là operation thường xuyên
        - Không cần validate các fields khác
        - Lightweight operation
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE NhanVien
                SET TrangThai = ?,
                    NgayCapNhat = GETDATE()
                WHERE MaNhanVien = ?
            """, (new_status, employee_id))
            
            conn.commit()
            conn.close()
            return True, f"Đã chuyển trạng thái thành {new_status}"
            
        except Exception as e:
            return False, f"Lỗi: {str(e)}"
    
    def search(self, keyword: str) -> List[Employee]:
        """
        UC05.3: Tìm kiếm nhân viên theo từ khóa
        
        SQL Query breakdown:
        - LIKE '%keyword%': Search pattern cho partial match
        - OR: Search multiple columns (HoTen, Email, PhongBan)
        - Case insensitive: SQL Server default
        
        Returns:
            List[Employee]: Kết quả tìm kiếm
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{keyword}%"
        cursor.execute("""
            SELECT 
                MaNhanVien, MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email,
                PhongBan, ChucVu, MucLuong, NgayVaoLam, MaQuanLy, TrangThai,
                NgayTao, NgayCapNhat
            FROM NhanVien
            WHERE (HoTen LIKE ? 
                   OR Email LIKE ? 
                   OR PhongBan LIKE ?)
              AND NgayXoa IS NULL
            ORDER BY MaNhanVien
        """, (search_pattern, search_pattern, search_pattern))
        
        employees = [self._map_to_employee(row) for row in cursor.fetchall()]
        conn.close()
        return employees
    
    def get_by_user_id(self, user_id: int) -> Optional[Employee]:
        """
        Helper: Lấy Employee theo MaNguoiDung (1-1 relationship)
        
        Dùng cho: Login flow - tìm Employee từ User
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                MaNhanVien, MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email,
                PhongBan, ChucVu, MucLuong, NgayVaoLam, MaQuanLy, TrangThai,
                NgayTao, NgayCapNhat
            FROM NhanVien
            WHERE MaNguoiDung = ? AND NgayXoa IS NULL
        """, (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return self._map_to_employee(row) if row else None
```

**Tổng kết EmployeeRepository:**
- 7 methods: get_all, get_by_id, create, update, update_status, search, get_by_user_id
- Tất cả SQL ở đây, Service KHÔNG biết SQL
- Error handling với try-catch
- Return types rõ ràng: Tuple[bool, int/str, str]

---

## 8. HƯỚNG DẪN CÀI ĐẶT

### 8.1. Yêu cầu hệ thống
- Windows 10/11
- Python 3.11+
- SQL Server 2019+
- ODBC Driver 18 for SQL Server

### 8.2. Cài đặt dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

**requirements.txt:**
```
customtkinter==5.2.1
pyodbc==5.0.1
matplotlib==3.8.0
reportlab==4.0.7
```

### 8.3. Setup Database
```bash
# 1. Tạo database
sqlcmd -S localhost -U SA -P "YourPassword" -i database_schema.sql

# 2. Insert sample data
sqlcmd -S localhost -U SA -P "YourPassword" -i sample_data.sql
```

### 8.4. Cấu hình kết nối
File: `bank_app_final.py` (dòng 50)
```python
self.connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=BankSystemOOP;"
    "UID=SA;"
    "PWD=YourPassword;"  # ← Thay đổi password
    "TrustServerCertificate=yes;"
)
```

### 8.5. Chạy ứng dụng
```bash
python bank_app_final.py
```

---

## 9. HƯỚNG DẪN SỬ DỤNG

### 9.1. Đăng nhập Credit Officer
```
TenDangNhap: officer1
MatKhau: officer1
Chọn vai trò: Nhân viên tín dụng
```

**Chức năng:**
1. Xem Dashboard → Thống kê + Biểu đồ
2. Tạo hồ sơ vay → Chọn KH, SP, nhập số tiền
3. Thẩm định → Chọn hồ sơ ChoXuLy → Bắt đầu
4. Phê duyệt → Chọn hồ sơ DangThamDinh → Phê duyệt
5. Giải ngân → Chọn hồ sơ DaDuyet → Giải ngân
6. Từ chối → Chọn hồ sơ → Nhập lý do

### 9.2. Đăng nhập Manager - User
```
TenDangNhap: manager1
MatKhau: manager1
Chọn vai trò: Manager - Quản lý người dùng
```

**Chức năng:**
1. Xem danh sách nhân viên
2. Thêm nhân viên → Điền form (có ChucVu, MucLuong)
3. Tìm kiếm → Nhập từ khóa
4. Xem chi tiết → Chọn nhân viên → Chi tiết
5. Chỉnh sửa → Chọn → Sửa thông tin
6. Khóa/Mở → Toggle status
7. Export PDF → Tải file PDF

### 9.3. Đăng nhập Manager - System
```
TenDangNhap: manager1
MatKhau: manager1
Chọn vai trò: Manager - Quản lý hệ thống ngoài
```

**Chức năng:**
1. Xem danh sách đối tác
2. Thêm đối tác → Nhập thông tin
3. Cập nhật trạng thái → Chọn KichHoat/KhongKichHoat/BaoTri
4. Xóa đối tác
5. Export PDF

---

## 10. ĐẶC ĐIỂM NỔI BẬT

### 10.1. Code Quality
✅ **Clean Code:**
- Comments đầy đủ
- Naming convention rõ ràng
- Tách function hợp lý
- Error handling toàn diện

✅ **SOLID Principles:**
- Single Responsibility: Mỗi class có 1 nhiệm vụ
- Dependency Inversion: Depend on abstractions (Repository)

✅ **Type Hints:**
```python
def add_employee(self, user_id: int, full_name: str, 
                 salary: float) -> Tuple[bool, str]:
```

### 10.2. Architecture
✅ **Separation of Concerns:**
- View không biết SQL
- Service không biết Tkinter
- Repository không biết business logic

✅ **Loose Coupling:**
- Dependency Injection
- Repository Pattern

✅ **High Cohesion:**
- Related methods trong cùng class

### 10.3. Database Design
✅ **Normalized (3NF):**
- No redundancy
- Referential integrity

✅ **Proper Constraints:**
- Primary Keys
- Foreign Keys (15+ ràng buộc)
- CHECK constraints
- UNIQUE constraints

✅ **Indexes:**
- Performance optimization
- Query speed improvement

### 10.4. UI/UX
✅ **Modern Design:**
- CustomTkinter dark theme
- Professional color scheme
- Responsive layout

✅ **User-Friendly:**
- Clear labels
- Error messages rõ ràng
- Success confirmations
- Loading indicators

✅ **Interactive:**
- Dynamic time update
- Real-time charts
- Smooth transitions

### 10.5. Bonus Features
✅ **Data Visualization:**
- Pie Chart với Matplotlib
- Bar Chart với value labels
- Dark theme matching

✅ **PDF Export:**
- Professional formatting
- Styled tables
- Auto-generated filename

✅ **Advanced Validation:**
- Email format check
- MucLuong > 0
- State transition validation

---

## 11. SCREENSHOTS

### 11.1. Credit Officer
- Dashboard với Pie Chart + Bar Chart
- Dialog tạo hồ sơ vay
- Danh sách hồ sơ theo trạng thái
- Workflow từ ChoXuLy → DaGiaiNgan

### 11.2. Manager User
- Danh sách nhân viên (có ChucVu + MucLuong)
- Dialog thêm nhân viên
- Dialog chỉnh sửa
- PDF export sample

### 11.3. Manager System
- Danh sách đối tác
- Dialog thêm đối tác
- Dialog cập nhật trạng thái
- PDF export sample

*(Screenshots được đính kèm trong folder /screenshots)*

---

## 12. KẾT LUẬN

### 12.1. Đã hoàn thành
✅ **Tất cả yêu cầu đề bài:**
- 3 đối tượng chính
- 15 Use Cases
- MVC + Repository Pattern
- Database design chuẩn
- GUI hiện đại

✅ **Bonus features:**
- Charts visualization
- PDF export
- Dynamic time
- Advanced validation

### 12.2. Điểm mạnh
- **Kiến trúc tốt:** Separation of concerns, loose coupling
- **Code quality cao:** Clean, maintainable, scalable
- **Database design chuẩn:** Normalized, indexed, constrained
- **UI/UX chuyên nghiệp:** Modern, user-friendly
- **Documentation đầy đủ:** README chi tiết, comments trong code

### 12.3. Hạn chế
- Chưa có unit tests
- Password plain text 
- Chưa handle concurrent access
- Chưa có logging system

### 12.4. Hướng phát triển
- Implement unit tests với pytest
- Add password hashing (bcrypt)
- Add transaction management
- Implement logging
- Deploy to cloud (Azure/AWS)
- Add REST API layer

---

## 13. TÀI LIỆU THAM KHẢO

1. **Design Patterns:**
   - "Design Patterns: Elements of Reusable Object-Oriented Software" - Gang of Four
   - "Clean Architecture" - Robert C. Martin

2. **Python Best Practices:**
   - PEP 8 - Python Style Guide
   - "Effective Python" - Brett Slatkin

3. **Database Design:**
   - "Database System Concepts" - Silberschatz
   - SQL Server Documentation - Microsoft

4. **GUI Development:**
   - CustomTkinter Documentation
   - Tkinter Documentation

---

**Document Version:** 2.0  
**Last Updated:** 06/01/2026  
**Status:** Completed & Submitted

---