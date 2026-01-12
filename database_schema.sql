-- ================================================
-- HỆ THỐNG QUẢN LÝ NGÂN HÀNG - SCHEMA CƠ SỞ DỮ LIỆU
-- Database: BankSystemOOP
-- ================================================

-- Xóa database nếu tồn tại và tạo mới
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'BankSystemOOP')
BEGIN
    ALTER DATABASE BankSystemOOP SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE BankSystemOOP;
END
GO

CREATE DATABASE BankSystemOOP;
GO

USE BankSystemOOP;
GO

PRINT '🏦 Đang tạo Schema Database BankSystemOOP...';
GO

-- ================================================
-- BẢNG 1: VaiTro (Roles)
-- ================================================
CREATE TABLE VaiTro (
    MaVaiTro INT PRIMARY KEY IDENTITY(1,1),
    TenVaiTro NVARCHAR(50) NOT NULL UNIQUE,
    MoTa NVARCHAR(255),
    NgayTao DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT CK_VaiTro_TenVaiTro CHECK (TenVaiTro IN (N'Admin', N'QuanLy', N'NhanVienTinDung', N'KhachHang'))
);

-- ================================================
-- BẢNG 2: NguoiDung (Users)
-- ================================================
CREATE TABLE NguoiDung (
    MaNguoiDung INT PRIMARY KEY IDENTITY(1,1),
    TenDangNhap NVARCHAR(50) NOT NULL UNIQUE,
    MatKhau NVARCHAR(100) NOT NULL,
    MaVaiTro INT NOT NULL,
    KichHoat BIT DEFAULT 1,
    DangNhapCuoi DATETIME,
    NgayTao DATETIME DEFAULT GETDATE(),
    NgayCapNhat DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_NguoiDung_VaiTro FOREIGN KEY (MaVaiTro) REFERENCES VaiTro(MaVaiTro)
);

-- ================================================
-- BẢNG 3: NhanVien (Employees)
-- ================================================
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
    NgayVaoLam DATE DEFAULT CAST(GETDATE() AS DATE),
    MaQuanLy INT,
    TrangThai NVARCHAR(20) DEFAULT N'KichHoat' CHECK (TrangThai IN (N'KichHoat', N'KhongKichHoat', N'BiKhoa')),
    NgayTao DATETIME DEFAULT GETDATE(),
    NgayCapNhat DATETIME DEFAULT GETDATE(),
    NgayXoa DATETIME NULL,
    
    -- Thông tin bổ sung
    DiaChi NVARCHAR(255),
    SoCMND NVARCHAR(20),
    QueQuan NVARCHAR(100),
    
    CONSTRAINT FK_NhanVien_NguoiDung FOREIGN KEY (MaNguoiDung) REFERENCES NguoiDung(MaNguoiDung),
    CONSTRAINT FK_NhanVien_QuanLy FOREIGN KEY (MaQuanLy) REFERENCES NhanVien(MaNhanVien)
);

-- ================================================
-- BẢNG 4: KhachHang (Customers)
-- ================================================
CREATE TABLE KhachHang (
    MaKhachHang INT PRIMARY KEY IDENTITY(1,1),
    HoTen NVARCHAR(100) NOT NULL,
    NgaySinh DATE,
    SoDienThoai NVARCHAR(15) UNIQUE,
    Email NVARCHAR(100) UNIQUE,
    DiaChi NVARCHAR(255),
    SoCMND NVARCHAR(20) UNIQUE,
    DiemTinDung INT DEFAULT 0,
    GioiTinh NVARCHAR(10),
    TrangThai NVARCHAR(20) DEFAULT N'KichHoat',
    NgayTao DATETIME DEFAULT GETDATE(),
    NgayCapNhat DATETIME DEFAULT GETDATE()
);

-- ================================================
-- BẢNG 5: SanPhamVay (LoanProducts)
-- ================================================
CREATE TABLE SanPhamVay (
    MaSanPham INT PRIMARY KEY IDENTITY(1,1),
    TenSanPham NVARCHAR(100) NOT NULL,
    LoaiSanPham NVARCHAR(50),
    SoTienToiThieu DECIMAL(18,2),
    SoTienToiDa DECIMAL(18,2),
    KyHanToiThieu INT,
    KyHanToiDa INT,
    LaiSuatToiThieu DECIMAL(5,2),
    LaiSuatToiDa DECIMAL(5,2),
    YeuCauTaiSan BIT DEFAULT 0,
    MoTa NVARCHAR(500),
    KichHoat BIT DEFAULT 1,
    NgayTao DATETIME DEFAULT GETDATE()
);

