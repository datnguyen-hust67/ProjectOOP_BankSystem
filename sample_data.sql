-- ================================================
-- INSERT SAMPLE DATA - BankSystemOOP
-- ================================================

USE BankSystemOOP;
GO

PRINT '📝 Inserting sample data...';
GO

-- ================================================
-- 1. INSERT ROLES
-- ================================================
PRINT 'Step 1: Inserting Roles...';

INSERT INTO Roles (RoleName, Description) VALUES
(N'Admin', N'Quản trị hệ thống'),
(N'Manager', N'Quản lý'),
(N'CreditOfficer', N'Nhân viên tín dụng'),
(N'Customer', N'Khách hàng');

PRINT '✅ Roles inserted';
GO

-- ================================================
-- 2. INSERT USERS (Plain text passwords)
-- ================================================
PRINT 'Step 2: Inserting Users...';

DECLARE @AdminRole INT = (SELECT RoleID FROM Roles WHERE RoleName = 'Admin');
DECLARE @ManagerRole INT = (SELECT RoleID FROM Roles WHERE RoleName = 'Manager');
DECLARE @OfficerRole INT = (SELECT RoleID FROM Roles WHERE RoleName = 'CreditOfficer');

-- Admins (2 users)
INSERT INTO Users (Username, PasswordPlainText, RoleID, IsActive) VALUES
('admin', 'admin', @AdminRole, 1),
('admin2', 'admin2', @AdminRole, 1);

-- Managers (5 users)
INSERT INTO Users (Username, PasswordPlainText, RoleID, IsActive) VALUES
('manager1', 'manager1', @ManagerRole, 1),
('manager2', 'manager2', @ManagerRole, 1),
('manager3', 'manager3', @ManagerRole, 1),
('manager4', 'manager4', @ManagerRole, 1),
('manager5', 'manager5', @ManagerRole, 1);

-- Credit Officers (10 users)
INSERT INTO Users (Username, PasswordPlainText, RoleID, IsActive) VALUES
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

PRINT '✅ Users inserted (17 total)';
GO

-- ================================================
-- 3. INSERT EMPLOYEES
-- ================================================
PRINT 'Step 3: Inserting Employees...';

-- Admins
INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Nguyễn Văn Admin', '1980-01-15', '0900000001', 'admin@bank.vn', N'Quản lý', N'Giám đốc', 100000000, 'Active', N'123 Láng Hạ, HN', '001080000001', N'Hà Nội'
FROM Users U WHERE U.Username = 'admin';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Trần Thị Admin 2', '1982-05-20', '0900000002', 'admin2@bank.vn', N'Quản lý', N'Phó Giám đốc', 90000000, 'Active', N'456 Giải Phóng, HN', '001082000002', N'Hải Phòng'
FROM Users U WHERE U.Username = 'admin2';

-- Managers
INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Lê Văn Manager 1', '1985-03-25', '0901111111', 'manager1@bank.vn', N'Quản lý', N'Trưởng phòng Tín dụng', 60000000, 'Active', N'12 Hoàng Hoa Thám, HN', '001085012345', N'Nam Định'
FROM Users U WHERE U.Username = 'manager1';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Phạm Thị Manager 2', '1987-07-14', '0902222222', 'manager2@bank.vn', N'Quản lý', N'Trưởng phòng Nhân sự', 58000000, 'Active', N'34 Láng Hạ, HN', '001087023456', N'Thái Bình'
FROM Users U WHERE U.Username = 'manager2';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Hoàng Văn Manager 3', '1986-09-30', '0903333333', 'manager3@bank.vn', N'Quản lý', N'Trưởng phòng Vận hành', 59000000, 'Active', N'56 Nguyễn Trãi, HN', '001086034567', N'Ninh Bình'
FROM Users U WHERE U.Username = 'manager3';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Vũ Thị Manager 4', '1988-12-05', '0904444444', 'manager4@bank.vn', N'Quản lý', N'Trưởng phòng Rủi ro', 57000000, 'Active', N'78 Trần Duy Hưng, HN', '001088045678', N'Hưng Yên'
FROM Users U WHERE U.Username = 'manager4';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Đặng Văn Manager 5', '1989-04-18', '0905555555', 'manager5@bank.vn', N'Quản lý', N'Trưởng phòng IT', 56000000, 'Active', N'90 Lê Văn Lương, HN', '001089056789', N'Vĩnh Phúc'
FROM Users U WHERE U.Username = 'manager5';

