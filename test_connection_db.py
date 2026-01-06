"""
Test connection to SQL Server from Python
"""
import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from .env
server = os.getenv('DB_SERVER', 'localhost')
database = os.getenv('DB_DATABASE', 'BankSystemOOP')
username = os.getenv('DB_USER', 'SA')
password = os.getenv('DB_PASSWORD')
driver = os.getenv('DB_DRIVER', 'ODBC Driver 18 for SQL Server')
trust_cert = os.getenv('DB_TRUST_CERT', 'yes')

# Build connection string
conn_str = (
    f'DRIVER={{{driver}}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    f'TrustServerCertificate={trust_cert};'
)

print("==============================================")
print("TESTING PYTHON → SQL SERVER CONNECTION")
print("==============================================")
print(f"Server: {server}")
print(f"Database: {database}")
print(f"Username: {username}")
print("-" * 46)

try:
    # Connect to database
    print("\n[1/4] Connecting to SQL Server...")
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("  ✓ Connection successful!")
    
    # Test 1: Get SQL Server version
    print("\n[2/4] Getting SQL Server version...")
    cursor.execute("SELECT @@VERSION AS Version")
    row = cursor.fetchone()
    version_info = row.Version.split('\n')[0]  # First line only
    print(f"  ✓ {version_info[:80]}...")
    
    # Test 2: Verify database
    print("\n[3/4] Verifying database...")
    cursor.execute("SELECT DB_NAME() AS CurrentDB")
    row = cursor.fetchone()
    print(f"  ✓ Current Database: {row.CurrentDB}")
    
    # Test 3: List tables
    print("\n[4/4] Listing tables...")
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
    """)
    
    tables = cursor.fetchall()
    print(f"  ✓ Found {len(tables)} tables:")
    
    for idx, table in enumerate(tables, 1):
        print(f"     {idx:2d}. {table.TABLE_NAME}")
    
    # Test 4: Count records in key tables
    print("\n[5/5] Checking sample data...")
    
    test_tables = ['Roles', 'Users', 'Employees', 'Customers', 'CreditLoans', 'ExternalSystems']
    
    for table in test_tables:
        try:
            cursor.execute(f"SELECT COUNT(*) AS cnt FROM {table}")
            row = cursor.fetchone()
            print(f"  ✓ {table:20s}: {row.cnt:3d} records")
        except:
            print(f"  ✗ {table:20s}: Table not found or empty")
    
    # Close connection
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 46)
    print("✓ ALL TESTS PASSED!")
    print("Python can connect to SQL Server successfully")
    print("=" * 46)
    
except pyodbc.Error as e:
    print("\n" + "=" * 46)
    print("✗ DATABASE CONNECTION ERROR!")
    print("=" * 46)
    print(f"\nError Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    print("\nPossible solutions:")
    print("  1. Check SQL Server is running:")
    print("     systemctl status mssql-server")
    print("  2. Check password in .env file")
    print("  3. Check ODBC driver installed:")
    print("     odbcinst -q -d")
    
except ModuleNotFoundError as e:
    print("\n" + "=" * 46)
    print("✗ MODULE NOT FOUND ERROR!")
    print("=" * 46)
    print(f"\nMissing module: {e}")
    print("\nInstall missing packages:")
    print("  pip install pyodbc python-dotenv")
    
except Exception as e:
    print("\n" + "=" * 46)
    print("✗ UNEXPECTED ERROR!")
    print("=" * 46)
    print(f"\nError: {str(e)}")
    print(f"Type: {type(e).__name__}")

print()