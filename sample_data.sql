-- ================================================
-- INSERT SAMPLE DATA - BankSystemOOP
-- ================================================

USE BankSystemOOP;
GO

PRINT '📝 Đang chèn dữ liệu mẫu...';
GO

-- ================================================
-- 1. INSERT VAI TRÒ
-- ================================================
PRINT 'Bước 1: Chèn Vai trò...';

INSERT INTO VaiTro (TenVaiTro, MoTa) VALUES
(N'Admin', N'Quản trị hệ thống'),
(N'QuanLy', N'Quản lý'),
(N'NhanVienTinDung', N'Nhân viên tín dụng'),
(N'KhachHang', N'Khách hàng');

PRINT '✅ Vai trò đã chèn';
GO

-- ================================================
-- 2. INSERT NGƯỜI DÙNG (Plain text passwords)
-- ================================================
PRINT 'Bước 2: Chèn Người dùng...';

DECLARE @AdminRole INT = (SELECT MaVaiTro FROM VaiTro WHERE TenVaiTro = 'Admin');
DECLARE @ManagerRole INT = (SELECT MaVaiTro FROM VaiTro WHERE TenVaiTro = N'QuanLy');
DECLARE @OfficerRole INT = (SELECT MaVaiTro FROM VaiTro WHERE TenVaiTro = N'NhanVienTinDung');

-- Admins (2 users)
INSERT INTO NguoiDung (TenDangNhap, MatKhau, MaVaiTro, KichHoat) VALUES
('admin', 'admin', @AdminRole, 1),
('admin2', 'admin2', @AdminRole, 1);

-- Managers (5 users)
INSERT INTO NguoiDung (TenDangNhap, MatKhau, MaVaiTro, KichHoat) VALUES
('manager1', 'manager1', @ManagerRole, 1),
('manager2', 'manager2', @ManagerRole, 1),
('manager3', 'manager3', @ManagerRole, 1),
('manager4', 'manager4', @ManagerRole, 1),
('manager5', 'manager5', @ManagerRole, 1);

-- Credit Officers (10 users)
INSERT INTO NguoiDung (TenDangNhap, MatKhau, MaVaiTro, KichHoat) VALUES
('officer1', 'officer1', @OfficerRole, 1),
('officer2', 'officer2', @OfficerRole, 1),
('officer3', 'officer3', @OfficerRole, 1),
('officer4', 'officer4', @OfficerRole, 1),
('officer5', 'officer5', @OfficerRole, 1),
('officer6', 'officer6', @OfficerRole, 1),
('officer7', 'officer7', @OfficerRole, 1),
('officer8', 'officer8', @OfficerRole, 1),
('officer9', 'officer9', @OfficerRole, 1),
('officer10', 'officer10', @OfficerRole, 1);

PRINT '✅ Người dùng đã chèn (17 tổng)';
GO

-- ================================================
-- 3. INSERT NHÂN VIÊN
-- ================================================
PRINT 'Bước 3: Chèn Nhân viên...';

-- Admins
INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Nguyễn Văn Admin', '1980-01-15', '0900000001', 'admin@bank.vn', N'Quản lý', N'Giám đốc', 100000000, N'KichHoat', N'123 Láng Hạ, HN', '001080000001', N'Hà Nội'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'admin';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Trần Thị Admin 2', '1982-05-20', '0900000002', 'admin2@bank.vn', N'Quản lý', N'Phó Giám đốc', 90000000, N'KichHoat', N'456 Giải Phóng, HN', '001082000002', N'Hải Phòng'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'admin2';