-- Credit Officers
INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Nguyễn Văn Officer 1', '1991-02-14', '0911111111', 'officer1@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng cao cấp', 35000000, 'Active', N'101 Kim Mã, HN', '001091111111', N'Phú Thọ'
FROM Users U WHERE U.Username = 'officer1';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Trần Thị Officer 2', '1992-05-20', '0922222222', 'officer2@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 30000000, 'Active', N'202 Láng Hạ, HN', '001092222222', N'Thanh Hóa'
FROM Users U WHERE U.Username = 'officer2';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Lê Văn Officer 3', '1993-08-25', '0933333333', 'officer3@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 28000000, 'Active', N'303 Giải Phóng, HN', '001093333333', N'Nghệ An'
FROM Users U WHERE U.Username = 'officer3';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Phạm Thị Officer 4', '1994-11-30', '0944444444', 'officer4@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 27000000, 'Active', N'404 Trần Hưng Đạo, HN', '001094444444', N'Hà Tĩnh'
FROM Users U WHERE U.Username = 'officer4';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Hoàng Văn Officer 5', '1995-03-15', '0955555555', 'officer5@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng junior', 25000000, 'Active', N'505 Cầu Giấy, HN', '001095555555', N'Quảng Bình'
FROM Users U WHERE U.Username = 'officer5';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Vũ Thị Officer 6', '1991-07-22', '0966666666', 'officer6@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 29000000, 'Active', N'606 Nguyễn Trãi, HN', '001091666666', N'Quảng Trị'
FROM Users U WHERE U.Username = 'officer6';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Đặng Văn Officer 7', '1992-10-18', '0977777777', 'officer7@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 28500000, 'Active', N'707 Lê Văn Lương, HN', '001092777777', N'Huế'
FROM Users U WHERE U.Username = 'officer7';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Bùi Thị Officer 8', '1993-12-05', '0988888888', 'officer8@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 27500000, 'Active', N'808 Trần Duy Hưng, HN', '001093888888', N'Đà Nẵng'
FROM Users U WHERE U.Username = 'officer8';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Ngô Văn Officer 9', '1994-04-28', '0999999999', 'officer9@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng', 26500000, 'Active', N'909 Tô Hiệu, HN', '001094999999', N'Quảng Nam'
FROM Users U WHERE U.Username = 'officer9';

INSERT INTO Employees (UserID, FullName, DateOfBirth, Phone, Email, Department, Position, Salary, Status, Address, IdentityNumber, Hometown)
SELECT U.UserID, N'Mai Thị Officer 10', '1995-06-10', '0910101010', 'officer10@bank.vn', N'Tín dụng', N'Chuyên viên Tín dụng junior', 25500000, 'Active', N'010 Nguyễn Xiển, HN', '001095101010', N'Quảng Ngãi'
FROM Users U WHERE U.Username = 'officer10';

PRINT '✅ Employees inserted (17 total)';
GO

-- ================================================
-- 4. INSERT CUSTOMERS
-- ================================================
PRINT 'Step 4: Inserting Customers...';

INSERT INTO Customers (FullName, DateOfBirth, Phone, Email, Address, IdentityNumber, CreditScore, Gender, Status) VALUES
(N'Nguyễn Văn Khách 1', '1988-01-15', '0901234567', 'khach1@email.com', N'12 Lê Lợi, Q1, TP.HCM', '079088001001', 750, N'Nam', 'Active'),
(N'Trần Thị Khách 2', '1990-05-20', '0902345678', 'khach2@email.com', N'34 Trần Hưng Đạo, Q5, TP.HCM', '079090002002', 720, N'Nữ', 'Active'),
(N'Lê Văn Khách 3', '1985-03-10', '0903456789', 'khach3@email.com', N'56 Nguyễn Huệ, Q1, TP.HCM', '079085003003', 780, N'Nam', 'Active'),
(N'Phạm Thị Khách 4', '1992-07-25', '0904567890', 'khach4@email.com', N'78 Hai Bà Trưng, Q3, TP.HCM', '079092004004', 690, N'Nữ', 'Active'),
(N'Hoàng Văn Khách 5', '1987-11-30', '0905678901', 'khach5@email.com', N'90 Điện Biên Phủ, Q3, TP.HCM', '079087005005', 710, N'Nam', 'Active'),
(N'Vũ Thị Khách 6', '1995-02-14', '0906789012', 'khach6@email.com', N'123 Võ Văn Tần, Q3, TP.HCM', '079095006006', 680, N'Nữ', 'Active'),
(N'Đặng Văn Khách 7', '1989-06-18', '0907890123', 'khach7@email.com', N'234 Phan Xích Long, PN, TP.HCM', '079089007007', 730, N'Nam', 'Active'),
(N'Bùi Thị Khách 8', '1991-09-22', '0908901234', 'khach8@email.com', N'345 Cách Mạng T8, Q10, TP.HCM', '079091008008', 700, N'Nữ', 'Active'),
(N'Ngô Văn Khách 9', '1986-12-05', '0909012345', 'khach9@email.com', N'456 Lý Thường Kiệt, Q10, TP.HCM', '079086009009', 740, N'Nam', 'Active'),
(N'Mai Thị Khách 10', '1994-04-28', '0910123456', 'khach10@email.com', N'567 3 Tháng 2, Q10, TP.HCM', '079094010010', 760, N'Nữ', 'Active'),
(N'Trương Văn Khách 11', '1993-08-15', '0911234567', 'khach11@email.com', N'678 Nguyễn Văn Cừ, Q5, TP.HCM', '079093011011', 705, N'Nam', 'Active'),
(N'Đinh Thị Khách 12', '1996-03-20', '0912345678', 'khach12@email.com', N'789 Lê Hồng Phong, Q10, TP.HCM', '079096012012', 725, N'Nữ', 'Active'),
(N'Phan Văn Khách 13', '1984-11-10', '0913456789', 'khach13@email.com', N'890 Trường Chinh, TB, TP.HCM', '079084013013', 745, N'Nam', 'Active'),
(N'Lý Thị Khách 14', '1991-07-05', '0914567890', 'khach14@email.com', N'901 Xô Viết Nghệ Tĩnh, BT, TP.HCM', '079091014014', 715, N'Nữ', 'Active'),
(N'Võ Văn Khách 15', '1989-12-25', '0915678901', 'khach15@email.com', N'012 Hoàng Văn Thụ, TB, TP.HCM', '079089015015', 735, N'Nam', 'Active');