-- ================================================
-- BẢNG 6: HoSoVay (CreditApplications)
-- ================================================
CREATE TABLE HoSoVay (
    MaHoSo INT PRIMARY KEY IDENTITY(1,1),
    SoHoSo NVARCHAR(50) UNIQUE NOT NULL,
    MaKhachHang INT NOT NULL,
    MaSanPham INT NOT NULL,
    
    -- Thông tin khoản vay
    SoTienYeuCau DECIMAL(18,2) NOT NULL,
    KyHanYeuCau INT NOT NULL,
    MucDich NVARCHAR(255),
    
    -- Trạng thái
    TrangThai NVARCHAR(50) DEFAULT N'ChoXuLy' CHECK (TrangThai IN (
        N'ChoXuLy',        -- Pending
        N'DangThamDinh',   -- UnderReview
        N'DaDuyet',        -- Approved
        N'TuChoi',         -- Rejected
        N'DaGiaiNgan',     -- Disbursed
        N'HoanThanh',      -- Completed
        N'DaHuy'           -- Cancelled
    )),
    
    -- Người xử lý
    MaNhanVienPhuTrach INT,
    NguoiThamDinh INT,
    NguoiPheDuyet INT,
    
    -- Ngày tháng
    NgayNop DATETIME DEFAULT GETDATE(),
    NgayThamDinh DATETIME,
    NgayPheDuyet DATETIME,
    NgayGiaiNgan DATETIME,
    
    -- Ghi chú
    GhiChu NVARCHAR(500),
    LyDoTuChoi NVARCHAR(500),
    
    NgayTao DATETIME DEFAULT GETDATE(),
    NgayCapNhat DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_HoSo_KhachHang FOREIGN KEY (MaKhachHang) REFERENCES KhachHang(MaKhachHang),
    CONSTRAINT FK_HoSo_SanPham FOREIGN KEY (MaSanPham) REFERENCES SanPhamVay(MaSanPham),
    CONSTRAINT FK_HoSo_NhanVien FOREIGN KEY (MaNhanVienPhuTrach) REFERENCES NhanVien(MaNhanVien),
    CONSTRAINT FK_HoSo_NguoiThamDinh FOREIGN KEY (NguoiThamDinh) REFERENCES NhanVien(MaNhanVien),
    CONSTRAINT FK_HoSo_NguoiPheDuyet FOREIGN KEY (NguoiPheDuyet) REFERENCES NhanVien(MaNhanVien)
);

-- ================================================
-- BẢNG 7: ThamDinhTinDung (CreditAssessment)
-- ================================================
CREATE TABLE ThamDinhTinDung (
    MaThamDinh INT PRIMARY KEY IDENTITY(1,1),
    MaHoSo INT NOT NULL UNIQUE,
    
    -- Thông tin CIC
    DiemCIC INT,
    TrangThaiCIC NVARCHAR(50),
    NgayKiemTraCIC DATETIME,
    
    -- Thẩm định thu nhập
    ThuNhapHangThang DECIMAL(18,2),
    ThuNhapKhac DECIMAL(18,2),
    ChiPhiHangThang DECIMAL(18,2),
    TyLeNoTrenThuNhap DECIMAL(5,2),
    
    -- Thẩm định tài sản
    LoaiTaiSan NVARCHAR(100),
    GiaTriTaiSan DECIMAL(18,2),
    TyLeVayTrenGiaTri DECIMAL(5,2),
    
    -- Kết quả thẩm định
    MucDoRuiRo NVARCHAR(20) CHECK (MucDoRuiRo IN (N'Thap', N'TrungBinh', N'Cao', N'RatCao')),
    SoTienDeXuat DECIMAL(18,2),
    LaiSuatDeXuat DECIMAL(5,2),
    GhiChuThamDinh NVARCHAR(1000),
    
    NguoiThamDinh INT,
    NgayThamDinh DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_ThamDinh_HoSo FOREIGN KEY (MaHoSo) REFERENCES HoSoVay(MaHoSo),
    CONSTRAINT FK_ThamDinh_NhanVien FOREIGN KEY (NguoiThamDinh) REFERENCES NhanVien(MaNhanVien)
);

