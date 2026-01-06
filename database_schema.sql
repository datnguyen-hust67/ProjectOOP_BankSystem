-- ================================================
-- BANK MANAGEMENT SYSTEM - DATABASE SCHEMA
-- Database: BankSystemOOP
-- ================================================

-- Drop database if exists and create new
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

PRINT '🏦 Creating BankSystemOOP Database Schema...';
GO

-- ================================================
-- TABLE 1: Roles (Vai trò)
-- ================================================
CREATE TABLE Roles (
    RoleID INT PRIMARY KEY IDENTITY(1,1),
    RoleName NVARCHAR(50) NOT NULL UNIQUE,
    Description NVARCHAR(255),
    CreatedAt DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT CK_Roles_RoleName CHECK (RoleName IN (N'Admin', N'Manager', N'CreditOfficer', N'Customer'))
);

-- ================================================
-- TABLE 2: Users (Người dùng)
-- ================================================
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) NOT NULL UNIQUE,
    PasswordPlainText NVARCHAR(100) NOT NULL, -- Plain text for easy testing
    RoleID INT NOT NULL,
    IsActive BIT DEFAULT 1,
    LastLogin DATETIME,
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_Users_Roles FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
);

-- ================================================
-- TABLE 3: Employees (Nhân viên)
-- ================================================
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL UNIQUE,
    FullName NVARCHAR(100) NOT NULL,
    DateOfBirth DATE,
    Phone NVARCHAR(15),
    Email NVARCHAR(100),
    Department NVARCHAR(100), -- Phòng ban
    Position NVARCHAR(100), -- Chức vụ
    Salary DECIMAL(18,2), -- Mức lương
    HireDate DATE DEFAULT CAST(GETDATE() AS DATE),
    ManagerID INT, -- Quản lý trực tiếp
    Status NVARCHAR(20) DEFAULT N'Active' CHECK (Status IN (N'Active', N'Inactive', N'Locked')),
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE(),
    DeletedAt DATETIME NULL,
    
    -- Additional fields
    Address NVARCHAR(255),
    IdentityNumber NVARCHAR(20),
    Hometown NVARCHAR(100),
    
    CONSTRAINT FK_Employees_Users FOREIGN KEY (UserID) REFERENCES Users(UserID),
    CONSTRAINT FK_Employees_Manager FOREIGN KEY (ManagerID) REFERENCES Employees(EmployeeID)
);

-- ================================================
-- TABLE 4: Customers (Khách hàng)
-- ================================================
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY IDENTITY(1,1),
    FullName NVARCHAR(100) NOT NULL,
    DateOfBirth DATE,
    Phone NVARCHAR(15) UNIQUE,
    Email NVARCHAR(100) UNIQUE,
    Address NVARCHAR(255),
    IdentityNumber NVARCHAR(20) UNIQUE, -- CCCD/CMND
    CreditScore INT DEFAULT 0, -- Điểm tín dụng
    Gender NVARCHAR(10),
    Status NVARCHAR(20) DEFAULT N'Active',
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE()
);

-- ================================================
-- TABLE 5: LoanProducts (Sản phẩm vay)
-- ================================================
CREATE TABLE LoanProducts (
    ProductID INT PRIMARY KEY IDENTITY(1,1),
    ProductName NVARCHAR(100) NOT NULL,
    ProductType NVARCHAR(50), -- Loại vay: Cá nhân, Doanh nghiệp, Thế chấp
    MinAmount DECIMAL(18,2),
    MaxAmount DECIMAL(18,2),
    MinTerm INT, -- Kỳ hạn tối thiểu (tháng)
    MaxTerm INT, -- Kỳ hạn tối đa (tháng)
    InterestRateMin DECIMAL(5,2), -- Lãi suất tối thiểu %
    InterestRateMax DECIMAL(5,2), -- Lãi suất tối đa %
    RequireCollateral BIT DEFAULT 0, -- Yêu cầu tài sản đảm bảo
    Description NVARCHAR(500),
    IsActive BIT DEFAULT 1,
    CreatedAt DATETIME DEFAULT GETDATE()
);