-- Managers
INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Lê Văn Manager 1', '1985-03-25', '0901111111', 'manager1@bank.vn', N'Quản lý', N'Trưởng phòng Tín dụng', 60000000, N'KichHoat', N'12 Hoàng Hoa Thám, HN', '001085012345', N'Nam Định'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'manager1';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Phạm Thị Manager 2', '1987-07-14', '0902222222', 'manager2@bank.vn', N'Quản lý', N'Trưởng phòng Nhân sự', 58000000, N'KichHoat', N'34 Láng Hạ, HN', '001087023456', N'Thái Bình'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'manager2';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Hoàng Văn Manager 3', '1986-09-30', '0903333333', 'manager3@bank.vn', N'Quản lý', N'Trưởng phòng Vận hành', 59000000, N'KichHoat', N'56 Nguyễn Trãi, HN', '001086034567', N'Ninh Bình'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'manager3';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Vũ Thị Manager 4', '1988-12-05', '0904444444', 'manager4@bank.vn', N'Quản lý', N'Trưởng phòng Rủi ro', 57000000, N'KichHoat', N'78 Trần Duy Hưng, HN', '001088045678', N'Hưng Yên'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'manager4';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Đặng Văn Manager 5', '1989-04-18', '0905555555', 'manager5@bank.vn', N'Quản lý', N'Trưởng phòng IT', 56000000, N'KichHoat', N'90 Lê Văn Lương, HN', '001089056789', N'Vĩnh Phúc'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'manager5';

-- Credit Officers
INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Nguyễn Văn Officer 1', '1991-02-14', '0911111111', 'officer1@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng cao cấp', 35000000, N'KichHoat', N'101 Kim Mã, HN', '001091111111', N'Phú Thọ'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'officer1';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Trần Thị Officer 2', '1992-05-20', '0922222222', 'officer2@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 30000000, N'KichHoat', N'202 Láng Hạ, HN', '001092222222', N'Thanh Hóa'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'officer2';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Lê Văn Officer 3', '1993-08-25', '0933333333', 'officer3@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 28000000, N'KichHoat', N'303 Giải Phóng, HN', '001093333333', N'Nghệ An'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'officer3';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Phạm Thị Officer 4', '1994-11-30', '0944444444', 'officer4@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 27000000, N'KichHoat', N'404 Trần Hưng Đạo, HN', '001094444444', N'Hà Tĩnh'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'officer4';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Hoàng Văn Officer 5', '1995-03-15', '0955555555', 'officer5@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng junior', 25000000, N'KichHoat', N'505 Cầu Giấy, HN', '001095555555', N'Quảng Bình'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'officer5';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Vũ Thị Officer 6', '1991-07-22', '0966666666', 'officer6@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 29000000, N'KichHoat', N'606 Nguyễn Trãi, HN', '001091666666', N'Quảng Trị'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'officer6';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Đặng Văn Officer 7', '1992-10-18', '0977777777', 'officer7@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 28500000, N'KichHoat', N'707 Lê Văn Lương, HN', '001092777777', N'Huế'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'officer7';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Bùi Thị Officer 8', '1993-12-05', '0988888888', 'officer8@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 27500000, N'KichHoat', N'808 Trần Duy Hưng, HN', '001093888888', N'Đà Nẵng'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'officer8';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Ngô Văn Officer 9', '1994-04-28', '0999999999', 'officer9@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 26500000, N'KichHoat', N'909 Tô Hiệu, HN', '001094999999', N'Quảng Nam'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'officer9';

INSERT INTO NhanVien (MaNguoiDung, HoTen, NgaySinh, SoDienThoai, Email, PhongBan, ChucVu, MucLuong, TrangThai, DiaChi, SoCMND, QueQuan)
SELECT ND.MaNguoiDung, N'Mai Thị Officer 10', '1995-06-10', '0910101010', 'officer10@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng junior', 25500000, N'KichHoat', N'010 Nguyễn Xiển, HN', '001095101010', N'Quảng Ngãi'
FROM NguoiDung ND WHERE ND.TenDangNhap = 'officer10';

PRINT '✅ Nhân viên đã chèn (17 tổng)';
GO

-- ================================================
-- 4. INSERT KHÁCH HÀNG
-- ================================================
PRINT 'Bước 4: Chèn Khách hàng...';

