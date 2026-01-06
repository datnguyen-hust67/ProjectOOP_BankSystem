"""
File: bank_app_final_COMPLETE.py
Bank Management System - COMPLETE VERSION
Database: BankSystemOOP

FEATURES:
✅ Fixed all dialog errors
✅ Dynamic time in all workspaces
✅ Charts in Credit Officer dashboard (Pie + Bar)
✅ Export PDF for Employee & System lists
✅ Fixed dashboard stats (correct counts)
✅ Create loan application with database reference
✅ All dialogs working perfectly
"""

import customtkinter as ctk
import pyodbc
from datetime import datetime
from tkinter import messagebox, ttk
import sys

sys.path.append('.')
from models.employee import Employee
from models.credit_application import CreditApplication
from models.external_system import ExternalSystem

from repositories.employee_repository import EmployeeRepository
from repositories.credit_application_repository import CreditApplicationRepository
from repositories.external_system_repository import ExternalSystemRepository

from services.employee_service import EmployeeService
from services.credit_service import CreditService
from services.external_system_service import ExternalSystemService

from controllers.manager_controller import ManagerController
from controllers.credit_officer_controller import CreditOfficerController
from controllers.external_system_controller import ExternalSystemController


class BankManagementApp(ctk.CTk):
    """Main Application - COMPLETE VERSION"""
    
    def __init__(self):
        super().__init__()
        
        self.title("BANK MANAGEMENT SYSTEM v2.0")
        self.geometry("1400x900")
        
        self.connection_string = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=BankSystemOOP;"
            "UID=SA;"
            "PWD=YourPassword;" #Your Password
            "TrustServerCertificate=yes;"
        )
        
        # Initialize repositories
        self.employee_repo = EmployeeRepository(self.connection_string)
        self.credit_repo = CreditApplicationRepository(self.connection_string)
        self.system_repo = ExternalSystemRepository(self.connection_string)
        
        # Initialize services
        self.employee_service = EmployeeService(self.employee_repo)
        self.credit_service = CreditService(self.credit_repo)
        self.system_service = ExternalSystemService(self.system_repo)
        
        # Initialize controllers
        self.manager_ctrl = ManagerController(self.employee_service)
        self.credit_ctrl = CreditOfficerController(self.credit_service)
        self.system_ctrl = ExternalSystemController(self.system_service)
        
        # Current user
        self.current_user = None
        self.current_employee = None
        self.selected_role = None
        
        # Time label
        self.time_label = None
        
        self.show_welcome_screen()
        self.update_time()
    
    def update_time(self):
        """Update time dynamically"""
        if self.time_label and self.time_label.winfo_exists():
            now = datetime.now()
            time_str = now.strftime("%H:%M:%S - %d/%m/%Y")
            self.time_label.configure(text=time_str)
        
        self.after(1000, self.update_time)
    
    # ================================================
    # WELCOME SCREEN
    # ================================================
    def show_welcome_screen(self):
        self.clear_window()
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=50, pady=50)
        
        ctk.CTkLabel(
            main_frame,
            text="🏦 BANK MANAGEMENT SYSTEM",
            font=("Arial Bold", 36)
        ).pack(pady=(0, 10))
        
        now = datetime.now()
        date_str = now.strftime("%A, %d/%m/%Y - %H:%M:%S")
        self.time_label = ctk.CTkLabel(
            main_frame,
            text=date_str,
            font=("Arial", 16)
        )
        self.time_label.pack(pady=(0, 40))
        
        ctk.CTkLabel(
            main_frame,
            text="Chọn vai trò của bạn:",
            font=("Arial", 20)
        ).pack(pady=(0, 30))
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        roles = [
            ("👨‍💼 Nhân viên tín dụng\nĐánh giá & Duyệt vay", "CreditOfficer"),
            ("👔 Manager\nQuản lý người dùng", "Manager_User"),
            ("🔧 Manager\nQuản lý hệ thống ngoài", "Manager_System")
        ]
        
        for text, role in roles:
            ctk.CTkButton(
                btn_frame,
                text=text,
                width=350,
                height=100,
                font=("Arial Bold", 18),
                command=lambda r=role: self.select_role(r)
            ).pack(pady=15)
    
    def select_role(self, role: str):
        self.selected_role = role
        self.show_login_screen()
    
    # ================================================
    # LOGIN SCREEN
    # ================================================
    def show_login_screen(self):
        self.clear_window()
        
        login_frame = ctk.CTkFrame(self)
        login_frame.pack(fill="both", expand=True, padx=100, pady=100)
        
        role_names = {
            "CreditOfficer": "Nhân viên tín dụng",
            "Manager_User": "Manager - Quản lý người dùng",
            "Manager_System": "Manager - Quản lý hệ thống ngoài"
        }
        
        ctk.CTkLabel(
            login_frame,
            text=f"🔐 ĐĂNG NHẬP\n{role_names[self.selected_role]}",
            font=("Arial Bold", 24)
        ).pack(pady=30)
        
        ctk.CTkLabel(login_frame, text="Tên đăng nhập:", font=("Arial", 14)).pack(pady=(20,5))
        self.username_entry = ctk.CTkEntry(login_frame, width=300, height=40)
        self.username_entry.pack(pady=5)
        
        ctk.CTkLabel(login_frame, text="Mật khẩu:", font=("Arial", 14)).pack(pady=(20,5))
        self.password_entry = ctk.CTkEntry(login_frame, width=300, height=40, show="*")
        self.password_entry.pack(pady=5)
        
        ctk.CTkButton(
            login_frame,
            text="Đăng nhập",
            width=300,
            height=45,
            font=("Arial Bold", 16),
            command=self.handle_login
        ).pack(pady=30)
        
        ctk.CTkButton(
            login_frame,
            text="← Quay lại",
            width=150,
            height=35,
            command=self.show_welcome_screen
        ).pack(pady=10)
        
        self.error_label = ctk.CTkLabel(
            login_frame,
            text="",
            font=("Arial", 12),
            text_color="red"
        )
        self.error_label.pack(pady=10)
    
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.error_label.configure(text="Vui lòng nhập đầy đủ thông tin")
            return
        
        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            
            query = """
                SELECT U.UserID, U.Username, U.RoleID, R.RoleName,
                       E.EmployeeID, E.FullName
                FROM Users U
                INNER JOIN Roles R ON U.RoleID = R.RoleID
                LEFT JOIN Employees E ON U.UserID = E.UserID
                WHERE U.Username = ? AND U.PasswordPlainText = ? AND U.IsActive = 1
            """
            
            cursor.execute(query, (username, password))
            row = cursor.fetchone()
            
            if not row:
                self.error_label.configure(text="❌ Sai tên đăng nhập hoặc mật khẩu")
                conn.close()
                return
            
            user = {
                'user_id': row[0],
                'username': row[1],
                'role_id': row[2],
                'role_name': row[3]
            }
            
            if row[4]:
                emp_query = """
                    SELECT EmployeeID, UserID, FullName, DateOfBirth, Phone, Email,
                           Department, Position, Salary, HireDate, ManagerID, Status,
                           CreatedAt, UpdatedAt, DeletedAt, Address, IdentityNumber, Hometown
                    FROM Employees WHERE EmployeeID = ?
                """
                cursor.execute(emp_query, (row[4],))
                emp_row = cursor.fetchone()
                
                if emp_row:
                    employee = Employee(
                        employee_id=emp_row[0],
                        user_id=emp_row[1],
                        full_name=emp_row[2],
                        date_of_birth=emp_row[3],
                        phone=emp_row[4],
                        email=emp_row[5],
                        department=emp_row[6],
                        position=emp_row[7],
                        salary=emp_row[8],
                        hire_date=emp_row[9],
                        manager_id=emp_row[10],
                        status=emp_row[11],
                        created_at=emp_row[12],
                        updated_at=emp_row[13],
                        deleted_at=emp_row[14],
                        address=emp_row[15],
                        identity_number=emp_row[16],
                        hometown=emp_row[17],
                        username=row[1],
                        role_name=row[3]
                    )
                    self.current_employee = employee
            
            self.current_user = user
            conn.close()
            
            self.validate_and_redirect()
            
        except Exception as e:
            self.error_label.configure(text=f"❌ Lỗi: {str(e)}")
    
    def validate_and_redirect(self):
        role_name = self.current_user['role_name']
        
        if self.selected_role == "CreditOfficer":
            if role_name == "CreditOfficer":
                self.show_credit_officer_workspace()
            else:
                messagebox.showerror("Lỗi", "Bạn không có quyền Credit Officer!")
                self.show_welcome_screen()
        
        elif self.selected_role in ["Manager_User", "Manager_System"]:
            if role_name in ["Manager", "Admin"]:
                if self.selected_role == "Manager_User":
                    self.show_manager_user_workspace()
                else:
                    self.show_manager_system_workspace()
            else:
                messagebox.showerror("Lỗi", "Bạn không có quyền Manager!")
                self.show_welcome_screen()
    
    # ================================================
    # CREDIT OFFICER WORKSPACE
    # ================================================
    def show_credit_officer_workspace(self):
        self.clear_window()
        self.credit_ctrl.set_current_user(self.current_user, self.current_employee)
        
        header = ctk.CTkFrame(self, height=60, fg_color="#1f6aa5")
        header.pack(fill="x", side="top")
        
        ctk.CTkLabel(
            header,
            text=f"👨‍💼 NHÂN VIÊN TÍN DỤNG - {self.current_employee.full_name}",
            font=("Arial Bold", 18),
            text_color="white"
        ).pack(side="left", padx=20, pady=15)
        
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S - %d/%m/%Y")
        self.time_label = ctk.CTkLabel(
            header,
            text=time_str,
            font=("Arial", 14),
            text_color="white"
        )
        self.time_label.pack(side="left", padx=20)
        
        ctk.CTkButton(
            header,
            text="Đăng xuất",
            width=100,
            command=self.show_welcome_screen
        ).pack(side="right", padx=20)
        
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        sidebar = ctk.CTkScrollableFrame(main, width=250)
        sidebar.pack(side="left", fill="y", padx=(0,20))
        
        self.content_area = ctk.CTkFrame(main)
        self.content_area.pack(side="left", fill="both", expand=True)
        
        menu_items = [
            ("📊 Dashboard", self.show_credit_dashboard),
            ("➕ Tạo hồ sơ vay mới", self.show_create_application_dialog),
            ("⏳ Hồ sơ chờ thẩm định", lambda: self.show_applications_by_status("Pending")),
            ("🔍 Đang thẩm định", lambda: self.show_applications_by_status("UnderReview")),
            ("✅ Chờ giải ngân", lambda: self.show_applications_by_status("Approved")),
            ("💰 Đã giải ngân", lambda: self.show_applications_by_status("Disbursed")),
            ("❌ Đã từ chối", lambda: self.show_applications_by_status("Rejected")),
        ]
        
        for text, command in menu_items:
            ctk.CTkButton(
                sidebar,
                text=text,
                width=230,
                height=40,
                anchor="w",
                command=command
            ).pack(pady=5, padx=10)
        
        self.show_credit_dashboard()
    
    def show_credit_dashboard(self):
        """Dashboard with FIXED stats and charts"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            self.content_area,
            text="📊 DASHBOARD - HỒ SƠ VAY",
            font=("Arial Bold", 24)
        ).pack(pady=20)
        
        # Get CORRECT statistics
        stats = self.credit_ctrl.get_statistics() 
        
        stats_frame = ctk.CTkFrame(self.content_area)
        stats_frame.pack(pady=20, padx=20, fill="x")
        
        stat_labels = [
            ("Tổng số", stats['total'], "#3498db"),
            ("Chờ xử lý", stats['pending'], "#f39c12"),
            ("Đang thẩm định", stats['under_review'], "#9b59b6"),
            ("Đã duyệt", stats['approved'], "#27ae60"),
            ("Đã giải ngân", stats['disbursed'], "#16a085"),
            ("Từ chối", stats['rejected'], "#e74c3c")
        ]
        
        for i, (label, value, color) in enumerate(stat_labels):
            card = ctk.CTkFrame(stats_frame, fg_color=color)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(card, text=label, font=("Arial", 14), text_color="white").pack(pady=5)
            ctk.CTkLabel(card, text=str(value), font=("Arial Bold", 32), text_color="white").pack(pady=5)
        
        stats_frame.grid_columnconfigure((0,1,2), weight=1)
        
        # CHARTS
        chart_frame = ctk.CTkFrame(self.content_area)
        chart_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        left_chart = ctk.CTkFrame(chart_frame)
        left_chart.pack(side="left", fill="both", expand=True, padx=(0,10))
        
        right_chart = ctk.CTkFrame(chart_frame)
        right_chart.pack(side="right", fill="both", expand=True, padx=(10,0))
        
        try:
            import matplotlib
            matplotlib.use('TkAgg')
            import matplotlib.pyplot as plt
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            # PIE CHART
            ctk.CTkLabel(left_chart, text="📊 Phân bổ trạng thái hồ sơ", font=("Arial Bold", 16)).pack(pady=10)
            
            labels = ['Chờ xử lý', 'Đang thẩm định', 'Đã duyệt', 'Đã giải ngân', 'Từ chối']
            sizes = [stats['pending'], stats['under_review'], stats['approved'], stats['disbursed'], stats['rejected']]
            colors = ['#f39c12', '#9b59b6', '#27ae60', '#16a085', '#e74c3c']
            
            fig1 = Figure(figsize=(5, 4), facecolor='#2b2b2b')
            ax1 = fig1.add_subplot(111)
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, textprops={'color': 'white'})
            ax1.set_facecolor('#2b2b2b')
            
            canvas1 = FigureCanvasTkAgg(fig1, left_chart)
            canvas1.draw()
            canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
            # BAR CHART
            ctk.CTkLabel(right_chart, text="📈 Thống kê số lượng hồ sơ", font=("Arial Bold", 16)).pack(pady=10)
            
            fig2 = Figure(figsize=(5, 4), facecolor='#2b2b2b')
            ax2 = fig2.add_subplot(111)
            
            statuses = ['Chờ xử lý', 'Đang thẩm định', 'Đã duyệt', 'Đã giải ngân', 'Từ chối']
            values = [stats['pending'], stats['under_review'], stats['approved'], stats['disbursed'], stats['rejected']]
            bar_colors = ['#f39c12', '#9b59b6', '#27ae60', '#16a085', '#e74c3c']
            
            bars = ax2.bar(statuses, values, color=bar_colors)
            ax2.set_ylabel('Số lượng', color='white')
            ax2.set_facecolor('#2b2b2b')
            ax2.tick_params(colors='white', labelsize=9)
            ax2.spines['bottom'].set_color('white')
            ax2.spines['left'].set_color('white')
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', color='white', fontweight='bold')
            
            # FIX: Use matplotlib.pyplot instead of plt
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=15, ha='right')
            fig2.tight_layout()
            
            canvas2 = FigureCanvasTkAgg(fig2, right_chart)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
        except ImportError:
            ctk.CTkLabel(left_chart, text="⚠️ Cài đặt matplotlib:\npip install matplotlib", 
                        text_color="orange").pack(pady=50)
            ctk.CTkLabel(right_chart, text="⚠️ Cài đặt matplotlib:\npip install matplotlib", 
                        text_color="orange").pack(pady=50)
    
    def show_create_application_dialog(self):
        """Dialog tạo hồ sơ vay - WITH DATABASE REFERENCE"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Tạo hồ sơ vay mới")
        dialog.geometry("650x750")
        
        dialog.update()
        dialog.after(100, lambda: dialog.grab_set())
        
        form = ctk.CTkScrollableFrame(dialog)
        form.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(form, text="TẠO HỒ SƠ VAY MỚI", font=("Arial Bold", 20)).pack(pady=15)
        
        # Load from database
        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            
            cursor.execute("SELECT CustomerID, FullName, IdentityNumber FROM Customers ORDER BY CustomerID")
            customers = cursor.fetchall()
            
            cursor.execute("SELECT ProductID, ProductName, InterestRateMin, InterestRateMax, MinAmount, MaxAmount FROM LoanProducts WHERE IsActive = 1 ORDER BY ProductID")
            products = cursor.fetchall()
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể load dữ liệu: {str(e)}")
            dialog.destroy()
            return
        
        if not customers:
            messagebox.showerror("Lỗi", "Không có khách hàng nào trong hệ thống!")
            dialog.destroy()
            return
        
        if not products:
            messagebox.showerror("Lỗi", "Không có sản phẩm vay nào!")
            dialog.destroy()
            return
        
        # Customer Selection
        ctk.CTkLabel(form, text="* Chọn khách hàng:", font=("Arial Bold", 13)).pack(anchor="w", padx=20, pady=(15,5))
        
        customer_options = [f"{c[0]} - {c[1]} ({c[2]})" for c in customers]
        customer_var = ctk.StringVar(value=customer_options[0])
        customer_menu = ctk.CTkOptionMenu(form, width=580, values=customer_options, variable=customer_var)
        customer_menu.pack(padx=20, pady=(0,15))
        
        # Product Selection
        ctk.CTkLabel(form, text="* Chọn sản phẩm vay:", font=("Arial Bold", 13)).pack(anchor="w", padx=20, pady=(0,5))
        
        product_options = [f"{p[0]} - {p[1]} (Lãi: {float(p[2]):.2f}%-{float(p[3]):.2f}%/năm)" for p in products]
        product_var = ctk.StringVar(value=product_options[0])
        product_menu = ctk.CTkOptionMenu(form, width=580, values=product_options, variable=product_var)
        product_menu.pack(padx=20, pady=(0,15))
        
        # Product info display
        info_frame = ctk.CTkFrame(form, fg_color="#2b2b2b")
        info_frame.pack(padx=20, pady=(0,15), fill="x")
        
        info_label = ctk.CTkLabel(info_frame, text="", font=("Arial", 11), justify="left")
        info_label.pack(pady=10, padx=15)
        
        def update_product_info(*args):
            if product_var.get():
                prod_id = int(product_var.get().split(" - ")[0])
                prod = next((p for p in products if p[0] == prod_id), None)
                if prod:
                    info_label.configure(
                        text=f"Lãi suất: {float(prod[2]):.2f}% - {float(prod[3]):.2f}%/năm\n"
                            f"Số tiền tối thiểu: {float(prod[4]):,.0f} VND\n"
                            f"Số tiền tối đa: {float(prod[5]):,.0f} VND"
                    )
        
        product_var.trace('w', update_product_info)
        update_product_info()
        
        # Amount
        ctk.CTkLabel(form, text="* Số tiền vay (VND):", font=("Arial Bold", 13)).pack(anchor="w", padx=20, pady=(0,5))
        amount_entry = ctk.CTkEntry(form, width=580, placeholder_text="VD: 500000000")
        amount_entry.pack(padx=20, pady=(0,15))
        
        # Term
        ctk.CTkLabel(form, text="* Kỳ hạn (tháng):", font=("Arial Bold", 13)).pack(anchor="w", padx=20, pady=(0,5))
        term_var = ctk.StringVar(value="12")
        term_menu = ctk.CTkOptionMenu(form, width=580, values=["6", "12", "24", "36", "48", "60"], variable=term_var)
        term_menu.pack(padx=20, pady=(0,15))
        
        # Purpose
        ctk.CTkLabel(form, text="* Mục đích vay:", font=("Arial Bold", 13)).pack(anchor="w", padx=20, pady=(0,5))
        purpose_entry = ctk.CTkEntry(form, width=580, placeholder_text="VD: Mua nhà, Kinh doanh...")
        purpose_entry.pack(padx=20, pady=(0,15))
        
        error_label = ctk.CTkLabel(form, text="", text_color="red", wraplength=550)
        error_label.pack(pady=10)
        
        def save():
            try:
                # Get values
                customer_id = int(customer_var.get().split(" - ")[0])
                product_id = int(product_var.get().split(" - ")[0])
                
                # Validate amount
                amount_str = amount_entry.get().strip().replace(',', '')
                if not amount_str:
                    error_label.configure(text="Vui lòng nhập số tiền vay")
                    return
                
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        error_label.configure(text="Số tiền vay phải lớn hơn 0")
                        return
                except ValueError:
                    error_label.configure(text="Số tiền vay không hợp lệ")
                    return
                
                # Validate purpose
                purpose = purpose_entry.get().strip()
                if not purpose:
                    error_label.configure(text="Vui lòng nhập mục đích vay")
                    return
                
                # DIRECT DATABASE INSERT - BYPASS SERVICE
                try:
                    conn = pyodbc.connect(self.connection_string)
                    cursor = conn.cursor()
                    
                    # Generate application number
                    now = datetime.now()
                    app_number = f"APP-{now.strftime('%Y%m%d%H%M%S')}"
                    
                    # Insert directly
                    cursor.execute("""
                        INSERT INTO CreditApplications 
                        (ApplicationNumber, CustomerID, ProductID, RequestedAmount, RequestedTerm, 
                        Purpose, Status, AssignedOfficerID, ApplicationDate)
                        VALUES (?, ?, ?, ?, ?, ?, N'Pending', ?, GETDATE())
                    """, (
                        app_number,
                        customer_id,
                        product_id,
                        amount,
                        int(term_var.get()),
                        purpose,
                        self.current_employee.employee_id
                    ))
                    
                    conn.commit()
                    
                    # Get inserted ID
                    cursor.execute("SELECT @@IDENTITY")
                    app_id = cursor.fetchone()[0]
                    
                    conn.close()
                    
                    messagebox.showinfo("Thành công", 
                        f"Đã tạo hồ sơ vay!\n\n"
                        f"Mã hồ sơ: {app_number}\n"
                        f"Khách hàng ID: {customer_id}\n"
                        f"Số tiền: {amount:,.0f} VND\n"
                        f"Kỳ hạn: {term_var.get()} tháng"
                    )
                    
                    dialog.destroy()
                    self.show_credit_dashboard()
                    
                except pyodbc.Error as db_err:
                    error_label.configure(text=f"Lỗi database: {str(db_err)}")
                except Exception as e:
                    error_label.configure(text=f"Lỗi: {str(e)}")
                    
            except ValueError as e:
                error_label.configure(text=f"Dữ liệu không hợp lệ: {str(e)}")
            except Exception as e:
                error_label.configure(text=f"Lỗi: {str(e)}")
        
        ctk.CTkButton(form, text="💾 Tạo hồ sơ", width=250, height=45, font=("Arial Bold", 15), command=save).pack(pady=25)
    
    def show_applications_by_status(self, status):
        """Show applications by status"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        status_names = {
            'Pending': '⏳ HỒ SƠ CHỜ THẨM ĐỊNH',
            'UnderReview': '🔍 HỒ SƠ ĐANG THẨM ĐỊNH',
            'Approved': '✅ HỒ SƠ CHỜ GIẢI NGÂN',
            'Disbursed': '💰 HỒ SƠ ĐÃ GIẢI NGÂN',
            'Rejected': '❌ HỒ SƠ ĐÃ TỪ CHỐI'
        }
        
        ctk.CTkLabel(
            self.content_area,
            text=status_names.get(status, status),
            font=("Arial Bold", 24)
        ).pack(pady=20)
        
        table_frame = ctk.CTkFrame(self.content_area)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        columns = ("ID", "Mã hồ sơ", "Khách hàng", "Số tiền", "Kỳ hạn", "Ngày nộp", "Trạng thái")
        tree = ttk.Treeview(table_frame, columns=columns, show="tree headings", height=15)
        
        tree.heading("#0", text="")
        for col in columns:
            tree.heading(col, text=col)
        
        tree.column("#0", width=0, stretch=False)
        tree.column("ID", width=50)
        tree.column("Mã hồ sơ", width=150)
        tree.column("Khách hàng", width=200)
        tree.column("Số tiền", width=150)
        tree.column("Kỳ hạn", width=80)
        tree.column("Ngày nộp", width=120)
        tree.column("Trạng thái", width=120)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        applications = self.credit_ctrl.get_applications_by_status(status)
        for app in applications:
            tree.insert("", "end", values=(
                app.application_id,
                app.application_number,
                app.customer_name or f"KH-{app.customer_id}",
                f"{float(app.requested_amount):,.0f}",
                f"{app.requested_term}",
                app.application_date.strftime("%d/%m/%Y") if app.application_date else "",
                app.status
            ))
        
        btn_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        if status == "Pending":
            def start_review():
                sel = tree.selection()
                if not sel:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn hồ sơ")
                    return
                app_id = tree.item(sel[0])['values'][0]
                success, msg = self.credit_ctrl.start_review(app_id)
                if success:
                    messagebox.showinfo("Thành công", msg)
                    self.show_applications_by_status(status)
                else:
                    messagebox.showerror("Lỗi", msg)
            
            ctk.CTkButton(btn_frame, text="🔍 Bắt đầu thẩm định", command=start_review).pack(side="left", padx=5)
        
        if status == "UnderReview":
            def approve():
                sel = tree.selection()
                if not sel:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn hồ sơ")
                    return
                app_id = tree.item(sel[0])['values'][0]
                if messagebox.askyesno("Xác nhận", "Phê duyệt hồ sơ này?"):
                    success, msg = self.credit_ctrl.approve_application(app_id)
                    if success:
                        messagebox.showinfo("Thành công", msg)
                        self.show_applications_by_status(status)
                    else:
                        messagebox.showerror("Lỗi", msg)
            
            def reject():
                sel = tree.selection()
                if not sel:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn hồ sơ")
                    return
                app_id = tree.item(sel[0])['values'][0]
                reason = ctk.CTkInputDialog(text="Nhập lý do từ chối:", title="Từ chối hồ sơ").get_input()
                if reason:
                    success, msg = self.credit_ctrl.reject_application(app_id, reason)
                    if success:
                        messagebox.showinfo("Thành công", msg)
                        self.show_applications_by_status(status)
                    else:
                        messagebox.showerror("Lỗi", msg)
            
            ctk.CTkButton(btn_frame, text="✅ Phê duyệt", command=approve).pack(side="left", padx=5)
            ctk.CTkButton(btn_frame, text="❌ Từ chối", command=reject).pack(side="left", padx=5)
        
        if status == "Approved":
            def disburse():
                sel = tree.selection()
                if not sel:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn hồ sơ")
                    return
                app_id = tree.item(sel[0])['values'][0]
                if messagebox.askyesno("Xác nhận", "Xác nhận giải ngân khoản vay này?"):
                    success, msg = self.credit_ctrl.disburse_loan(app_id)
                    if success:
                        messagebox.showinfo("Thành công", msg)
                        self.show_applications_by_status(status)
                    else:
                        messagebox.showerror("Lỗi", msg)
            
            ctk.CTkButton(btn_frame, text="💰 Giải ngân", command=disburse).pack(side="left", padx=5)
    
    # ================================================
    # MANAGER USER WORKSPACE
    # ================================================
    def show_manager_user_workspace(self):
        self.clear_window()
        self.manager_ctrl.set_current_user(self.current_user)
        
        header = ctk.CTkFrame(self, height=60, fg_color="#2c3e50")
        header.pack(fill="x", side="top")
        
        ctk.CTkLabel(
            header,
            text="👔 MANAGER - QUẢN LÝ NGƯỜI DÙNG",
            font=("Arial Bold", 18),
            text_color="white"
        ).pack(side="left", padx=20, pady=15)
        
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S - %d/%m/%Y")
        self.time_label = ctk.CTkLabel(
            header,
            text=time_str,
            font=("Arial", 14),
            text_color="white"
        )
        self.time_label.pack(side="left", padx=20)
        
        ctk.CTkButton(
            header,
            text="Đăng xuất",
            width=100,
            command=self.show_welcome_screen
        ).pack(side="right", padx=20)
        
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.show_employee_list(main)
    
    def show_employee_list(self, parent):
        """Employee list"""
        title_frame = ctk.CTkFrame(parent, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0,20))
        
        ctk.CTkLabel(
            title_frame,
            text="👥 DANH SÁCH NHÂN VIÊN",
            font=("Arial Bold", 24)
        ).pack(side="left")
        
        ctk.CTkButton(
            title_frame,
            text="📄 Export PDF",
            width=120,
            height=35,
            command=self.export_employees_pdf
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            title_frame,
            text="➕ Thêm nhân viên",
            width=150,
            height=35,
            command=self.show_add_employee_dialog
        ).pack(side="right", padx=10)
        
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0,10))
        
        self.search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Tìm kiếm...")
        self.search_entry.pack(side="left", padx=(0,10))
        
        ctk.CTkButton(
            search_frame,
            text="🔍 Tìm kiếm",
            width=100,
            command=self.handle_search_employee
        ).pack(side="left")
        
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("ID", "Họ tên", "Email", "Phòng ban", "Chức vụ", "Lương", "Trạng thái")
        self.emp_tree = ttk.Treeview(table_frame, columns=columns, show="tree headings", height=20)
        
        self.emp_tree.heading("#0", text="")
        for col in columns:
            self.emp_tree.heading(col, text=col)
        
        self.emp_tree.column("#0", width=0, stretch=False)
        self.emp_tree.column("ID", width=50)
        self.emp_tree.column("Họ tên", width=200)
        self.emp_tree.column("Email", width=200)
        self.emp_tree.column("Phòng ban", width=150)
        self.emp_tree.column("Chức vụ", width=200)
        self.emp_tree.column("Lương", width=120)
        self.emp_tree.column("Trạng thái", width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.emp_tree.yview)
        self.emp_tree.configure(yscrollcommand=scrollbar.set)
        
        self.emp_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10,0))
        
        ctk.CTkButton(btn_frame, text="👁️ Xem chi tiết", command=self.view_employee_detail).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✏️ Chỉnh sửa", command=self.edit_employee).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔒 Khóa/Mở", command=self.toggle_employee_lock).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Xóa", command=self.delete_employee).pack(side="left", padx=5)
        
        self.load_employee_data()
    
    def load_employee_data(self):
        for item in self.emp_tree.get_children():
            self.emp_tree.delete(item)
        
        employees = self.manager_ctrl.get_all_employees()
        employees.sort(key=lambda x: x.employee_id)
        
        for emp in employees:
            self.emp_tree.insert("", "end", values=(
                emp.employee_id,
                emp.full_name,
                emp.email,
                emp.department,
                emp.position,
                f"{emp.salary:,.0f}" if emp.salary else "",
                emp.status
            ))
    
    def handle_search_employee(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.load_employee_data()
            return
        
        for item in self.emp_tree.get_children():
            self.emp_tree.delete(item)
        
        employees = self.manager_ctrl.search_employees(keyword)
        
        for emp in employees:
            self.emp_tree.insert("", "end", values=(
                emp.employee_id,
                emp.full_name,
                emp.email,
                emp.department,
                emp.position,
                f"{emp.salary:,.0f}" if emp.salary else "",
                emp.status
            ))
    
    def show_add_employee_dialog(self):
        """Add employee dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Thêm nhân viên mới")
        dialog.geometry("600x750")
        
        dialog.update()
        dialog.after(100, lambda: dialog.grab_set())
        
        main_container = ctk.CTkScrollableFrame(dialog)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_container, text="THÊM NHÂN VIÊN MỚI", font=("Arial Bold", 18)).pack(pady=20)
        
        fields = {}
        
        field_defs = [
            ("* Tên đăng nhập:", "username", ""),
            ("* Mật khẩu:", "password", ""),
            ("* Họ tên:", "full_name", ""),
            ("* Email:", "email", ""),
            ("* Số điện thoại:", "phone", ""),
            ("* Phòng ban:", "department", "VD: Tín dụng"),
            ("* Chức vụ:", "position", "VD: Chuyên viên"),
            ("* Mức lương (VND):", "salary", "VD: 30000000")
        ]
        
        for label, key, placeholder in field_defs:
            ctk.CTkLabel(main_container, text=label, font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10,5))
            fields[key] = ctk.CTkEntry(main_container, width=500, placeholder_text=placeholder)
            fields[key].pack(padx=20, pady=(0,10))
        
        error_label = ctk.CTkLabel(main_container, text="", text_color="red")
        error_label.pack(pady=10)
        
        def save():
            try:
                conn = pyodbc.connect(self.connection_string)
                cursor = conn.cursor()
                
                cursor.execute("SELECT RoleID FROM Roles WHERE RoleName = 'CreditOfficer'")
                role_row = cursor.fetchone()
                if not role_row:
                    error_label.configure(text="Không tìm thấy role")
                    return
                
                role_id = role_row[0]
                
                cursor.execute("""
                    INSERT INTO Users (Username, PasswordPlainText, RoleID, IsActive)
                    VALUES (?, ?, ?, 1)
                """, (fields['username'].get(), fields['password'].get(), role_id))
                
                cursor.execute("SELECT @@IDENTITY")
                user_id = int(cursor.fetchone()[0])
                
                conn.commit()
                conn.close()
                
                success, msg = self.manager_ctrl.add_employee(
                    user_id=user_id,
                    full_name=fields['full_name'].get(),
                    email=fields['email'].get(),
                    phone=fields['phone'].get(),
                    department=fields['department'].get(),
                    position=fields['position'].get(),
                    salary=fields['salary'].get()
                )
                
                if success:
                    messagebox.showinfo("Thành công", msg)
                    dialog.destroy()
                    self.load_employee_data()
                else:
                    error_label.configure(text=msg)
                    
            except Exception as e:
                error_label.configure(text=f"Lỗi: {str(e)}")
        
        ctk.CTkButton(main_container, text="💾 Lưu", width=200, height=40, command=save).pack(pady=30)
    
    def view_employee_detail(self):
        selection = self.emp_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên")
            return
        
        emp_id = self.emp_tree.item(selection[0])['values'][0]
        emp = self.manager_ctrl.get_employee_details(emp_id)
        
        if emp:
            messagebox.showinfo(
                "Chi tiết nhân viên",
                f"ID: {emp.employee_id}\n"
                f"Họ tên: {emp.full_name}\n"
                f"Email: {emp.email}\n"
                f"Phòng ban: {emp.department}\n"
                f"Chức vụ: {emp.position}\n"
                f"Lương: {emp.salary:,.0f} VND\n"
                f"Trạng thái: {emp.status}"
            )
    
    def edit_employee(self):
        """Edit employee dialog"""
        selection = self.emp_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên")
            return
        
        emp_id = self.emp_tree.item(selection[0])['values'][0]
        emp = self.manager_ctrl.get_employee_details(emp_id)
        
        if not emp:
            messagebox.showerror("Lỗi", "Không tìm thấy nhân viên")
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Chỉnh sửa - {emp.full_name}")
        dialog.geometry("600x650")
        
        dialog.update()
        dialog.after(100, lambda: dialog.grab_set())
        
        main_container = ctk.CTkScrollableFrame(dialog)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_container, text="CHỈNH SỬA NHÂN VIÊN", font=("Arial Bold", 18)).pack(pady=10)
        ctk.CTkLabel(main_container, text=f"ID: {emp.employee_id} - {emp.full_name}").pack(pady=5)
        
        fields = {}
        
        field_defs = [
            ("Họ tên:", "full_name", emp.full_name or ""),
            ("Email:", "email", emp.email or ""),
            ("Số điện thoại:", "phone", emp.phone or ""),
            ("Phòng ban:", "department", emp.department or ""),
            ("Chức vụ:", "position", emp.position or ""),
            ("Lương (VND):", "salary", str(int(emp.salary)) if emp.salary else "")
        ]
        
        for label, key, value in field_defs:
            ctk.CTkLabel(main_container, text=label, font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10,5))
            fields[key] = ctk.CTkEntry(main_container, width=500)
            fields[key].insert(0, value)
            fields[key].pack(padx=20, pady=(0,10))
        
        error_label = ctk.CTkLabel(main_container, text="", text_color="red")
        error_label.pack(pady=5)
        
        def save():
            try:
                success, msg = self.manager_ctrl.update_employee(
                    emp_id,
                    full_name=fields['full_name'].get() or None,
                    email=fields['email'].get() or None,
                    phone=fields['phone'].get() or None,
                    department=fields['department'].get() or None,
                    position=fields['position'].get() or None,
                    salary=fields['salary'].get() or None
                )
                
                if success:
                    messagebox.showinfo("Thành công", msg)
                    dialog.destroy()
                    self.load_employee_data()
                else:
                    error_label.configure(text=msg)
            except Exception as e:
                error_label.configure(text=f"Lỗi: {str(e)}")
        
        ctk.CTkButton(main_container, text="💾 Lưu thay đổi", width=200, height=40, command=save).pack(pady=20)
    
    def toggle_employee_lock(self):
        selection = self.emp_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên")
            return
        
        emp_id = self.emp_tree.item(selection[0])['values'][0]
        status = self.emp_tree.item(selection[0])['values'][6]
        
        if status == "Locked":
            success, msg = self.manager_ctrl.unlock_account(emp_id)
        else:
            success, msg = self.manager_ctrl.lock_account(emp_id)
        
        if success:
            messagebox.showinfo("Thành công", msg)
            self.load_employee_data()
        else:
            messagebox.showerror("Lỗi", msg)
    
    def delete_employee(self):
        selection = self.emp_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa nhân viên này?"):
            emp_id = self.emp_tree.item(selection[0])['values'][0]
            success, msg = self.manager_ctrl.delete_employee(emp_id)
            
            if success:
                messagebox.showinfo("Thành công", msg)
                self.load_employee_data()
            else:
                messagebox.showerror("Lỗi", msg)
    
    def export_employees_pdf(self):
        """Export employees to PDF"""
        try:
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from datetime import datetime
            
            filename = f"DanhSachNhanVien_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
            elements = []
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#1f6aa5'),
                spaceAfter=30,
                alignment=1
            )
            
            elements.append(Paragraph("DANH SÁCH NHÂN VIÊN", title_style))
            elements.append(Paragraph(f"Ngày xuất: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
            
            employees = self.manager_ctrl.get_all_employees()
            employees.sort(key=lambda x: x.employee_id)
            
            data = [['ID', 'Họ tên', 'Email', 'Phòng ban', 'Chức vụ', 'Lương (VND)', 'Trạng thái']]
            
            for emp in employees:
                data.append([
                    str(emp.employee_id),
                    emp.full_name,
                    emp.email or "",
                    emp.department or "",
                    emp.position or "",
                    f"{emp.salary:,.0f}" if emp.salary else "",
                    emp.status
                ])
            
            table = Table(data, colWidths=[0.6*inch, 1.8*inch, 1.8*inch, 1.2*inch, 1.5*inch, 1.2*inch, 1*inch])
            
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f6aa5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            elements.append(table)
            doc.build(elements)
            
            messagebox.showinfo("Thành công", f"Đã export file: {filename}")
            
        except ImportError:
            messagebox.showerror("Lỗi", "Vui lòng cài đặt ReportLab:\npip install reportlab")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể export PDF: {str(e)}")
    
    # ================================================
    # MANAGER SYSTEM WORKSPACE
    # ================================================
    def show_manager_system_workspace(self):
        self.clear_window()
        self.system_ctrl.set_current_user(self.current_user)
        
        header = ctk.CTkFrame(self, height=60, fg_color="#16a085")
        header.pack(fill="x", side="top")
        
        ctk.CTkLabel(
            header,
            text="🔧 MANAGER - QUẢN LÝ HỆ THỐNG NGOÀI",
            font=("Arial Bold", 18),
            text_color="white"
        ).pack(side="left", padx=20, pady=15)
        
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S - %d/%m/%Y")
        self.time_label = ctk.CTkLabel(
            header,
            text=time_str,
            font=("Arial", 14),
            text_color="white"
        )
        self.time_label.pack(side="left", padx=20)
        
        ctk.CTkButton(
            header,
            text="Đăng xuất",
            width=100,
            command=self.show_welcome_screen
        ).pack(side="right", padx=20)
        
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_frame = ctk.CTkFrame(main, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0,20))
        
        ctk.CTkLabel(
            title_frame,
            text="🔧 DANH SÁCH HỆ THỐNG BÊN NGOÀI",
            font=("Arial Bold", 24)
        ).pack(side="left")
        
        ctk.CTkButton(
            title_frame,
            text="📄 Export PDF",
            width=120,
            height=35,
            command=self.export_systems_pdf
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            title_frame,
            text="➕ Thêm đối tác",
            width=150,
            height=35,
            command=self.show_add_system_dialog
        ).pack(side="right", padx=10)
        
        table_frame = ctk.CTkFrame(main)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("ID", "Tên hệ thống", "Loại", "Endpoint", "Trạng thái")
        self.system_tree = ttk.Treeview(table_frame, columns=columns, show="tree headings", height=15)
        
        self.system_tree.heading("#0", text="")
        for col in columns:
            self.system_tree.heading(col, text=col)
        
        self.system_tree.column("#0", width=0, stretch=False)
        self.system_tree.column("ID", width=50)
        self.system_tree.column("Tên hệ thống", width=250)
        self.system_tree.column("Loại", width=150)
        self.system_tree.column("Endpoint", width=400)
        self.system_tree.column("Trạng thái", width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.system_tree.yview)
        self.system_tree.configure(yscrollcommand=scrollbar.set)
        
        self.system_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        systems = self.system_ctrl.get_all_systems()
        systems.sort(key=lambda x: x.system_id)
        
        for sys in systems:
            self.system_tree.insert("", "end", values=(
                sys.system_id,
                sys.system_name,
                sys.get_type_display(),
                sys.api_endpoint,
                sys.get_status_display()
            ))
        
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10,0))
        
        ctk.CTkButton(btn_frame, text="🔄 Cập nhật trạng thái", command=self.update_system_status).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Xóa đối tác", command=self.delete_system).pack(side="left", padx=5)
    
    def show_add_system_dialog(self):
        """Add system dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Thêm đối tác mới")
        dialog.geometry("500x500")
        
        dialog.update()
        dialog.after(100, lambda: dialog.grab_set())
        
        form = ctk.CTkFrame(dialog)
        form.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(form, text="THÊM ĐỐI TÁC MỚI", font=("Arial Bold", 18)).pack(pady=15)
        
        ctk.CTkLabel(form, text="* Tên hệ thống:", font=("Arial", 12)).pack(anchor="w", pady=(10,5))
        name_entry = ctk.CTkEntry(form, width=450)
        name_entry.pack(pady=(0,10))
        
        ctk.CTkLabel(form, text="* Loại:", font=("Arial", 12)).pack(anchor="w", pady=(0,5))
        type_var = ctk.StringVar(value="Payment")
        type_menu = ctk.CTkOptionMenu(form, width=450, values=["Payment", "CreditCheck", "ExchangeRate", "Other"], variable=type_var)
        type_menu.pack(pady=(0,10))
        
        ctk.CTkLabel(form, text="Endpoint:", font=("Arial", 12)).pack(anchor="w", pady=(0,5))
        endpoint_entry = ctk.CTkEntry(form, width=450, placeholder_text="https://api.example.com")
        endpoint_entry.pack(pady=(0,10))
        
        ctk.CTkLabel(form, text="API Key:", font=("Arial", 12)).pack(anchor="w", pady=(0,5))
        key_entry = ctk.CTkEntry(form, width=450)
        key_entry.pack(pady=(0,10))
        
        ctk.CTkLabel(form, text="Mô tả:", font=("Arial", 12)).pack(anchor="w", pady=(0,5))
        desc_entry = ctk.CTkEntry(form, width=450)
        desc_entry.pack(pady=(0,10))
        
        error_label = ctk.CTkLabel(form, text="", text_color="red")
        error_label.pack(pady=5)
        
        def save():
            success, msg = self.system_ctrl.add_system(
                system_name=name_entry.get(),
                system_type=type_var.get(),
                api_endpoint=endpoint_entry.get() or None,
                api_key=key_entry.get() or None,
                description=desc_entry.get() or None
            )
            
            if success:
                messagebox.showinfo("Thành công", msg)
                dialog.destroy()
                self.show_manager_system_workspace()
            else:
                error_label.configure(text=msg)
        
        ctk.CTkButton(form, text="💾 Lưu", width=200, height=40, command=save).pack(pady=20)
    
    def update_system_status(self):
        """Update system status"""
        selection = self.system_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hệ thống")
            return
        
        system_id = self.system_tree.item(selection[0])['values'][0]
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Cập nhật trạng thái")
        dialog.geometry("400x250")
        
        dialog.update()
        dialog.after(100, lambda: dialog.grab_set())
        
        ctk.CTkLabel(dialog, text="Chọn trạng thái mới:", font=("Arial Bold", 14)).pack(pady=20)
        
        status_var = ctk.StringVar(value="Active")
        
        for status in ["Active", "Inactive", "Maintenance"]:
            ctk.CTkRadioButton(dialog, text=status, variable=status_var, value=status).pack(pady=5)
        
        def save_status():
            success, msg = self.system_ctrl.update_system(system_id, status=status_var.get())
            if success:
                messagebox.showinfo("Thành công", msg)
                dialog.destroy()
                self.show_manager_system_workspace()
            else:
                messagebox.showerror("Lỗi", msg)
        
        ctk.CTkButton(dialog, text="💾 Cập nhật", width=150, height=40, command=save_status).pack(pady=20)
    
    def delete_system(self):
        selection = self.system_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hệ thống")
            return
        
        system_id = self.system_tree.item(selection[0])['values'][0]
        system_name = self.system_tree.item(selection[0])['values'][1]
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa đối tác '{system_name}' không?"):
            success, msg = self.system_ctrl.delete_system(system_id)
            if success:
                messagebox.showinfo("Thành công", msg)
                self.show_manager_system_workspace()
            else:
                messagebox.showerror("Lỗi", msg)
    
    def export_systems_pdf(self):
        """Export systems to PDF"""
        try:
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from datetime import datetime
            
            filename = f"DanhSachHeThong_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
            elements = []
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#16a085'),
                spaceAfter=30,
                alignment=1
            )
            
            elements.append(Paragraph("DANH SÁCH HỆ THỐNG BÊN NGOÀI", title_style))
            elements.append(Paragraph(f"Ngày xuất: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
            
            systems = self.system_ctrl.get_all_systems()
            systems.sort(key=lambda x: x.system_id)
            
            data = [['ID', 'Tên hệ thống', 'Loại', 'API Endpoint', 'Trạng thái']]
            
            for sys in systems:
                data.append([
                    str(sys.system_id),
                    sys.system_name,
                    sys.get_type_display(),
                    sys.api_endpoint or "N/A",
                    sys.get_status_display()
                ])
            
            table = Table(data, colWidths=[0.6*inch, 2*inch, 1.5*inch, 3.5*inch, 1.2*inch])
            
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16a085')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            elements.append(table)
            doc.build(elements)
            
            messagebox.showinfo("Thành công", f"Đã export file: {filename}")
            
        except ImportError:
            messagebox.showerror("Lỗi", "Vui lòng cài đặt ReportLab:\npip install reportlab")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể export PDF: {str(e)}")
    
    # ================================================
    # UTILITIES
    # ================================================
    def clear_window(self):
        """Clear all widgets"""
        for widget in self.winfo_children():
            widget.destroy()


# ================================================
# RUN APPLICATION
# ================================================
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = BankManagementApp()
    app.mainloop()