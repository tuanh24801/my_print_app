import tkinter as tk
from tkinter import ttk
from printer_manager import load_printers

def create_gui(root):
    # Tạo combobox để chọn máy in
    printer_combobox = ttk.Combobox(root)
    printer_combobox['values'] = load_printers()
    printer_combobox.pack(pady=10)
    
    return printer_combobox
