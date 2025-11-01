import customtkinter as ctk

class OptionSection(ctk.CTkFrame):
    def __init__(self, parent, open_subject_manager_callback):
        super().__init__(parent, corner_radius=12)
        self.grid_columnconfigure(0, weight=1)

        # --- ORGANIZE BY OPTIONS ---
        self.option_label = ctk.CTkLabel(
            self,
            text="⚙️ Organize by:",
            font=("Inter", 14, "bold")
        )
        self.option_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))

        self.mode_var = ctk.StringVar(value="type")

        self.radio1 = ctk.CTkRadioButton(
            self,
            text="File type (PDF, DOCX, etc.)",
            variable=self.mode_var,
            value="type"
        )
        self.radio1.grid(row=1, column=0, sticky="w", padx=20, pady=2)

        self.radio2 = ctk.CTkRadioButton(
            self,
            text="Subject keywords (Math, Physics, etc.)",
            variable=self.mode_var,
            value="subject"
        )
        self.radio2.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 5))

        self.subject_button = ctk.CTkButton(self, text="Manage Subjects", height=35, width=180, command=open_subject_manager_callback)
        self.subject_button.grid(row=2, column=1, padx=(10, 15), pady=(0, 5), sticky="w")
    def get_mode(self):
        return self.mode_var.get()
