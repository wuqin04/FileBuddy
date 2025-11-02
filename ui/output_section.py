import customtkinter as ctk
import os

class OutputSection(ctk.CTkFrame):
    def __init__(self, parent, browse_output):
        super().__init__(parent, corner_radius=12)

        self.grid_columnconfigure(0, weight=1)

        self.output_label = ctk.CTkLabel(self, text="📁 Save organized files to this folder:", font=("Inter", 14))
        self.output_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

        self.output_entry = ctk.CTkEntry(self, placeholder_text="Select your organized files folder")
        self.output_entry.grid(row=1, column=0, padx=15, pady=10, sticky="ew")

         # get the default's Downloads folder and set it to default
        default_download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        if os.path.exists(default_download_path):
            self.output_entry.insert(0, default_download_path)    
        else:
            self.output_entry.insert(0, "")


        self.output_button = ctk.CTkButton(self, text="Browse", width=100, command=browse_output)
        self.output_button.grid(row=1, column=1, padx=15, pady=10)