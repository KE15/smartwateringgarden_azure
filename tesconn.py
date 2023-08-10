import pyodbc
import tesid

# Konfigurasi koneksi dengan detail database Azure SQL
server = 'smart-watering-server.database.windows.net'
database = 'mySWGDatabase'
username = 'SmartWateringGarden'
password = '{Raspberrypi4}' 
driver = '{ODBC Driver 18 for SQL Server}'  # Pastikan driver ini sudah terinstal di sistem Anda

idDevice = tesid.id_Device

# print (idDevice)

# Membangun string koneksi
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # Membuka koneksi
    conn = pyodbc.connect(connection_string)
    
    # Membuat cursor
    cursor = conn.cursor()
    
    # Melakukan query=
    cursor.execute("SELECT A.NoTelp FROM [dbo].[tuser] as A JOIN [dbo].[tdevice] as B ON A.id_User = B.id_User WHERE B.id_Device ='"+ str(idDevice)+"'" )
    
    # Mengambil hasil query
    rows = cursor.fetchall()
    
    # Menampilkan hasil
    for row in rows:
        print(row)
    
    # Menutup cursor dan koneksi
    cursor.close()
    conn.close()

except pyodbc.Error as e:
    # Menangani error
    print(f"Error: {e}")
