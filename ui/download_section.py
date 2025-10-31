import customtkinter as ctk

class DownloadSection(ctk.CTkFrame):
    def __init__(self, parent, browse_callback):
        super().__init__(parent, corner_radius=12)
        self.grid_columnconfigure(0, weight=1)

        self.download_label = ctk.CTkLabel(self, text="📁 Where are your downloads?", font=("Inter", 14))
        self.download_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

        self.download_entry = ctk.CTkEntry(self, placeholder_text="Select your downloads folder")
        self.download_entry.grid(row=1, column=0, padx=15, pady=10, sticky="ew")

        self.download_button = ctk.CTkButton(self, text="Browse", width=100, command=browse_callback)
        self.download_button.grid(row=1, column=1, padx=15, pady=10)

        