INSERT INTO KhachHang (HoTen, NgaySinh, SoDienThoai, Email, DiaChi, SoCMND, DiemTinDung, GioiTinh, TrangThai) VALUES
(N'Nguyễn Văn Khách 1', '1988-01-15', '0901234567', 'khach1@email.com', N'12 Lê Lợi, Q1, TP.HCM', '079088001001', 750, N'Nam', N'KichHoat'),
(N'Trần Thị Khách 2', '1990-05-20', '0902345678', 'khach2@email.com', N'34 Trần Hưng Đạo, Q5, TP.HCM', '079090002002', 720, N'Nữ', N'KichHoat'),
(N'Lê Văn Khách 3', '1985-03-10', '0903456789', 'khach3@email.com', N'56 Nguyễn Huệ, Q1, TP.HCM', '079085003003', 780, N'Nam', N'KichHoat'),
(N'Phạm Thị Khách 4', '1992-07-25', '0904567890', 'khach4@email.com', N'78 Hai Bà Trưng, Q3, TP.HCM', '079092004004', 690, N'Nữ', N'KichHoat'),
(N'Hoàng Văn Khách 5', '1987-11-30', '0905678901', 'khach5@email.com', N'90 Điện Biên Phủ, Q3, TP.HCM', '079087005005', 710, N'Nam', N'KichHoat'),
(N'Vũ Thị Khách 6', '1995-02-14', '0906789012', 'khach6@email.com', N'123 Võ Văn Tần, Q3, TP.HCM', '079095006006', 680, N'Nữ', N'KichHoat'),
(N'Đặng Văn Khách 7', '1989-06-18', '0907890123', 'khach7@email.com', N'234 Phan Xích Long, PN, TP.HCM', '079089007007', 730, N'Nam', N'KichHoat'),
(N'Bùi Thị Khách 8', '1991-09-22', '0908901234', 'khach8@email.com', N'345 Cách Mạng T8, Q10, TP.HCM', '079091008008', 700, N'Nữ', N'KichHoat'),
(N'Ngô Văn Khách 9', '1986-12-05', '0909012345', 'khach9@email.com', N'456 Lý Thường Kiệt, Q10, TP.HCM', '079086009009', 740, N'Nam', N'KichHoat'),
(N'Mai Thị Khách 10', '1994-04-28', '0910123456', 'khach10@email.com', N'567 3 Tháng 2, Q10, TP.HCM', '079094010010', 760, N'Nữ', N'KichHoat'),
(N'Trương Văn Khách 11', '1993-08-15', '0911234567', 'khach11@email.com', N'678 Nguyễn Văn Cừ, Q5, TP.HCM', '079093011011', 705, N'Nam', N'KichHoat'),
(N'Đinh Thị Khách 12', '1996-03-20', '0912345678', 'khach12@email.com', N'789 Lê Hồng Phong, Q10, TP.HCM', '079096012012', 725, N'Nữ', N'KichHoat'),
(N'Phan Văn Khách 13', '1984-11-10', '0913456789', 'khach13@email.com', N'890 Trường Chinh, TB, TP.HCM', '079084013013', 745, N'Nam', N'KichHoat'),
(N'Lý Thị Khách 14', '1991-07-05', '0914567890', 'khach14@email.com', N'901 Xô Viết Nghệ Tĩnh, BT, TP.HCM', '079091014014', 715, N'Nữ', N'KichHoat'),
(N'Võ Văn Khách 15', '1989-12-25', '0915678901', 'khach15@email.com', N'012 Hoàng Văn Thụ, TB, TP.HCM', '079089015015', 735, N'Nam', N'KichHoat');

PRINT '✅ Khách hàng đã chèn (15 tổng)';
GO

-- ================================================
-- 5. INSERT SẢN PHẨM VAY
-- ================================================
PRINT 'Bước 5: Chèn Sản phẩm vay...';

