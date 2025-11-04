import customtkinter as ctk
from customtkinter import filedialog
import os
from utils.config_manager import load_config, save_config
from utils.file_types_manager import load_file_types, save_file_types
from utils.subject_manager import load_subjects, save_subjects
from ui.sections import TargetFolderSection, OutputSection, OptionSection, ThemeSection

class OrganizerTab(ctk.CTkFrame):
    def __init__(self, master, log_callback):
        super().__init__(master)

        self.log_callback = log_callback
        self.config_data = load_config()
        ctk.set_appearance_mode(self.config_data["theme"])

        self.grid_rowconfigure(8, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- TOP BAR (Header + Theme Switch) ---
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=40, pady=(20, 10))
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=0)

        # --- HEADER ---
        self.header_label = ctk.CTkLabel(self.top_frame, text="👋 Welcome! Let's keep your computer tidy today.", 
                                         font=("Inter", 18, "bold"))
        self.header_label.grid(row=0, column=0, sticky="w")

        # --- Theme Selection ---
        self.theme_frame = ThemeSection(self.top_frame, self.toggle_theme, self.config_data["theme"])
        self.theme_frame.grid(row=0, column=1, sticky="e")

        # --- Download Section ---
        self.download_frame = TargetFolderSection(self, self.browse_download)
        self.download_frame.grid(row=1, column=0, sticky="ew", padx=40, pady=8)

        # --- Output Section ---
        self.output_frame = OutputSection(self, self.browse_output)
        self.output_frame.grid(row=2, column=0, sticky="ew", padx=40, pady=8)

        # --- Options Section ---
        self.option_frame = OptionSection(self, self.open_file_type_manager, self.open_subject_manager)
        self.option_frame.grid(row=3, column=0, sticky="ew", padx=40, pady=8)

        # --- START BUTTON ---
        self.start_button = ctk.CTkButton(self, text="Start Organizing!", height=40, width=200, font=("Inter", 16, "bold"), command=self.start_sorting)
        self.start_button.grid(row=4, column=0, pady=(10, 10))

        # --- LOG BOX ---
        self.log_title = ctk.CTkLabel(self, text="📜 Activity Log", font=("Inter", 14, "bold"))
        self.log_title.grid(row=5, column=0, sticky="w", padx=45, pady=(8, 0))
        self.log_box = ctk.CTkTextbox(self, height=180, corner_radius=12)
        self.log_box.grid(row=6, column=0, sticky="nsew", padx=40, pady=(0, 8))
        
        # configure log message color code
        self.log_box.tag_config("warning", foreground="#E6B800")   # yellow for warnings
        self.log_box.tag_config("error", foreground="#FF4D4D")     # red for critical

        self.log_message("Start organizing your folders or files!\n")

        # --Progression Bar Section---
        self.progress_index = None

    # --- FUNCTIONS ---
    def browse_download(self):
        download_path = filedialog.askdirectory(title="Select your Downloads folder")
        if download_path:
            self.download_frame.download_entry.delete(0, "end")
            self.download_frame.download_entry.insert(0, download_path)
            self.log_message(f"Download directory is set to: {download_path}")

            self.config_data["last_download_path"] = download_path
            save_config(self.config_data)

        if not os.path.exists(download_path):
            self.log_message("⚠️ Selected folder does not exist.", "warning")
            return

    def browse_output(self):
        output_path = filedialog.askdirectory(title="Select your Organized folder")
        if output_path:
            self.output_frame.output_entry.delete(0, "end")
            self.output_frame.output_entry.insert(0, output_path)
            self.log_message(f"Output directory is set to: {output_path}")

            self.config_data["last_output_path"] = output_path
            save_config(self.config_data)

        if not os.path.exists(output_path):
            self.log_message("⚠️ Selected folder does not exist.", "warning")
            return

    def open_subject_manager(self):
        win = ctk.CTkToplevel(self)
        win.title("Manage Subjects")
        win.geometry("360x450")
        win.resizable(False, False)
        win.transient(self.winfo_toplevel())
        win.grab_set()
        win.focus_force()
        win.lift()

        subjects = load_subjects()

        # --- HEADER ---
        title = ctk.CTkLabel(win, text="Manage Your Subjects", font=("Inter", 16, "bold"))
        title.pack(pady=(15, 5))

        desc = ctk.CTkLabel(win, text="Add or remove subjects to personalize sorting", font=("Inter", 12))
        desc.pack(pady=(0, 10))

        # --- SCROLLABLE LIST ---
        list_frame = ctk.CTkScrollableFrame(win, width=320, height=260)
        list_frame.pack(pady=(0, 10), fill="both", expand=True)

        def refresh_list():
            # Rebuild the scrollable list of subjects
            for widget in list_frame.winfo_children():
                widget.destroy()

            if not subjects:
                empty = ctk.CTkLabel(list_frame, text="No subjects added yet.", font=("Inter", 12, "italic"))
                empty.pack(pady=20)
                return

            for sub in subjects:
                row = ctk.CTkFrame(list_frame, fg_color="transparent")
                row.pack(fill="x", padx=5, pady=2)

                # Checkbox (include toggle)
                include_var = ctk.BooleanVar(value=sub.get("include", True))

                def toggle_include(var=include_var, s=sub):
                    s["include"] = var.get()
                    save_subjects(subjects)
                    self.log_message(f"{'✅' if var.get() else '🚫'} Sorting status updated for: {s['name']}")

                chk = ctk.CTkCheckBox(row, text=sub["name"], variable=include_var, command=toggle_include)
                chk.pack(side="left", padx=10, pady=3)

                # Delete button
                del_btn = ctk.CTkButton(
                    row,
                    text="🗑",
                    width=40,
                    height=28,
                    fg_color="#e63946",
                    hover_color="#d62839",
                    command=lambda s=sub: delete_subject(s)
                )
                del_btn.pack(side="right", padx=5)

        def delete_subject(sub):
            subjects.remove(sub)
            save_subjects(subjects)
            self.log_message(f"🗑️ Removed subject: {sub['name']}")
            refresh_list()

        # --- ADD SUBJECT POPUP ---
        def open_add_popup():
            popup = ctk.CTkToplevel(win)
            popup.title("Add New Subject")
            popup.geometry("300x160")
            popup.resizable(False, False)
            popup.transient(win)
            popup.grab_set()

            ctk.CTkLabel(popup, text="Enter new subject name or subject code:", font=("Inter", 13)).pack(pady=(15, 5))
            entry = ctk.CTkEntry(popup, placeholder_text="e.g. Programming, FHMM1024", width=200)
            entry.pack(pady=(0, 10), padx=30)

            def add_subject():
                sub_name = entry.get().strip()
                if not sub_name:
                    return

                # Ensure backward compatibility with old list format
                if any(
                    (s["name"].lower() if isinstance(s, dict) else s.lower()) == sub_name.lower()
                    for s in subjects
                ):
                    self.log_message(f"⚠️ {sub_name} already exists.")
                    popup.destroy()
                    return

                # Always append in new structured format
                new_subject = {"name": sub_name, "include": True}
                subjects.append(new_subject)
                save_subjects(subjects)
                refresh_list()
                self.log_message(f"✅ Added new subject: {sub_name}")
                popup.destroy()

            ctk.CTkButton(popup, text="Add Subject", command=add_subject).pack(pady=10)

        # --- FOOTER BUTTONS ---
        add_btn = ctk.CTkButton(win, text="➕ Add Subject", height=35, command=open_add_popup)
        add_btn.pack(pady=(5, 5))

        close_btn = ctk.CTkButton(win, text="Close", height=35, command=win.destroy)
        close_btn.pack(pady=(0, 10))

        # Build initial list
        refresh_list()

    def open_file_type_manager(self):
        src_folder = self.download_frame.download_entry.get().strip()

        if not os.path.exists(src_folder) or not os.path.isdir(src_folder):
            self.log_message("⚠️ Invalid or missing source folder.", "warning")
            return

        # --- Create popup window ---
        win = ctk.CTkToplevel(self)
        win.title("Manage File Types")
        win.geometry("360x450")
        win.resizable(False, False)
        win.transient(self.winfo_toplevel())
        win.grab_set()
        win.focus_force()
        win.lift()

        label = ctk.CTkLabel(win, text="Select which file types to organize:", font=("Inter", 14, "bold"))
        label.pack(pady=(15, 10))

        # --- Detect available extensions in source folder ---
        exts = set()
        for f in os.listdir(src_folder):
            path = os.path.join(src_folder, f)
            if os.path.isfile(path):
                ext = os.path.splitext(f)[1].lower()
                if ext:
                    exts.add(ext)
        exts = sorted(exts)

        if not exts:
            ctk.CTkLabel(win, text="No file types found.", text_color="gray").pack(pady=20)
            return
        
        # --- Load saved file type settings ---
        saved_types = load_file_types()  # dict like {".pdf": True, ".docx": False, ...}

        # --- Store checkbox states ---
        ext_vars = {}
        for ext in exts:
            ext_vars[ext] = ctk.BooleanVar(value=saved_types.get(ext, True))  # default True if not saved

        # --- Scrollable frame for checkboxes ---
        scroll_frame = ctk.CTkScrollableFrame(win, width=280, height=250)
        scroll_frame.pack(pady=(0, 10))

        for ext in exts:
            chk = ctk.CTkCheckBox(scroll_frame, text=ext.upper(), variable=ext_vars[ext])
            chk.pack(anchor="w", padx=10, pady=2)

        # --- Footer buttons ---
        def save_selection():
            # Save updated checkbox states
            updated = {ext: var.get() for ext, var in ext_vars.items()}
            save_file_types(updated)
            self.log_message("💾 File type preferences saved.")
            win.destroy()

        save_btn = ctk.CTkButton(win, text="Save & Close", command=save_selection)
        save_btn.pack(pady=(5, 5))

        cancel_btn = ctk.CTkButton(win, text="Cancel", fg_color="gray", command=win.destroy)
        cancel_btn.pack(pady=(0, 10))

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
            file_types = load_file_types()
            selected_exts = [ext.lstrip(".") for ext, enabled in file_types.items() if enabled]

            if not selected_exts:
                self.log_message("⚠️ No file types selected for sorting. Please manage file types first.", "warning")
                return
            
            self.organize_by_type(download_path, output_path, selected_exts)
        elif mode == "subject":
            self.organize_by_subject(download_path, output_path)

        self.log_message("✅ All files have been organized successfully!\n")

    def organize_by_type(self, src_folder, dst_folder, selected_exts=None):
        screenshot_patterns = ["screenshot", "screen_shot", "screen shot", "snip", "capture", "截图"]

        files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]
        total = len(files)
        if total == 0:
            self.log_message("⚠️ No files found to organize.", "warning")
            return
        
        if selected_exts:
            selected_exts = [ext.lower() for ext in selected_exts]
            files = [f for f in files if os.path.splitext(f)[1][1:].lower() in selected_exts]
            total = len(files)
            if total == 0:
                self.log_message("⚠️ No matching files found for selected types.", "warning")
                return

        self.log_box.configure(state="normal")
        self.log_box.insert("end", "\n📊 Progress Bar (Organizing Files)\n")
        self.log_box.insert("end", "\n[░░░░░░░░░░░░░░░░░░░░] 0%\n")
        self.progress_index = self.log_box.index("end-2l")  # store progress bar index
        self.log_box.configure(state="disabled")
        self.log_box.update_idletasks()

        for i, file in enumerate(files, start=1):
            file_path = os.path.join(src_folder, file)
            ext = os.path.splitext(file)[1][1:].strip().lower()
            if not ext:
                continue

            if any(keyword in file.lower() for keyword in screenshot_patterns):
                dest_folder = os.path.join(dst_folder, "Screenshots")
            else:
                dest_folder = os.path.join(dst_folder, ext.upper())

            os.makedirs(dest_folder, exist_ok=True)

            try:
                os.rename(file_path, os.path.join(dest_folder, file))
                self.log_message(f"📦 Moved {file} → {dest_folder}")
            except Exception as e:
                self.log_message(f"⚠️ Failed to move {file}: {e}", "warning")

            self.update_text_progress(i, total)

    def organize_by_subject(self, src_folder, dst_folder):
        subjects = load_subjects()

        files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]
        total = len(files)
        if total == 0:
            self.log_message("⚠️ No files found to organize.", "warning")
            return

        self.log_box.configure(state="normal")
        self.log_box.insert("end", "\n📊 Progress Bar (Organizing Files)\n")
        self.log_box.insert("end", "\n[░░░░░░░░░░░░░░░░░░░░] 0%\n")
        self.progress_index = self.log_box.index("end-2l")  # Store position of progress bar
        self.log_box.configure(state="disabled")
        self.log_box.update_idletasks()

        # --- Start organizing files ---
        for i, file in enumerate(files, start=1):
            file_path = os.path.join(src_folder, file)
            moved = False

            for subject in subjects:
                # Skip subjects that are not marked as included
                if not subject.get("include", True):
                    continue

                sub_name = subject["name"]
                if sub_name.lower() in file.lower():
                    dest_folder = os.path.join(dst_folder, sub_name)
                    os.makedirs(dest_folder, exist_ok=True)
                    try:
                        os.rename(file_path, os.path.join(dest_folder, file))
                        self.log_message(f"📦 Moved {file} → {sub_name}")
                        moved = True
                        break
                    except Exception as e:
                        self.log_message(f"⚠️ Failed to move {file}: {e}", "warning")

            if not moved:
                self.log_message(f"Skipped {file} (no subject match)")

            self.update_text_progress(i, total)

    def log_message(self, message, level="info"):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n", level)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")        

    def update_text_progress(self, current, total):
        bar_length = 20  # Number of boxes in the bar
        progress = current / total
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        percent = int(progress * 100)

        # Move to the stored index where progress was inserted
        self.log_box.configure(state="normal")
        self.log_box.delete(self.progress_index, f"{self.progress_index} lineend")
        self.log_box.insert(self.progress_index, f"[{bar}] {percent}%")
        self.log_box.configure(state="disabled")
        self.log_box.update_idletasks()

    def toggle_theme(self):
        current = ctk.get_appearance_mode().lower()
        new_mode = "dark" if current == "light" else "light"
        ctk.set_appearance_mode(new_mode)
        self.config_data["theme"] = new_mode
        save_config(self.config_data)
        self.log_message(f"✅ {new_mode.capitalize()} theme has successfully updated.")