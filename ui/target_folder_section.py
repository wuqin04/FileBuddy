import customtkinter as ctk
import os

class TargetFolderSection(ctk.CTkFrame):
    def __init__(self, parent, browse_callback, log_callback=None):
        super().__init__(parent, corner_radius=12)
        self.grid_columnconfigure(0, weight=1)
        self.log_callback = log_callback
        

        self.download_label = ctk.CTkLabel(self, text="📁 Choose the folder you want to organize: ", font=("Inter", 14))
        self.download_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

        self.download_entry = ctk.CTkEntry(self, placeholder_text="Select a folder to manage")
        self.download_entry.grid(row=1, column=0, padx=15, pady=10, sticky="ew")

        # get the default's Downloads folder and set it to default
        default_download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        if os.path.exists(default_download_path):
            self.download_entry.insert(0, default_download_path)    
        else:
            self.download_entry.insert(0, "")

        self.download_button = ctk.CTkButton(self, text="Browse", width=100, command=browse_callback)
        self.download_button.grid(row=1, column=1, padx=15, pady=10)

        
