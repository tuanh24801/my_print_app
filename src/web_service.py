import requests
from bs4 import BeautifulSoup
from tkinter import messagebox

# Hàm nhận lệnh in từ file HTML
def get_print_job_from_web():
    try:
        # Đọc nội dung từ file HTML
        with open("test_print.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        
        # Sử dụng BeautifulSoup để trích xuất văn bản từ HTML
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Trích xuất nội dung văn bản
        print_content = soup.get_text()
        
        return print_content
    except Exception as e:
        messagebox.showerror("Error", f"Lỗi khi tải file HTML: {e}")
        return None
