from ui.download_section import DownloadSection
from ui.output_section import OutputSection
from ui.option_section import OptionSection
from ui.theme_selection import ThemeSection
from utils.subject_manager import load_subjects, save_subjects
import customtkinter as ctk
from customtkinter import filedialog
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class FileBuddy(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧠 FileBuddy — Your Study File Helper")
        self.geometry("800x700")
        self.resizable(False, False)

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        # --- HEADER ---
        self.header_label = ctk.CTkLabel(self, text="👋 Welcome! Let's keep your computer tidy today.", 
                                         font=("Inter", 18, "bold"))
        self.header_label.grid(row=0, column=0, pady=(20, 10))

        # --- Download Section ---
        self.download_frame = DownloadSection(self, self.browse_download)
        self.download_frame.grid(row=1, column=0, sticky="ew", padx=40, pady=10)

        # --- Output Section ---
        self.output_frame = OutputSection(self, self.browse_output)
        self.output_frame.grid(row=2, column=0, sticky="ew", padx=40, pady=10)

        # --- Options Section ---
        self.option_frame = OptionSection(self, self.open_subject_manager)
        self.option_frame.grid(row=3, column=0, sticky="ew", padx=40, pady=10)

        # --- START BUTTON ---
        self.start_button = ctk.CTkButton(self, text="Start Organizing 🚀", height=40, width=200, font=("Inter", 16, "bold"), command=self.start_sorting)
        self.start_button.grid(row=4, column=0, pady=(10, 10))

        # --- LOG BOX ---
        self.log_box = ctk.CTkTextbox(self, height=180, corner_radius=12)
        self.log_box.grid(row=5, column=0, sticky="nsew", padx=40, pady=(0, 10))
        
        # configure log message color code
        self.log_box.tag_config("warning", foreground="#e6b800")   # yellow for warnings
        self.log_box.tag_config("error", foreground="#ff4d4d")     # red for critical

        self.log_message("Start organizing your folders or files!\n")

        # --- Theme Selection ---
        self.theme_frame = ThemeSection(self, self.toggle_theme)
        self.theme_frame.grid(row=6, column=0, pady=(5, 20))

    # --- FUNCTIONS ---
    def browse_download(self):
        download_path = filedialog.askdirectory(title="Select your Downloads folder")
        if download_path:
            self.download_frame.download_entry.delete(0, "end")
            self.download_frame.download_entry.insert(0, download_path)
            self.log_message(f"Download directory is set to: {download_path}")

        if not os.path.exists(download_path):
            self.log_message("⚠️ Selected folder does not exist.", "warning")
            return

    def browse_output(self):
        output_path = filedialog.askdirectory(title="Select your Organized folder")
        if output_path:
            self.output_frame.output_entry.delete(0, "end")
            self.output_frame.output_entry.insert(0, output_path)
            self.log_message(f"Output directory is set to: {output_path}")

        if not os.path.exists(output_path):
            self.log_message("⚠️ Selected folder does not exist.", "warning")
            return

    def open_subject_manager(self):
        win = ctk.CTkToplevel(self)
        win.title("Manage Subjects")
        win.geometry("350x400")
        win.resizable(False, False)

        win.transient(self)
        win.grab_set()
        win.focus_force()
        win.lift()

        subjects = load_subjects()

        title = ctk.CTkLabel(win, text="Your Subjects", font=("Inter", 16, "bold"))
        title.pack(pady=10)

        subject_box = ctk.CTkTextbox(win, width=300, height=220)
        subject_box.pack(pady=5)
        subject_box.insert("end", "\n".join(subjects))

        entry = ctk.CTkEntry(win, placeholder_text="Add or remove subject...")
        entry.pack(pady=5)

        def refresh_box():
            subject_box.delete("1.0", "end")
            subject_box.insert("end", "\n".join(subjects))

        def add_subject():
            sub = entry.get().strip()
            if sub and sub not in subjects:
                subjects.append(sub)
                save_subjects(subjects)
                refresh_box()
                entry.delete(0, "end")
                self.log_message(f"✅ Added new subject: {sub}")

        def delete_subject():
            sub = entry.get().strip()
            if sub in subjects:
                subjects.remove(sub)
                save_subjects(subjects)
                refresh_box()
                entry.delete(0, "end")
                self.log_message(f"🗑️ Removed subject: {sub}")

        add_btn = ctk.CTkButton(win, text="Add", command=add_subject)
        add_btn.pack(pady=(5, 2))

        del_btn = ctk.CTkButton(win, text="Delete", command=delete_subject)
        del_btn.pack(pady=(0, 10))

        close_btn = ctk.CTkButton(win, text="Close", command=win.destroy)
        close_btn.pack(pady=(10, 5))

    def start_sorting(self):
        self.log_message("Initializing to sort your files and folders...")
        
        download_path = self.download_frame.download_entry.get().strip()
        output_path = self.output_frame.output_entry.get().strip()

        if not output_path or download_path:
            self.log_message("⚠️ Path is not found, either your download path or organized path is not specified.", "warning")

        if not os.path.exists(download_path) or not os.path.isdir(download_path):
            self.log_message("⚠️ Folder does not exists or is not a folder path.", "warning")
            return
        
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path, exist_ok=True)
                self.log_message(f"📁 Created output folder at: {output_path}")
            except Exception as e:
                self.log_message(f"❌ Failed to create output folder: {e}", "error")

        self.log_message(f"🚀 Organizing files from {download_path} → {output_path}")
        
        mode = self.option_frame.mode_var.get()

        self.log_message(f"Starting organization in '{mode}' mode...")
        
        if mode == "type":
            self.organize_by_type(download_path, output_path)
        elif mode == "subject":
            self.organize_by_subject(download_path)

        self.log_message("✅ All files have been organized successfully!\n")

    def organize_by_type(self, src_folder, dst_folder):
        for file in os.listdir(src_folder):
            src_file = os.path.join(src_folder, file)
            if os.path.isfile(src_file):
                ext = os.path.splitext(file)[1][1:].strip().lower()
                if not ext:
                    continue
                dest_folder = os.path.join(dst_folder, ext.upper())
                os.makedirs(dest_folder, exist_ok=True)
                try:
                    os.rename(src_file, os.path.join(dest_folder, file))
                    self.log_message(f"📦 Moved {file} → {dest_folder}")
                except Exception as e:
                    self.log_message(f"⚠️ Failed to move {file}: {e}", "warning")

    def organize_by_subject(self, folder):
        subjects = load_subjects()

        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                moved = False
                for subject in subjects:
                    if subject.lower() in file.lower():
                        dest_folder = os.path.join(folder, subject)
                        os.makedirs(dest_folder, exist_ok=True)
                        try:
                            os.rename(file_path, os.path.join(dest_folder, file))
                            self.log_message(f"📦 Moved {file} → {subject}/")
                            moved = True
                            break
                        except Exception as e:
                            self.log_message(f"⚠️ Failed to move {file}: {e}", "warning")
                if not moved:
                    self.log_message(f"Skipped {file} (no subject match)")


    def log_message(self, message, level="info"):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n", level)
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
