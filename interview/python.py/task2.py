import tkinter as tk
import winreg
import ctypes
import sys

def is_admin():
    """Check if script is running as administrator"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-run script with admin privileges"""
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def disable_usb():
    """Disables USB ports"""
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\USBSTOR", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 4)  # 4 = Disabled
        winreg.CloseKey(key)
        status_label.config(text="USB Ports Disabled!", fg="red")
    except PermissionError:
        status_label.config(text="Run as Administrator!", fg="red")

def enable_usb():
    """Enables USB ports"""
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\USBSTOR", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 3)  # 3 = Enabled
        winreg.CloseKey(key)
        status_label.config(text="USB Ports Enabled!", fg="green")
    except PermissionError:
        status_label.config(text="Run as Administrator!", fg="red")

# Ensure Admin Privileges
run_as_admin()

# Tkinter GUI
root = tk.Tk()
root.title("USB Port Control")
root.geometry("300x150")

tk.Button(root, text="Disable USB", command=disable_usb, fg="white", bg="red").pack(pady=10)
tk.Button(root, text="Enable USB", command=enable_usb, fg="white", bg="green").pack(pady=10)
status_label = tk.Label(root, text="Status: Ready", fg="blue")
status_label.pack()

root.mainloop()
