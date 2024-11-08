import threading
from flask import Flask, request, jsonify
import tkinter as tk
from tkinter import messagebox
import win32print
import win32ui
import json
import os
import time
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Đường dẫn tới file lưu trữ máy in đã chọn
PRINTER_CONFIG_FILE = 'printer_config.json'

# Global variable to store selected printer
selected_printer = None

# Hàm để lấy danh sách máy in
def get_printers():
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
    return [printer[2] for printer in printers]

# Hàm kiểm tra kết nối máy in
def check_printer_connection(printer_name):
    try:
        # Thử mở máy in để kiểm tra kết nối
        printer_handle = win32print.OpenPrinter(printer_name)
        status = win32print.GetPrinter(printer_handle, 2)
        # Kiểm tra xem máy in có trong trạng thái "Ready" hay không
        if status['Status'] & win32print.PRINTER_STATUS_READY:
            return True
        else:
            return False
    except Exception as e:
        return False

# Hàm hiển thị giao diện Tkinter để chọn máy in
def show_printer_dialog():
    global selected_printer
    printers = get_printers()

    def on_select():
        global selected_printer
        selected_printer = printer_listbox.get(tk.ACTIVE)
        
        # Lưu máy in đã chọn vào file config
        with open(PRINTER_CONFIG_FILE, 'w') as f:
            json.dump({"printer": selected_printer}, f)

        root.quit()  # Đóng cửa sổ Tkinter khi chọn xong máy in

    root = tk.Tk()
    root.title("Chọn Máy In")

    label = tk.Label(root, text="Chọn Máy In:")
    label.pack(pady=10)

    printer_listbox = tk.Listbox(root)
    for printer in printers:
        printer_listbox.insert(tk.END, printer)
    printer_listbox.pack(pady=10)

    select_button = tk.Button(root, text="Chọn", command=on_select)
    select_button.pack(pady=20)

    root.mainloop()  # Khởi chạy Tkinter

# Hàm in lệnh với máy in đã chọn
def print_job(printer_name, content):
    if not check_printer_connection(printer_name):
        messagebox.showerror("Lỗi", "Chưa kết nối máy in.")
        return

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
        messagebox.showerror("Lỗi khi in", f"Lỗi khi in: {e}")

# Đọc máy in đã chọn từ file config
def load_selected_printer():
    global selected_printer
    if os.path.exists(PRINTER_CONFIG_FILE):
        with open(PRINTER_CONFIG_FILE, 'r') as f:
            config = json.load(f)
            selected_printer = config.get("printer")


@app.route('/print', methods=['POST'])
def print_order():
    # return "in thành công"
    global selected_printer

    # Nếu chưa có máy in đã chọn, yêu cầu người dùng chọn máy in
    if not selected_printer:
        # Hiển thị màn hình chọn máy in nếu chưa có máy in đã chọn
        show_printer_dialog()

    if not selected_printer:
        return jsonify({"error": "Không có máy in nào được chọn."}), 400

    # Nhận dữ liệu từ yêu cầu HTTP (nội dung HTML)
    data = request.get_json()
    print_content = data.get('content', '')

    try:
        # Gửi lệnh in đến máy in đã chọn
        print_job(selected_printer, print_content)
        return jsonify({"message": "Đơn hàng đã được in!"})
    except Exception as e:
        return jsonify({"error": f"Lỗi khi in: {str(e)}"}), 500

# Chạy Flask server trong một thread riêng biệt
def run_flask():
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)  # Tắt reloader

if __name__ == '__main__':
    # Đọc máy in đã chọn từ file
    load_selected_printer()

    # Nếu chưa có máy in, hiển thị giao diện để chọn
    if not selected_printer:
        show_printer_dialog()

    # Chạy Flask server trong một thread riêng biệt
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Cho phép dừng Flask khi đóng ứng dụng
    flask_thread.start()

    # Đảm bảo rằng Flask và Tkinter không cản trở nhau
    time.sleep(2)  # Đảm bảo Flask server có thời gian để khởi động trước khi tương tác với Tkinter

    # Flask đã chạy trong background, bây giờ có thể làm các tác vụ Tkinter hoặc các tác vụ khác
    messagebox.showinfo("Thông Báo", "Ứng dụng đang chạy. Mở HTML và bấm nút In Đơn để thử nghiệm.")