PRINT '✅ Customers inserted (15 total)';
GO

-- ================================================
-- 5. INSERT LOAN PRODUCTS
-- ================================================
PRINT 'Step 5: Inserting Loan Products...';

INSERT INTO LoanProducts (ProductName, ProductType, MinAmount, MaxAmount, MinTerm, MaxTerm, InterestRateMin, InterestRateMax, RequireCollateral, Description, IsActive) VALUES
(N'Vay tiêu dùng cá nhân', N'Cá nhân', 10000000, 500000000, 12, 60, 7.5, 12.0, 0, N'Vay tiêu dùng không cần tài sản đảm bảo', 1),
(N'Vay mua nhà', N'Thế chấp', 100000000, 5000000000, 60, 240, 6.5, 9.5, 1, N'Vay mua nhà với thế chấp bất động sản', 1),
(N'Vay mua ô tô', N'Thế chấp', 50000000, 2000000000, 12, 84, 7.0, 10.0, 1, N'Vay mua ô tô với thế chấp xe', 1),
(N'Vay kinh doanh SME', N'Doanh nghiệp', 50000000, 10000000000, 12, 120, 8.0, 13.0, 1, N'Vay cho doanh nghiệp SME', 1),
(N'Vay tín chấp lương', N'Cá nhân', 5000000, 200000000, 6, 36, 8.5, 14.0, 0, N'Vay tín chấp dựa trên lương', 1);

PRINT '✅ Loan Products inserted (5 total)';
GO

-- ================================================
-- 6. INSERT CREDIT APPLICATIONS
-- ================================================
PRINT 'Step 6: Inserting Credit Applications...';

DECLARE @Cust1 INT, @Cust2 INT, @Cust3 INT, @Cust4 INT, @Cust5 INT;
DECLARE @Cust6 INT, @Cust7 INT, @Cust8 INT, @Cust9 INT, @Cust10 INT;
DECLARE @Prod1 INT, @Prod2 INT, @Prod3 INT;
DECLARE @Off1 INT, @Off2 INT, @Off3 INT;

SELECT @Cust1 = MIN(CustomerID) FROM Customers;
SET @Cust2 = @Cust1 + 1; SET @Cust3 = @Cust1 + 2; SET @Cust4 = @Cust1 + 3; SET @Cust5 = @Cust1 + 4;
SET @Cust6 = @Cust1 + 5; SET @Cust7 = @Cust1 + 6; SET @Cust8 = @Cust1 + 7; SET @Cust9 = @Cust1 + 8; SET @Cust10 = @Cust1 + 9;

SELECT @Prod1 = MIN(ProductID) FROM LoanProducts;
SET @Prod2 = @Prod1 + 1; SET @Prod3 = @Prod1 + 2;

SELECT @Off1 = MIN(EmployeeID) FROM Employees WHERE Department = N'Tín dụng';
SET @Off2 = @Off1 + 1; SET @Off3 = @Off1 + 2;