INSERT INTO SanPhamVay (TenSanPham, LoaiSanPham, SoTienToiThieu, SoTienToiDa, KyHanToiThieu, KyHanToiDa, LaiSuatToiThieu, LaiSuatToiDa, YeuCauTaiSan, MoTa, KichHoat) VALUES
(N'Vay tiêu dùng cá nhân', N'Cá nhân', 10000000, 500000000, 12, 60, 7.5, 12.0, 0, N'Vay tiêu dùng không cần tài sản đảm bảo', 1),
(N'Vay mua nhà', N'Thế chấp', 100000000, 5000000000, 60, 240, 6.5, 9.5, 1, N'Vay mua nhà với thế chấp bất động sản', 1),
(N'Vay mua ô tô', N'Thế chấp', 50000000, 2000000000, 12, 84, 7.0, 10.0, 1, N'Vay mua ô tô với thế chấp xe', 1),
(N'Vay kinh doanh SME', N'Doanh nghiệp', 50000000, 10000000000, 12, 120, 8.0, 13.0, 1, N'Vay cho doanh nghiệp SME', 1),
(N'Vay tín chấp lương', N'Cá nhân', 5000000, 200000000, 6, 36, 8.5, 14.0, 0, N'Vay tín chấp dựa trên lương', 1);

PRINT '✅ Sản phẩm vay đã chèn (5 tổng)';
GO

-- ================================================
-- 6. INSERT HỒ SƠ VAY
-- ================================================
PRINT 'Bước 6: Chèn Hồ sơ vay...';

DECLARE @Cust1 INT, @Cust2 INT, @Cust3 INT, @Cust4 INT, @Cust5 INT;
DECLARE @Cust6 INT, @Cust7 INT, @Cust8 INT, @Cust9 INT, @Cust10 INT;
DECLARE @Prod1 INT, @Prod2 INT, @Prod3 INT;
DECLARE @Off1 INT, @Off2 INT, @Off3 INT;

SELECT @Cust1 = MIN(MaKhachHang) FROM KhachHang;
SET @Cust2 = @Cust1 + 1; SET @Cust3 = @Cust1 + 2; SET @Cust4 = @Cust1 + 3; SET @Cust5 = @Cust1 + 4;
SET @Cust6 = @Cust1 + 5; SET @Cust7 = @Cust1 + 6; SET @Cust8 = @Cust1 + 7; SET @Cust9 = @Cust1 + 8; SET @Cust10 = @Cust1 + 9;

SELECT @Prod1 = MIN(MaSanPham) FROM SanPhamVay;
SET @Prod2 = @Prod1 + 1; SET @Prod3 = @Prod1 + 2;

SELECT @Off1 = MIN(MaNhanVien) FROM NhanVien WHERE PhongBan = N'Tín dụng';
SET @Off2 = @Off1 + 1; SET @Off3 = @Off1 + 2;

-- HỒ SƠ CHỜ XỬ LÝ (5)
INSERT INTO HoSoVay (SoHoSo, MaKhachHang, MaSanPham, SoTienYeuCau, KyHanYeuCau, MucDich, TrangThai, MaNhanVienPhuTrach, NgayNop) VALUES
('APP-2026-001', @Cust1, @Prod1, 200000000, 24, N'Vay tiêu dùng mua sắm', N'ChoXuLy', @Off1, GETDATE()),
('APP-2026-002', @Cust2, @Prod2, 1500000000, 120, N'Vay mua nhà', N'ChoXuLy', @Off2, DATEADD(day, -1, GETDATE())),
('APP-2026-003', @Cust3, @Prod3, 500000000, 60, N'Vay mua xe ô tô', N'ChoXuLy', @Off1, DATEADD(day, -2, GETDATE())),
('APP-2026-004', @Cust4, @Prod1, 100000000, 12, N'Vay du lịch', N'ChoXuLy', @Off3, DATEADD(day, -3, GETDATE())),
('APP-2026-005', @Cust5, @Prod1, 150000000, 18, N'Vay sửa nhà', N'ChoXuLy', @Off2, DATEADD(day, -4, GETDATE()));

