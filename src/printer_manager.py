import win32print
import win32ui
from tkinter import messagebox

# Hàm để lấy máy in mặc định
def get_default_printer():
    try:
        default_printer = win32print.GetDefaultPrinter()
        return default_printer
    except Exception as e:
        messagebox.showerror("Error", f"Lỗi khi lấy máy in mặc định: {e}")
        return None

# Hàm để in lệnh lên máy in
def print_job(printer_name, content):
    try:
        # Mở máy in và chuẩn bị in
        printer_handle = win32print.OpenPrinter(printer_name)
        print_dc = win32ui.CreateDC()
        print_dc.CreatePrinterDC(printer_name)
        print_dc.StartDoc("In Lệnh từ Web")
        print_dc.StartPage()

        # In nội dung
        print_dc.TextOut(100, 100, content)

        print_dc.EndPage()
        print_dc.EndDoc()
        print_dc.DeleteDC()
    except Exception as e:
        messagebox.showerror("Error", f"Lỗi khi in: {e}")
