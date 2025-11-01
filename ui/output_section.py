import customtkinter as ctk

class OutputSection(ctk.CTkFrame):
    def __init__(self, parent, browse_output):
        super().__init__(parent, corner_radius=12)

        self.grid_columnconfigure(0, weight=1)

        self.output_label = ctk.CTkLabel(self, text="📁 Where should I organize your files?", font=("Inter", 14))
        self.output_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

        self.output_entry = ctk.CTkEntry(self, placeholder_text="Select your organized files folder")
        self.output_entry.grid(row=1, column=0, padx=15, pady=10, sticky="ew")

        self.output_button = ctk.CTkButton(self, text="Browse", width=100, command=browse_output)
        self.output_button.grid(row=1, column=1, padx=15, pady=10)