-- ĐANG THẨM ĐỊNH (3)
INSERT INTO HoSoVay (SoHoSo, MaKhachHang, MaSanPham, SoTienYeuCau, KyHanYeuCau, MucDich, TrangThai, MaNhanVienPhuTrach, NguoiThamDinh, NgayNop, NgayThamDinh) VALUES
('APP-2026-006', @Cust6, @Prod2, 2000000000, 180, N'Vay mua căn hộ', N'DangThamDinh', @Off1, @Off1, DATEADD(day, -7, GETDATE()), DATEADD(day, -5, GETDATE())),
('APP-2026-007', @Cust7, @Prod3, 800000000, 72, N'Vay mua xe Mercedes', N'DangThamDinh', @Off2, @Off2, DATEADD(day, -8, GETDATE()), DATEADD(day, -6, GETDATE())),
('APP-2026-008', @Cust8, @Prod1, 300000000, 36, N'Vay kinh doanh nhỏ', N'DangThamDinh', @Off3, @Off3, DATEADD(day, -9, GETDATE()), DATEADD(day, -7, GETDATE()));

-- ĐÃ DUYỆT (2)
INSERT INTO HoSoVay (SoHoSo, MaKhachHang, MaSanPham, SoTienYeuCau, KyHanYeuCau, MucDich, TrangThai, MaNhanVienPhuTrach, NguoiThamDinh, NguoiPheDuyet, NgayNop, NgayThamDinh, NgayPheDuyet) VALUES
('APP-2026-009', @Cust9, @Prod1, 180000000, 24, N'Vay tín dụng cá nhân', N'DaDuyet', @Off1, @Off1, @Off1, DATEADD(day, -15, GETDATE()), DATEADD(day, -12, GETDATE()), DATEADD(day, -10, GETDATE())),
('APP-2026-010', @Cust10, @Prod2, 3000000000, 240, N'Vay mua biệt thự', N'DaDuyet', @Off2, @Off2, @Off2, DATEADD(day, -20, GETDATE()), DATEADD(day, -17, GETDATE()), DATEADD(day, -15, GETDATE()));

PRINT '✅ Hồ sơ vay đã chèn (10 tổng)';
GO

-- ================================================
-- 7. INSERT HỆ THỐNG NGOÀI
-- ================================================
PRINT 'Bước 7: Chèn Hệ thống ngoài...';

INSERT INTO HeThongNgoai (TenHeThong, LoaiHeThong, DiaChiAPI, KhoaAPI, TrangThai, MoTa) VALUES
(N'VNPay Payment Gateway', 'ThanhToan', 'https://api.vnpay.vn/v2', 'VNPAY_KEY_2026', N'KichHoat', N'Cổng thanh toán VNPay'),
(N'CIC Credit Bureau', 'KiemTraTinDung', 'https://api.cic.org.vn/check', 'CIC_API_2026', N'KichHoat', N'Trung tâm Thông tin Tín dụng'),
(N'SBV Exchange Rate', 'TyGia', 'https://api.sbv.gov.vn/rates', 'SBV_KEY_2026', N'KichHoat', N'Tỷ giá Ngân hàng Nhà nước');

PRINT '✅ Hệ thống ngoài đã chèn (3 tổng)';
GO

-- ================================================
-- XÁC NHẬN
-- ================================================
PRINT '';
PRINT '==============================================';
PRINT '✅ HOÀN TẤT CHÈN DỮ LIỆU!';
PRINT '==============================================';
PRINT '';

SELECT N'VaiTro' AS [Bảng], COUNT(*) AS [Số lượng] FROM VaiTro
UNION ALL SELECT N'NguoiDung', COUNT(*) FROM NguoiDung
UNION ALL SELECT N'NhanVien', COUNT(*) FROM NhanVien
UNION ALL SELECT N'KhachHang', COUNT(*) FROM KhachHang
UNION ALL SELECT N'SanPhamVay', COUNT(*) FROM SanPhamVay
UNION ALL SELECT N'HoSoVay', COUNT(*) FROM HoSoVay
UNION ALL SELECT N'HeThongNgoai', COUNT(*) FROM HeThongNgoai;

PRINT '';
PRINT '📝 THÔNG TIN ĐĂNG NHẬP:';
PRINT '  Admin:    admin/admin, admin2/admin2';
PRINT '  Manager:  manager1/manager1 ... manager5/manager5';
PRINT '  Officer:  officer1/officer1 ... officer10/officer10';
PRINT '';
PRINT '✅ Cơ sở dữ liệu sẵn sàng sử dụng!';
GO