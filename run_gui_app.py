import tkinter as tk
from tkinter import messagebox
import subprocess
import webbrowser
import os
import shutil
import time
import threading
import sys

# Constants
DJANGO_PORT = "8000"
URL = f"http://127.0.0.1:{DJANGO_PORT}/"

# Use full Python path to support PyInstaller .exe
PYTHON_EXE = sys.executable
DJANGO_COMMAND = [PYTHON_EXE, "manage.py", "runserver"]

# Paths
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(PROJECT_DIR, "media")
FINAL_OUTPUT = os.path.join(MEDIA_DIR, "final_output")
LOGO_DIR = os.path.join(MEDIA_DIR, "logos")
GENERATED_DOCS = os.path.join(MEDIA_DIR, "generated_docs")

def check_server_running():
    try:
        import requests
        return requests.get(URL, timeout=1).status_code == 200
    except:
        return False

def start_server():
    def server_thread():
        try:
            with open("server_log.txt", "w") as log_file:
                log_file.write("Starting server...\n")
                log_file.write(f"Project Dir: {PROJECT_DIR}\n")
                log_file.write(f"Python Executable: {PYTHON_EXE}\n")

                if check_server_running():
                    log_file.write("Server already running.\n")
                    webbrowser.open(URL)
                    messagebox.showinfo("Server Running", "Django server is already running!")
                    return

                creation_flags = 0
                if os.name == 'nt':
                    creation_flags = subprocess.CREATE_NEW_CONSOLE

                server_process = subprocess.Popen(
                    DJANGO_COMMAND,
                    cwd=PROJECT_DIR,
                    creationflags=creation_flags,
                    stdout=log_file,
                    stderr=log_file,
                    text=True
                )

                start_time = time.time()
                while True:
                    if check_server_running():
                        webbrowser.open(URL)
                        messagebox.showinfo("Server Started", f"Django server started at:\n{URL}")
                        return

                    if time.time() - start_time > 30:
                        server_process.kill()
                        messagebox.showerror("Timeout", "Server failed to start within 30 seconds.")
                        return

                    time.sleep(1)

        except Exception as e:
            with open("server_log.txt", "a") as log_file:
                log_file.write(f"Exception: {str(e)}\n")
            messagebox.showerror("Startup Error", f"Error occurred. Check server_log.txt.")

    threading.Thread(target=server_thread, daemon=True).start()

def open_output_folder():
    path = os.path.abspath(FINAL_OUTPUT)
    if os.path.exists(path):
        os.startfile(path)
    else:
        messagebox.showwarning("Missing Folder", "Output folder not found yet.")

def cleanup_cache():
    try:
        for path in [FINAL_OUTPUT, LOGO_DIR, GENERATED_DOCS]:
            if os.path.exists(path):
                shutil.rmtree(path)
        messagebox.showinfo("Cleanup Done", "Cache and old folders cleaned up.")
    except Exception as e:
        messagebox.showerror("Cleanup Error", str(e))

# GUI
app = tk.Tk()
app.title("NIC Document Generator")
app.geometry("400x350")
app.configure(bg="#f7f7f7")

tk.Label(
    app,
    text="NIC Documentation Desktop Launcher",
    font=("Segoe UI", 14, "bold"),
    bg="#f7f7f7"
).pack(pady=20)

tk.Button(
    app,
    text="🚀 Start Django Server",
    width=30,
    height=2,
    bg="#4CAF50",
    fg="white",
    command=start_server
).pack(pady=10)

tk.Button(
    app,
    text="📁 Open Final Output Folder",
    width=30,
    height=2,
    command=open_output_folder
).pack(pady=10)

tk.Button(
    app,
    text="🧹 Cleanup Cache (media/)",
    width=30,
    height=2,
    bg="#f44336",
    fg="white",
    command=cleanup_cache
).pack(pady=10)

tk.Button(
    app,
    text="Exit",
    width=30,
    command=app.quit
).pack(pady=20)

app.mainloop()