-- ================================================
-- TABLE 6: CreditApplications (Hồ sơ vay)
-- ================================================
CREATE TABLE CreditApplications (
    ApplicationID INT PRIMARY KEY IDENTITY(1,1),
    ApplicationNumber NVARCHAR(50) UNIQUE NOT NULL, -- Mã hồ sơ
    CustomerID INT NOT NULL,
    ProductID INT NOT NULL,
    
    -- Thông tin khoản vay
    RequestedAmount DECIMAL(18,2) NOT NULL,
    RequestedTerm INT NOT NULL, -- Kỳ hạn (tháng)
    Purpose NVARCHAR(255), -- Mục đích vay
    
    -- Trạng thái
    Status NVARCHAR(50) DEFAULT N'Pending' CHECK (Status IN (
        N'Pending',        -- Chờ thẩm định
        N'UnderReview',    -- Đang thẩm định
        N'Approved',       -- Đã duyệt
        N'Rejected',       -- Từ chối
        N'Disbursed',      -- Đã giải ngân
        N'Completed',      -- Hoàn thành
        N'Cancelled'       -- Hủy bỏ
    )),
    
    -- Người xử lý
    AssignedOfficerID INT, -- Nhân viên được giao
    ReviewedBy INT, -- Người thẩm định
    ApprovedBy INT, -- Người phê duyệt
    
    -- Ngày tháng
    ApplicationDate DATETIME DEFAULT GETDATE(),
    ReviewDate DATETIME,
    ApprovalDate DATETIME,
    DisbursementDate DATETIME,
    
    -- Ghi chú
    Notes NVARCHAR(500),
    RejectionReason NVARCHAR(500),
    
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_CreditApp_Customer FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    CONSTRAINT FK_CreditApp_Product FOREIGN KEY (ProductID) REFERENCES LoanProducts(ProductID),
    CONSTRAINT FK_CreditApp_Officer FOREIGN KEY (AssignedOfficerID) REFERENCES Employees(EmployeeID),
    CONSTRAINT FK_CreditApp_Reviewer FOREIGN KEY (ReviewedBy) REFERENCES Employees(EmployeeID),
    CONSTRAINT FK_CreditApp_Approver FOREIGN KEY (ApprovedBy) REFERENCES Employees(EmployeeID)
);

-- ================================================
-- TABLE 7: CreditAssessment (Thẩm định tín dụng)
-- ================================================
CREATE TABLE CreditAssessment (
    AssessmentID INT PRIMARY KEY IDENTITY(1,1),
    ApplicationID INT NOT NULL UNIQUE,
    
    -- Thông tin CIC
    CICScore INT, -- Điểm CIC
    CICStatus NVARCHAR(50), -- Kết quả tra cứu CIC
    CICCheckDate DATETIME,
    
    -- Thẩm định thu nhập
    MonthlyIncome DECIMAL(18,2),
    OtherIncome DECIMAL(18,2),
    MonthlyExpenses DECIMAL(18,2),
    DebtToIncomeRatio DECIMAL(5,2), -- Tỷ lệ nợ/thu nhập
    
    -- Thẩm định tài sản
    CollateralType NVARCHAR(100), -- Loại tài sản đảm bảo
    CollateralValue DECIMAL(18,2), -- Giá trị tài sản
    LoanToValueRatio DECIMAL(5,2), -- Tỷ lệ cho vay/giá trị tài sản
    
    -- Kết quả thẩm định
    RiskLevel NVARCHAR(20) CHECK (RiskLevel IN (N'Low', N'Medium', N'High', N'VeryHigh')),
    RecommendedAmount DECIMAL(18,2),
    RecommendedInterestRate DECIMAL(5,2),
    AssessmentNotes NVARCHAR(1000),
    
    AssessedBy INT,
    AssessmentDate DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_Assessment_Application FOREIGN KEY (ApplicationID) REFERENCES CreditApplications(ApplicationID),
    CONSTRAINT FK_Assessment_Officer FOREIGN KEY (AssessedBy) REFERENCES Employees(EmployeeID)
);

-- ================================================
-- TABLE 8: Loans (Khoản vay đã giải ngân)
-- ================================================
CREATE TABLE Loans (
    LoanID INT PRIMARY KEY IDENTITY(1,1),
    LoanNumber NVARCHAR(50) UNIQUE NOT NULL,
    ApplicationID INT NOT NULL UNIQUE,
    CustomerID INT NOT NULL,
    
    -- Thông tin khoản vay
    PrincipalAmount DECIMAL(18,2) NOT NULL, -- Số tiền gốc
    InterestRate DECIMAL(5,2) NOT NULL,
    LoanTerm INT NOT NULL, -- Kỳ hạn (tháng)
    MonthlyPayment DECIMAL(18,2), -- Trả hàng tháng
    
    -- Số dư
    OutstandingBalance DECIMAL(18,2), -- Dư nợ gốc
    OutstandingInterest DECIMAL(18,2) DEFAULT 0, -- Lãi phải trả
    
    -- Trạng thái
    Status NVARCHAR(50) DEFAULT N'Active' CHECK (Status IN (
        N'Active',      -- Đang hoạt động
        N'Overdue',     -- Quá hạn
        N'PaidOff',     -- Đã tất toán
        N'WrittenOff'   -- Xóa nợ
    )),
    
    -- Ngày tháng
    DisbursementDate DATE NOT NULL,
    FirstPaymentDate DATE,
    MaturityDate DATE, -- Ngày đến hạn
    
    -- Giải ngân
    DisbursedBy INT,
    DisbursementMethod NVARCHAR(50), -- Phương thức giải ngân
    
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_Loans_Application FOREIGN KEY (ApplicationID) REFERENCES CreditApplications(ApplicationID),
    CONSTRAINT FK_Loans_Customer FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    CONSTRAINT FK_Loans_Officer FOREIGN KEY (DisbursedBy) REFERENCES Employees(EmployeeID)
);