-- ================================================
-- BẢNG 8: KhoanVay (Loans)
-- ================================================
CREATE TABLE KhoanVay (
    MaKhoanVay INT PRIMARY KEY IDENTITY(1,1),
    SoKhoanVay NVARCHAR(50) UNIQUE NOT NULL,
    MaHoSo INT NOT NULL UNIQUE,
    MaKhachHang INT NOT NULL,
    
    -- Thông tin khoản vay
    SoTienGoc DECIMAL(18,2) NOT NULL,
    LaiSuat DECIMAL(5,2) NOT NULL,
    KyHan INT NOT NULL,
    TraHangThang DECIMAL(18,2),
    
    -- Số dư
    DuNoGoc DECIMAL(18,2),
    LaiPhaiTra DECIMAL(18,2) DEFAULT 0,
    
    -- Trạng thái
    TrangThai NVARCHAR(50) DEFAULT N'DangHoatDong' CHECK (TrangThai IN (
        N'DangHoatDong',   -- Active
        N'QuaHan',         -- Overdue
        N'DaTatToan',      -- PaidOff
        N'XoaNo'           -- WrittenOff
    )),
    
    -- Ngày tháng
    NgayGiaiNgan DATE NOT NULL,
    NgayTraDauTien DATE,
    NgayDaoHan DATE,
    
    -- Giải ngân
    NguoiGiaiNgan INT,
    PhuongThucGiaiNgan NVARCHAR(50),
    
    NgayTao DATETIME DEFAULT GETDATE(),
    NgayCapNhat DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_KhoanVay_HoSo FOREIGN KEY (MaHoSo) REFERENCES HoSoVay(MaHoSo),
    CONSTRAINT FK_KhoanVay_KhachHang FOREIGN KEY (MaKhachHang) REFERENCES KhachHang(MaKhachHang),
    CONSTRAINT FK_KhoanVay_NhanVien FOREIGN KEY (NguoiGiaiNgan) REFERENCES NhanVien(MaNhanVien)
);

-- ================================================
-- BẢNG 9: LichTraNo (PaymentSchedule)
-- ================================================
CREATE TABLE LichTraNo (
    MaLichTra INT PRIMARY KEY IDENTITY(1,1),
    MaKhoanVay INT NOT NULL,
    SoKyTra INT NOT NULL,
    
    -- Số tiền
    TienGoc DECIMAL(18,2),
    TienLai DECIMAL(18,2),
    TongTien DECIMAL(18,2),
    
    -- Ngày
    NgayDenHan DATE NOT NULL,
    NgayThucTra DATE,
    
    -- Trạng thái
    TrangThai NVARCHAR(20) DEFAULT N'ChuaDenHan' CHECK (TrangThai IN (
        N'ChuaDenHan',  -- Pending
        N'DaTra',       -- Paid
        N'QuaHan',      -- Overdue
        N'TraMotPhan'   -- Partial
    )),
    
    SoTienDaTra DECIMAL(18,2) DEFAULT 0,
    
    NgayTao DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_LichTra_KhoanVay FOREIGN KEY (MaKhoanVay) REFERENCES KhoanVay(MaKhoanVay)
);

-- ================================================
-- BẢNG 10: ThanhToan (Payments)
-- ================================================
CREATE TABLE ThanhToan (
    MaThanhToan INT PRIMARY KEY IDENTITY(1,1),
    MaKhoanVay INT NOT NULL,
    MaLichTra INT,
    
    SoTienThanhToan DECIMAL(18,2) NOT NULL,
    NgayThanhToan DATETIME DEFAULT GETDATE(),
    PhuongThucThanhToan NVARCHAR(50),
    
    GocDaTra DECIMAL(18,2) DEFAULT 0,
    LaiDaTra DECIMAL(18,2) DEFAULT 0,
    PhiPhat DECIMAL(18,2) DEFAULT 0,
    
    MaGiaoDich NVARCHAR(100),
    GhiChu NVARCHAR(255),
    
    NguoiGhiNhan INT,
    NgayTao DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_ThanhToan_KhoanVay FOREIGN KEY (MaKhoanVay) REFERENCES KhoanVay(MaKhoanVay),
    CONSTRAINT FK_ThanhToan_LichTra FOREIGN KEY (MaLichTra) REFERENCES LichTraNo(MaLichTra),
    CONSTRAINT FK_ThanhToan_NhanVien FOREIGN KEY (NguoiGhiNhan) REFERENCES NhanVien(MaNhanVien)
);

