import customtkinter as ctk
from tkinter import filedialog

ctk.set_appearance_mode("System")  # Light/Dark mode auto
ctk.set_default_color_theme("blue")  # Soft blue accent

class SmartDeskApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧠 SmartDesk — Your Study File Helper")
        self.geometry("750x600")
        self.resizable(False, False)

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        # --- HEADER ---
        self.header_label = ctk.CTkLabel(self, text="👋 Welcome! Let's keep your computer tidy today.", font=("Inter", 18, "bold"))
        self.header_label.grid(row=0, column=0, pady=(20, 10))

        # --- DOWNLOAD FOLDER ---
        self.download_frame = ctk.CTkFrame(self, corner_radius=12)
        self.download_frame.grid(row=1, column=0, sticky="ew", padx=40, pady=10)
        self.download_frame.grid_columnconfigure(0, weight=1)

        self.download_label = ctk.CTkLabel(self.download_frame, text="📁 Where are your downloads?", font=("Inter", 14))
        self.download_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

        self.download_entry = ctk.CTkEntry(self.download_frame, placeholder_text="Select your downloads folder")
        self.download_entry.grid(row=1, column=0, padx=15, pady=10, sticky="ew")

        self.download_button = ctk.CTkButton(self.download_frame, text="Browse", width=100, command=self.browse_download)
        self.download_button.grid(row=1, column=1, padx=15, pady=10)

        # --- OUTPUT FOLDER ---
        self.output_frame = ctk.CTkFrame(self, corner_radius=12)
        self.output_frame.grid(row=2, column=0, sticky="ew", padx=40, pady=10)
        self.output_frame.grid_columnconfigure(0, weight=1)

        self.output_label = ctk.CTkLabel(self.output_frame, text="🗂️ Where should I organize your files?", font=("Inter", 14))
        self.output_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

        self.output_entry = ctk.CTkEntry(self.output_frame, placeholder_text="Select your organized files folder")
        self.output_entry.grid(row=1, column=0, padx=15, pady=10, sticky="ew")

        self.output_button = ctk.CTkButton(self.output_frame, text="Browse", width=100, command=self.browse_output)
        self.output_button.grid(row=1, column=1, padx=15, pady=10)

        # --- ORGANIZATION OPTIONS ---
        self.option_frame = ctk.CTkFrame(self, corner_radius=12)
        self.option_frame.grid(row=3, column=0, sticky="ew", padx=40, pady=10)

        self.option_label = ctk.CTkLabel(self.option_frame, text="⚙️ Organize by:", font=("Inter", 14, "bold"))
        self.option_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))

        self.mode_var = ctk.StringVar(value="type")
        self.radio1 = ctk.CTkRadioButton(self.option_frame, text="File type (PDF, DOCX, etc.)", variable=self.mode_var, value="type")
        self.radio2 = ctk.CTkRadioButton(self.option_frame, text="Subject keywords (Math, Physics, etc.)", variable=self.mode_var, value="subject")
        self.radio1.grid(row=1, column=0, sticky="w", padx=20, pady=2)
        self.radio2.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 10))

        # --- START BUTTON ---
        self.start_button = ctk.CTkButton(self, text="Start Organizing 🚀", height=40, width=200, font=("Inter", 16, "bold"), command=self.start_sorting)
        self.start_button.grid(row=4, column=0, pady=(10, 10))

        # --- LOG BOX ---
        self.log_box = ctk.CTkTextbox(self, height=180, corner_radius=12)
        self.log_box.grid(row=5, column=0, sticky="nsew", padx=40, pady=(0, 10))
        self.log_box.insert("end", "Ready to go!\n")

        # --- THEME SWITCH ---
        self.theme_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.theme_frame.grid(row=6, column=0, pady=(5, 20))

        self.theme_switch = ctk.CTkSwitch(
            self.theme_frame,
            text="🌙 Dark Mode",
            font=("Inter", 13),
            command=self.toggle_theme
        )
        self.theme_switch.grid(row=0, column=0, pady=10)

    # --- FUNCTIONS ---
    def browse_download(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_entry.delete(0, "end")
            self.download_entry.insert(0, folder)

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, folder)

    def start_sorting(self):
        download_path = self.download_entry.get()
        output_path = self.output_entry.get()
        mode = self.mode_var.get()

        if not download_path or not output_path:
            self.log_box.insert("end", "⚠️ Please select both folders before starting.\n")
            return

        self.log_box.insert("end", f"🚀 Started organizing by {mode}...\n")
        self.log_box.see("end")

        # (File organization logic will be added later)

    def toggle_theme(self):
        mode = ctk.get_appearance_mode()
        if mode == "Light":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")


if __name__ == "__main__":
    app = SmartDeskApp()
    app.mainloop()