-- ================================================
-- TABLE 9: PaymentSchedule (Lịch trả nợ)
-- ================================================
CREATE TABLE PaymentSchedule (
    ScheduleID INT PRIMARY KEY IDENTITY(1,1),
    LoanID INT NOT NULL,
    InstallmentNumber INT NOT NULL, -- Kỳ trả thứ
    
    -- Số tiền
    PrincipalAmount DECIMAL(18,2), -- Gốc
    InterestAmount DECIMAL(18,2), -- Lãi
    TotalAmount DECIMAL(18,2), -- Tổng
    
    -- Ngày
    DueDate DATE NOT NULL, -- Ngày đến hạn
    PaidDate DATE, -- Ngày thực trả
    
    -- Trạng thái
    Status NVARCHAR(20) DEFAULT N'Pending' CHECK (Status IN (
        N'Pending',  -- Chưa đến hạn
        N'Paid',     -- Đã trả
        N'Overdue',  -- Quá hạn
        N'Partial'   -- Trả một phần
    )),
    
    PaidAmount DECIMAL(18,2) DEFAULT 0,
    
    CreatedAt DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_Schedule_Loan FOREIGN KEY (LoanID) REFERENCES Loans(LoanID)
);

-- ================================================
-- TABLE 10: Payments (Giao dịch thanh toán)
-- ================================================
CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY IDENTITY(1,1),
    LoanID INT NOT NULL,
    ScheduleID INT,
    
    PaymentAmount DECIMAL(18,2) NOT NULL,
    PaymentDate DATETIME DEFAULT GETDATE(),
    PaymentMethod NVARCHAR(50), -- Phương thức thanh toán
    
    PrincipalPaid DECIMAL(18,2) DEFAULT 0,
    InterestPaid DECIMAL(18,2) DEFAULT 0,
    PenaltyPaid DECIMAL(18,2) DEFAULT 0, -- Phí phạt (nếu có)
    
    TransactionReference NVARCHAR(100), -- Mã giao dịch
    Notes NVARCHAR(255),
    
    RecordedBy INT, -- Người ghi nhận
    CreatedAt DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_Payments_Loan FOREIGN KEY (LoanID) REFERENCES Loans(LoanID),
    CONSTRAINT FK_Payments_Schedule FOREIGN KEY (ScheduleID) REFERENCES PaymentSchedule(ScheduleID),
    CONSTRAINT FK_Payments_Officer FOREIGN KEY (RecordedBy) REFERENCES Employees(EmployeeID)
);

-- ================================================
-- TABLE 11: ExternalSystems (Hệ thống bên ngoài)
-- ================================================
CREATE TABLE ExternalSystems (
    SystemID INT PRIMARY KEY IDENTITY(1,1),
    SystemName NVARCHAR(100) NOT NULL,
    SystemType NVARCHAR(50) CHECK (SystemType IN ('Payment', 'CreditCheck', 'ExchangeRate', 'Other')),
    APIEndpoint NVARCHAR(255),
    APIKey NVARCHAR(255),
    Status NVARCHAR(20) DEFAULT N'Active' CHECK (Status IN (N'Active', N'Inactive', N'Maintenance')),
    Description NVARCHAR(500),
    LastChecked DATETIME,
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE()
);

-- ================================================
-- TABLE 12: AuditLog (Nhật ký hệ thống)
-- ================================================
CREATE TABLE AuditLog (
    LogID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT,
    Action NVARCHAR(100), -- Hành động
    TableName NVARCHAR(50), -- Bảng bị tác động
    RecordID INT, -- ID bản ghi
    OldValue NVARCHAR(MAX), -- Giá trị cũ (JSON)
    NewValue NVARCHAR(MAX), -- Giá trị mới (JSON)
    IPAddress NVARCHAR(50),
    CreatedAt DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_AuditLog_User FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- ================================================
-- INDEXES for Performance
-- ================================================
CREATE INDEX IX_Users_Username ON Users(Username);
CREATE INDEX IX_Employees_Status ON Employees(Status);
CREATE INDEX IX_Customers_IdentityNumber ON Customers(IdentityNumber);
CREATE INDEX IX_CreditApp_Status ON CreditApplications(Status);
CREATE INDEX IX_CreditApp_Customer ON CreditApplications(CustomerID);
CREATE INDEX IX_Loans_Customer ON Loans(CustomerID);
CREATE INDEX IX_Loans_Status ON Loans(Status);
CREATE INDEX IX_PaymentSchedule_DueDate ON PaymentSchedule(DueDate);
CREATE INDEX IX_PaymentSchedule_Status ON PaymentSchedule(Status);

GO

PRINT '✅ Database schema created successfully!';
PRINT '';
PRINT '📊 Tables created:';
PRINT '  1. Roles';
PRINT '  2. Users (Plain text password)';
PRINT '  3. Employees';
PRINT '  4. Customers';
PRINT '  5. LoanProducts';
PRINT '  6. CreditApplications';
PRINT '  7. CreditAssessment';
PRINT '  8. Loans';
PRINT '  9. PaymentSchedule';
PRINT ' 10. Payments';
PRINT ' 11. ExternalSystems';
PRINT ' 12. AuditLog';
PRINT '';
PRINT '✅ Ready for data insertion!';
GO