-- ================================================
-- BẢNG 11: HeThongNgoai (ExternalSystems)
-- ================================================
CREATE TABLE HeThongNgoai (
    MaHeThong INT PRIMARY KEY IDENTITY(1,1),
    TenHeThong NVARCHAR(100) NOT NULL,
    LoaiHeThong NVARCHAR(50) CHECK (LoaiHeThong IN ('ThanhToan', 'KiemTraTinDung', 'TyGia', 'Khac')),
    DiaChiAPI NVARCHAR(255),
    KhoaAPI NVARCHAR(255),
    TrangThai NVARCHAR(20) DEFAULT N'KichHoat' CHECK (TrangThai IN (N'KichHoat', N'KhongKichHoat', N'BaoTri')),
    MoTa NVARCHAR(500),
    KiemTraCuoi DATETIME,
    NgayTao DATETIME DEFAULT GETDATE(),
    NgayCapNhat DATETIME DEFAULT GETDATE()
);

-- ================================================
-- BẢNG 12: NhatKyHeThong (AuditLog)
-- ================================================
CREATE TABLE NhatKyHeThong (
    MaNhatKy INT PRIMARY KEY IDENTITY(1,1),
    MaNguoiDung INT,
    HanhDong NVARCHAR(100),
    TenBang NVARCHAR(50),
    MaBanGhi INT,
    GiaTriCu NVARCHAR(MAX),
    GiaTriMoi NVARCHAR(MAX),
    DiaChiIP NVARCHAR(50),
    NgayTao DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_NhatKy_NguoiDung FOREIGN KEY (MaNguoiDung) REFERENCES NguoiDung(MaNguoiDung)
);

-- ================================================
-- CHỈ MỤC (INDEXES) để tối ưu hiệu suất
-- ================================================
CREATE INDEX IX_NguoiDung_TenDangNhap ON NguoiDung(TenDangNhap);
CREATE INDEX IX_NhanVien_TrangThai ON NhanVien(TrangThai);
CREATE INDEX IX_KhachHang_SoCMND ON KhachHang(SoCMND);
CREATE INDEX IX_HoSo_TrangThai ON HoSoVay(TrangThai);
CREATE INDEX IX_HoSo_KhachHang ON HoSoVay(MaKhachHang);
CREATE INDEX IX_KhoanVay_KhachHang ON KhoanVay(MaKhachHang);
CREATE INDEX IX_KhoanVay_TrangThai ON KhoanVay(TrangThai);
CREATE INDEX IX_LichTra_NgayDenHan ON LichTraNo(NgayDenHan);
CREATE INDEX IX_LichTra_TrangThai ON LichTraNo(TrangThai);

GO

PRINT '✅ Tạo schema database thành công!';
PRINT '';
PRINT '📊 Các bảng đã tạo:';
PRINT '  1. VaiTro (Roles)';
PRINT '  2. NguoiDung (Users)';
PRINT '  3. NhanVien (Employees)';
PRINT '  4. KhachHang (Customers)';
PRINT '  5. SanPhamVay (LoanProducts)';
PRINT '  6. HoSoVay (CreditApplications)';
PRINT '  7. ThamDinhTinDung (CreditAssessment)';
PRINT '  8. KhoanVay (Loans)';
PRINT '  9. LichTraNo (PaymentSchedule)';
PRINT ' 10. ThanhToan (Payments)';
PRINT ' 11. HeThongNgoai (ExternalSystems)';
PRINT ' 12. NhatKyHeThong (AuditLog)';
PRINT '';
PRINT '✅ Sẵn sàng chèn dữ liệu!';
GO