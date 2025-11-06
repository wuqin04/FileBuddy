import customtkinter as ctk
import tkinter as tk
from ui.organizer_tab import OrganizerTab
from ui.duplicate_tab import DuplicateScannerTab
from ui.license_dialog import LicenseDialog
from utils import license_manager

class FileBuddy(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🧠 FileBuddy — Your Study File Helper")
        self.geometry("700x720")
        self.resizable(False, False)

        # --- Grid layout for window ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Menu Bar ---
        self.menu_bar = tk.Menu(self)

        # Settings Menu
        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        settings_menu.add_command(label="Activate License", command=self.open_license_dialog)
        settings_menu.add_separator()
        settings_menu.add_command(label="Exit", command=self.destroy)

        # Attach menu
        self.menu_bar.add_cascade(label="⚙️ Settings", menu=settings_menu)
        self.config(menu=self.menu_bar)


        # --- MAIN TABS ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # --- Organizer Tab ---
        organizer_frame = self.tabview.add("🗂️ Organizer")
        organizer_frame.grid_rowconfigure(0, weight=1)
        organizer_frame.grid_columnconfigure(0, weight=1)

        self.organizer_tab = OrganizerTab(organizer_frame, log_callback=self.log_to_console)
        self.organizer_tab.grid(row=0, column=0, sticky="nsew")

        # --- Duplicate Scanner Tab ---
        duplicate_frame = self.tabview.add("🔍 Duplicate Scanner")
        duplicate_frame.grid_rowconfigure(0, weight=1)
        duplicate_frame.grid_columnconfigure(0, weight=1)

        self.duplicate_tab = DuplicateScannerTab(duplicate_frame)
        self.duplicate_tab.grid(row=0, column=0, sticky="nsew")

        status = "Pro" if license_manager.is_pro_user() else "Free"
        self.status_label = ctk.CTkLabel(self, text=f"Account Status: {status}")
        self.status_label.place(x=15, y=10)

    def log_to_console(self, message):
        print(message)

    def open_license_dialog(self):
        LicenseDialog(self)


if __name__ == "__main__":
    app = FileBuddy()
    app.mainloop()