-- PENDING applications (5)
INSERT INTO CreditApplications (ApplicationNumber, CustomerID, ProductID, RequestedAmount, RequestedTerm, Purpose, Status, AssignedOfficerID, ApplicationDate) VALUES
('APP-2026-001', @Cust1, @Prod1, 200000000, 24, N'Vay tiêu dùng mua sắm', 'Pending', @Off1, GETDATE()),
('APP-2026-002', @Cust2, @Prod2, 1500000000, 120, N'Vay mua nhà', 'Pending', @Off2, DATEADD(day, -1, GETDATE())),
('APP-2026-003', @Cust3, @Prod3, 500000000, 60, N'Vay mua xe ô tô', 'Pending', @Off1, DATEADD(day, -2, GETDATE())),
('APP-2026-004', @Cust4, @Prod1, 100000000, 12, N'Vay du lịch', 'Pending', @Off3, DATEADD(day, -3, GETDATE())),
('APP-2026-005', @Cust5, @Prod1, 150000000, 18, N'Vay sửa nhà', 'Pending', @Off2, DATEADD(day, -4, GETDATE()));

-- UNDER REVIEW (3)
INSERT INTO CreditApplications (ApplicationNumber, CustomerID, ProductID, RequestedAmount, RequestedTerm, Purpose, Status, AssignedOfficerID, ReviewedBy, ApplicationDate, ReviewDate) VALUES
('APP-2026-006', @Cust6, @Prod2, 2000000000, 180, N'Vay mua căn hộ', 'UnderReview', @Off1, @Off1, DATEADD(day, -7, GETDATE()), DATEADD(day, -5, GETDATE())),
('APP-2026-007', @Cust7, @Prod3, 800000000, 72, N'Vay mua xe Mercedes', 'UnderReview', @Off2, @Off2, DATEADD(day, -8, GETDATE()), DATEADD(day, -6, GETDATE())),
('APP-2026-008', @Cust8, @Prod1, 300000000, 36, N'Vay kinh doanh nhỏ', 'UnderReview', @Off3, @Off3, DATEADD(day, -9, GETDATE()), DATEADD(day, -7, GETDATE()));

-- APPROVED (2)
INSERT INTO CreditApplications (ApplicationNumber, CustomerID, ProductID, RequestedAmount, RequestedTerm, Purpose, Status, AssignedOfficerID, ReviewedBy, ApprovedBy, ApplicationDate, ReviewDate, ApprovalDate) VALUES
('APP-2026-009', @Cust9, @Prod1, 180000000, 24, N'Vay tín dụng cá nhân', 'Approved', @Off1, @Off1, @Off1, DATEADD(day, -15, GETDATE()), DATEADD(day, -12, GETDATE()), DATEADD(day, -10, GETDATE())),
('APP-2026-010', @Cust10, @Prod2, 3000000000, 240, N'Vay mua biệt thự', 'Approved', @Off2, @Off2, @Off2, DATEADD(day, -20, GETDATE()), DATEADD(day, -17, GETDATE()), DATEADD(day, -15, GETDATE()));

PRINT '✅ Credit Applications inserted (10 total)';
GO

-- ================================================
-- 7. INSERT EXTERNAL SYSTEMS
-- ================================================
PRINT 'Step 7: Inserting External Systems...';

INSERT INTO ExternalSystems (SystemName, SystemType, APIEndpoint, APIKey, Status, Description) VALUES
(N'VNPay Payment Gateway', 'Payment', 'https://api.vnpay.vn/v2', 'VNPAY_KEY_2026', 'Active', N'Cổng thanh toán VNPay'),
(N'CIC Credit Bureau', 'CreditCheck', 'https://api.cic.org.vn/check', 'CIC_API_2026', 'Active', N'Trung tâm Thông tin Tín dụng'),
(N'SBV Exchange Rate', 'ExchangeRate', 'https://api.sbv.gov.vn/rates', 'SBV_KEY_2026', 'Active', N'Tỷ giá Ngân hàng Nhà nước');

PRINT '✅ External Systems inserted (3 total)';
GO

-- ================================================
-- VERIFICATION
-- ================================================
PRINT '';
PRINT '==============================================';
PRINT '✅ DATA INSERTION COMPLETED!';
PRINT '==============================================';
PRINT '';

SELECT 'Roles' AS [Table], COUNT(*) AS [Count] FROM Roles
UNION ALL SELECT 'Users', COUNT(*) FROM Users
UNION ALL SELECT 'Employees', COUNT(*) FROM Employees
UNION ALL SELECT 'Customers', COUNT(*) FROM Customers
UNION ALL SELECT 'LoanProducts', COUNT(*) FROM LoanProducts
UNION ALL SELECT 'CreditApplications', COUNT(*) FROM CreditApplications
UNION ALL SELECT 'ExternalSystems', COUNT(*) FROM ExternalSystems;

PRINT '';
PRINT '📝 LOGIN CREDENTIALS:';
PRINT '  Admin:    admin/admin, admin2/admin2';
PRINT '  Manager:  manager1/manager1 ... manager5/manager5';
PRINT '  Officer:  officer1/officer1 ... officer10/officer10';
PRINT '';
PRINT '✅ Database ready for use!';
GO