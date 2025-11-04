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

class OutputSection(ctk.CTkFrame):
    def __init__(self, parent, browse_output):
        super().__init__(parent, corner_radius=12)

        self.grid_columnconfigure(0, weight=1)

        self.output_label = ctk.CTkLabel(self, text="📁 Choose the folder you want to save:", font=("Inter", 14))
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
    
class OptionSection(ctk.CTkFrame):
    def __init__(self, parent, open_file_type_manager_callback, open_subject_manager_callback):
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

        self.type_button = ctk.CTkButton(self, text="Manage File Types", height=35, width=180, command=open_file_type_manager_callback)
        self.type_button.grid(row=1, column=1, padx=(10,15), pady=(0, 5), sticky="w")
        
        self.subject_button = ctk.CTkButton(self, text="Manage Subjects", height=35, width=180, command=open_subject_manager_callback)
        self.subject_button.grid(row=2, column=1, padx=(10, 15), pady=(0, 5), sticky="w")

    def get_mode(self):
        return self.mode_var.get()

class ThemeSection(ctk.CTkFrame):
    def __init__(self, parent, toggle_callback, current_theme="light"):
        super().__init__(parent, fg_color="transparent")

        self.theme_switch = ctk.CTkSwitch(
            self,
            text="🌙 Dark Mode",
            font=("Inter", 13),
            command=toggle_callback
        )
        self.theme_switch.grid(row=0, column=0, pady=10)

        if current_theme.lower() == "light":
            self.theme_switch.deselect()
        else:
            self.theme_switch.select()
