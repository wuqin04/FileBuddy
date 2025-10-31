from ui.download_section import DownloadSection
from ui.option_section import OptionSection
from ui.theme_selection import ThemeSection
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class FileBuddy(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧠 SmartDesk — Your Study File Helper")
        self.geometry("700x600")
        self.resizable(False, False)

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        # ---HEADER---
        self.header_label = ctk.CTkLabel(self, text="👋 Welcome! Let's keep your computer tidy today.", 
                                         font=("Inter", 18, "bold"))
        self.header_label.grid(row=0, column=0, pady=(20, 10))

        # ---Download Section---
        self.download_frame = DownloadSection(self, self.browse_download)
        self.download_frame.grid(row=1, column=0, sticky="ew", padx=40, pady=10)

        # ---Options Section---
        self.option_frame = OptionSection(self)
        self.option_frame.grid(row=3, column=0, sticky="ew", padx=40, pady=10)

        # --- START BUTTON ---
        self.start_button = ctk.CTkButton(self, text="Start Organizing 🚀", height=40, width=200, font=("Inter", 16, "bold"), command=self.start_sorting)
        self.start_button.grid(row=4, column=0, pady=(10, 10))

        # --- LOG BOX ---
        self.log_box = ctk.CTkTextbox(self, height=180, corner_radius=12)
        self.log_box.grid(row=5, column=0, sticky="nsew", padx=40, pady=(0, 10))
        self.log_box.insert("end", "Ready to go!\n")

        # ---Theme Selection---
        self.theme_frame = ThemeSection(self, self.toggle_theme)
        self.theme_frame.grid(row=6, column=0, pady=(5, 20))

    # ---FUNCTIONS---
    def browse_download(self):
        print("Browsing directory...")
        pass

    def start_sorting(self):
        print("Starting to sort...")
        pass

    def toggle_theme(self):
        mode = ctk.get_appearance_mode()
        if mode == "Light":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

if __name__ == "__main__":
    app = FileBuddy()
    app.mainloop()