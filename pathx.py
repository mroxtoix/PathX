import os
import sys
import ctypes
import subprocess
import webbrowser
import tkinter as tk
import customtkinter as ctk

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ix.pathx.tool.1.0")
except Exception:
    pass

ctk.set_appearance_mode("Dark")

BG_MAIN = "#0B0F19"
BG_CARD = "#131C2E"
BG_INPUT = "#1B263B"
BLUE_PRIMARY = "#007ACC"
BLUE_HOVER = "#005999"
BLUE_GLOW = "#3399FF"
TEXT_WHITE = "#F5F5F7"
TEXT_MUTED = "#8A99AD"


class PathXApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PathX - Windows Persistence & Path Inspector")
        self.geometry("850x520")
        self.resizable(False, False)
        self.configure(fg_color=BG_MAIN)
        self.current_path = ""

     
        self.icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons8-star-100.ico")
        if os.path.exists(self.icon_path):
            try:
                self.iconbitmap(self.icon_path)
            except Exception:
                try:
                    ico = tk.PhotoImage(file=self.icon_path)
                    self.iconphoto(True, ico)
                except Exception:
                    pass

        self._build_ui()
        self.load_path(self.get_special_paths()["Startup (User)"])

    def _build_ui(self):
        sidebar = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, width=220, border_width=1, border_color="#1F2E4D")
        sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            sidebar, text="PathX",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=BLUE_GLOW
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            sidebar, text="Sensitive Paths Inspector",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=TEXT_MUTED
        ).pack(pady=(0, 20))

        paths_dict = self.get_special_paths()
        for name, path_val in paths_dict.items():
            btn = ctk.CTkButton(
                sidebar, text=name, height=36, anchor="w",
                fg_color="transparent", hover_color="#1A2A47",
                text_color=TEXT_WHITE, font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                command=lambda p=path_val: self.load_path(p)
            )
            btn.pack(fill="x", padx=12, pady=3)

        main_area = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=0)
        main_area.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        top_bar = ctk.CTkFrame(main_area, fg_color=BG_CARD, corner_radius=10, height=45, border_width=1, border_color="#1F2E4D")
        top_bar.pack(fill="x", pady=(0, 10))

        self.path_entry = ctk.CTkEntry(
            top_bar, height=32, fg_color=BG_INPUT, border_color="#2A3E66",
            text_color=TEXT_WHITE, font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=10, pady=6)
        self.path_entry.configure(state="readonly")

        open_folder_btn = ctk.CTkButton(
            top_bar, text="Open in Explorer", width=120, height=32,
            fg_color=BLUE_PRIMARY, hover_color=BLUE_HOVER,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self.open_current_in_explorer
        )
        open_folder_btn.pack(side="right", padx=10)

        self.file_list_box = ctk.CTkTextbox(
            main_area, fg_color=BG_CARD, text_color=TEXT_WHITE,
            corner_radius=10, border_width=1, border_color="#1F2E4D",
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.file_list_box.pack(fill="both", expand=True, pady=(0, 10))

      
        self.right_click_menu = tk.Menu(self, tearoff=0, bg="#131C2E", fg="#F5F5F7", activebackground="#007ACC", activeforeground="#FFFFFF")
        self.right_click_menu.add_command(label="🔄 Refresh", command=self.refresh_current_view)

        self.file_list_box.bind("<Button-3>", self.show_context_menu)

        footer = ctk.CTkFrame(main_area, fg_color="transparent", height=30)
        footer.pack(fill="x")

        self.status_label = ctk.CTkLabel(
            footer, text="Status: Ready | Dev: ix",
            font=ctk.CTkFont(family="Segoe UI", size=11), text_color=TEXT_MUTED
        )
        self.status_label.pack(side="left")

        
        about_btn = ctk.CTkButton(
            footer, text="About", width=80, height=26,
            fg_color="#1B263B", hover_color=BLUE_PRIMARY,
            text_color=TEXT_WHITE, font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            command=self.open_about_dialog
        )
        about_btn.pack(side="right")

    def show_context_menu(self, event):
        try:
            self.right_click_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.right_click_menu.grab_release()

    def refresh_current_view(self):
        if self.current_path:
            self.load_path(self.current_path)

    def open_about_dialog(self):
        about_win = ctk.CTkToplevel(self)
        about_win.title("About PathX")
        about_win.geometry("380x260")
        about_win.resizable(False, False)
        about_win.configure(fg_color=BG_MAIN)
        about_win.grab_set()

     
        if os.path.exists(self.icon_path):
            try:
                about_win.iconbitmap(self.icon_path)
            except Exception:
                try:
                    ico = tk.PhotoImage(file=self.icon_path)
                    about_win.iconphoto(True, ico)
                except Exception:
                    pass

        ctk.CTkLabel(
            about_win, text="PathX Inspector",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=BLUE_GLOW
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            about_win, text="Windows Persistence & Path Inspector Tool\nDeveloped by ix",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXT_MUTED
        ).pack(pady=(0, 15))

        yt_btn = ctk.CTkButton(
            about_win, text="YouTube Channel", height=35,
            fg_color="#CC0000", hover_color="#990000",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: webbrowser.open("https://youtube.com/@ixlol.1?si=WievwTNzrHV0dWe3")
        )
        yt_btn.pack(fill="x", padx=30, pady=5)

        dc_btn = ctk.CTkButton(
            about_win, text="Discord Server", height=35,
            fg_color="#5865F2", hover_color="#4752C4",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: webbrowser.open("https://discord.gg/WKB")
        )
        dc_btn.pack(fill="x", padx=30, pady=5)

    def get_special_paths(self):
        user_profile = os.environ.get("USERPROFILE", "C:\\Users\\Default")
        appdata = os.environ.get("APPDATA", os.path.join(user_profile, "AppData", "Roaming"))
        localappdata = os.environ.get("LOCALAPPDATA", os.path.join(user_profile, "AppData", "Local"))
        windir = os.environ.get("WINDIR", "C:\\Windows")

        return {
            "Startup (User)": os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs", "Startup"),
            "AppData (Roaming)": appdata,
            "AppData (Local)": localappdata,
            "Temp Files": os.path.join(localappdata, "Temp"),
            "System32": os.path.join(windir, "System32"),
            "Tasks (Scheduled)": "POWERSHELL_SCHEDULED_TASKS",
            "Program Files": os.environ.get("ProgramFiles", "C:\\Program Files"),
        }

    def load_path(self, path):
        self.current_path = path
        self.path_entry.configure(state="normal")
        self.path_entry.delete(0, "end")
        self.path_entry.insert(0, path if path != "POWERSHELL_SCHEDULED_TASKS" else "C:\\Windows\\System32\\Tasks (Root Tasks Only)")
        self.path_entry.configure(state="readonly")

        self.file_list_box.delete("0.0", "end")

        if path == "POWERSHELL_SCHEDULED_TASKS":
            self.load_scheduled_tasks_powershell()
            return

        if not os.path.exists(path):
            self.file_list_box.insert("0.0", "[!] Path does not exist or access denied.")
            self.status_label.configure(text="Status: Error loading path")
            return

        try:
            items = os.listdir(path)
            header = f"{'TYPE':<10} | {'NAME':<45} | {'SIZE / INFO'}\n" + "-"*75 + "\n"
            self.file_list_box.insert("end", header)

            count = 0
            for item in items:
                full_path = os.path.join(path, item)
                item_type = "[DIR]" if os.path.isdir(full_path) else "[FILE]"
                
                info = ""
                if os.path.isfile(full_path):
                    try:
                        size_kb = os.path.getsize(full_path) // 1024
                        info = f"{size_kb} KB"
                    except:
                        info = "N/A"
                else:
                    try:
                        sub_count = len(os.listdir(full_path))
                        info = f"{sub_count} items"
                    except:
                        info = "Protected"

                line = f"{item_type:<10} | {item[:43]:<45} | {info}\n"
                self.file_list_box.insert("end", line)
                count += 1

            self.status_label.configure(text=f"Status: Loaded {count} items successfully.")
        except Exception as e:
            self.file_list_box.insert("end", f"[!] Error reading directory: {str(e)}")
            self.status_label.configure(text="Status: Access Denied / Error")

    def load_scheduled_tasks_powershell(self):
        try:
            self.status_label.configure(text="Status: Fetching Root Scheduled Tasks via PowerShell...")
            self.update_idletasks()

            ps_command = (
                "Get-ScheduledTask | Where-Object { $_.TaskPath -eq '\\' } | ForEach-Object { "
                "Write-Output $_.TaskName "
                "}"
            )

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                startupinfo=startupinfo
            )

            header = f"{'TYPE':<10} | {'ROOT TASK NAME'}\n" + "═" * 65 + "\n"
            self.file_list_box.insert("end", header)

            tasks = [t.strip() for t in result.stdout.strip().split("\n") if t.strip()]
            
            if not tasks:
                self.file_list_box.insert("end", "No tasks found in the root directory.\n")
            else:
                for task in tasks:
                    row = f"{'[ROOT]':<10} | /{task}\n"
                    self.file_list_box.insert("end", row)

            self.status_label.configure(text=f"Status: Loaded {len(tasks)} root scheduled tasks successfully.")
        except Exception as e:
            self.file_list_box.insert("end", f"[!] Error fetching scheduled tasks: {str(e)}")
            self.status_label.configure(text="Status: PowerShell Error")

    def open_current_in_explorer(self):
        if hasattr(self, "current_path") and self.current_path != "POWERSHELL_SCHEDULED_TASKS" and os.path.exists(self.current_path):
            os.startfile(self.current_path)


if __name__ == "__main__":
    app = PathXApp()
    app.mainloop()