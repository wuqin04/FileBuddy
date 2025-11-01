from ui.download_section import DownloadSection
from ui.output_section import OutputSection
from ui.option_section import OptionSection
from ui.theme_selection import ThemeSection
import customtkinter as ctk
from customtkinter import filedialog
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class FileBuddy(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧠 SmartDesk — Your Study File Helper")
        self.geometry("800x700")
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

        # ---Output Section---
        self.output_frame = OutputSection(self, self.browse_output)
        self.output_frame.grid(row=2, column=0, sticky="ew", padx=40, pady=10)

        # ---Options Section---
        self.option_frame = OptionSection(self)
        self.option_frame.grid(row=3, column=0, sticky="ew", padx=40, pady=10)

        # --- START BUTTON ---
        self.start_button = ctk.CTkButton(self, text="Start Organizing 🚀", height=40, width=200, font=("Inter", 16, "bold"), command=self.start_sorting)
        self.start_button.grid(row=4, column=0, pady=(10, 10))

        # --- LOG BOX ---
        self.log_box = ctk.CTkTextbox(self, height=180, corner_radius=12)
        self.log_box.grid(row=5, column=0, sticky="nsew", padx=40, pady=(0, 10))
        self.log_message("Start organizing your folders or files!\n")

        # ---Theme Selection---
        self.theme_frame = ThemeSection(self, self.toggle_theme)
        self.theme_frame.grid(row=6, column=0, pady=(5, 20))

    # ---FUNCTIONS---
    def browse_download(self):
        print("Browsing download directory...")
        download_path = filedialog.askdirectory(title="Select your Downloads folder")
        if download_path:
            self.download_frame.download_entry.delete(0, "end")
            self.download_frame.download_entry.insert(0, download_path)
            self.log_message(f"Download directory is set to: {download_path}")

        if not os.path.exists(download_path):
            self.log_message("⚠️ Selected folder does not exist.")
            return

    def browse_output(self):
        output_path = filedialog.askdirectory(title="Select your Organized folder")
        if output_path:
            self.output_frame.output_entry.delete(0, "end")
            self.output_frame.output_entry.insert(0, output_path)
            self.log_message(f"Output directory is set to: {output_path}")

        if not os.path.exists(output_path):
            self.log_message("⚠️ Selected folder does not exist.")
            return

    # TODO: implement sorting logic
    def start_sorting(self):
        self.log_message("Initializing to sort your files and folders...")
        
        download_path = self.download_frame.download_entry.get().strip()

        if not os.path.exists(download_path):
            self.log_message("⚠️ Folder does not exist. Please check the path.")
            return
        
        if not os.path.isdir(download_path):
            self.log_message("⚠️ The path is not a folder, select again.")
            return
        
        mode = self.option_frame.mode_var.get()

        self.log_message(f"Starting organization in '{mode}' mode...")
        
        if mode == "type":
            self.organize_by_type(download_path)
        elif mode == "subject":
            self.organize_by_subject(download_path)

        self.log_message("✅ Organizing complete!\n")

    # TODO: Organize the files by type
    def organize_by_type(self, folder):
        pass
    
    # TODO: Organize the files by subject
    def organize_by_subject(self, folder):
        pass

    def log_message(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")        

    def toggle_theme(self):
        mode = ctk.get_appearance_mode()
        if mode == "Light":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

if __name__ == "__main__":
    app = FileBuddy()
    app.mainloop()
