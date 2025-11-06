import customtkinter as ctk
from tkinter import filedialog
from utils.config_manager import load_config, save_config
import os, hashlib
from tkinter import messagebox
from send2trash import send2trash

class ToolTip:
    active_tip = None

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        # Destroy any existing tooltip
        if ToolTip.active_tip:
            try:
                ToolTip.active_tip.destroy()
            except:
                pass
            ToolTip.active_tip = None

        # Create new tooltip
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tip_window = tw = ctk.CTkToplevel(self.widget)
        ToolTip.active_tip = tw  # track it globally
        tw.wm_overrideredirect(True)
        tw.geometry(f"+{x}+{y}")

        label = ctk.CTkLabel(
            tw, text=self.text, justify="left",
            fg_color="#333", corner_radius=6,
            text_color="white", font=("Inter", 11)
        )
        label.pack(ipadx=6, ipady=3)

    def hide(self, event=None):
        if self.tip_window:
            try:
                self.tip_window.destroy()
            except:
                pass
            self.tip_window = None
        if ToolTip.active_tip:
            ToolTip.active_tip = None

    @staticmethod
    def hide_all():
        if ToolTip.active_tip:
            try:
                ToolTip.active_tip.destroy()
            except:
                pass
            ToolTip.active_tip = None

class DuplicateScannerTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.duplicates = {}
        self.file_check_vars = {}

        # --- Grid config for responsiveness ---
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- HEADER ---
        self.header_label = ctk.CTkLabel(
            self,
            text="🔍 Find and Manage Duplicate Files",
            font=("Inter", 18, "bold")
        )
        self.header_label.grid(row=0, column=0, pady=(20, 10))

        # --- Folder Selection ---
        self.folder_frame = ctk.CTkFrame(self)
        self.folder_frame.grid(row=1, column=0, sticky="ew", padx=40, pady=(10, 5))
        self.folder_frame.grid_columnconfigure(0, weight=1)

        self.config_data = load_config()
        default_folder = self.config_data.get("last_scan_path", "")
        self.folder_path_var = ctk.StringVar(value=default_folder)
        self.folder_entry = ctk.CTkEntry(self.folder_frame, textvariable=self.folder_path_var, placeholder_text="Select a folder to scan...")
        self.folder_entry.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=10)

        self.browse_btn = ctk.CTkButton(self.folder_frame, text="Browse", width=100, command=self.browse_folder)
        self.browse_btn.grid(row=0, column=1, padx=(5, 10), pady=10)

        # --- Scan Button ---
        self.scan_btn = ctk.CTkButton(
            self, 
            text="Start Scanning for Duplicates", 
            height=40, 
            width=220, 
            font=("Inter", 16, "bold"),
            command=self.start_scan
        )
        self.scan_btn.grid(row=2, column=0, pady=(10, 15))

        # --- Results List---
        self.result_title = ctk.CTkLabel(self, text="📂 Duplicate Files Found", font=("Inter", 14, "bold"))
        self.result_title.grid(row=3, column=0, sticky="w", padx=45, pady=(10, 0))

        self.result_frame = ctk.CTkScrollableFrame(self, height=250, corner_radius=12)
        self.result_frame.grid(row=4, column=0, sticky="nsew", padx=40, pady=(0, 10))

        # --- Action Buttons ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=5, column=0, pady=(5, 10))

        self.remove_selected_btn = ctk.CTkButton(
            self.action_frame, 
            text="🗑️ Remove Selected", 
            width=160, 
            state="disabled",
            command=self.delete_selected_files
        )
        self.remove_selected_btn.grid(row=0, column=0, padx=5)

        self.remove_all_btn = ctk.CTkButton(
            self.action_frame,
            text="⚠️ Remove All Duplicates",
            width=180,
            state="disabled",
            fg_color="#D9534F",
            hover_color="#C9302C",
            command=self.delete_all_duplicates
        )
        self.remove_all_btn.grid(row=0, column=1, padx=5)

        # --- Log Box ---
        self.log_title = ctk.CTkLabel(self, text="🧾 Scanner Log", font=("Inter", 14, "bold"))
        self.log_title.grid(row=6, column=0, sticky="w", padx=45, pady=(10, 0))

        self.log_box = ctk.CTkTextbox(self, height=120, corner_radius=12)
        self.log_box.grid(row=7, column=0, sticky="nsew", padx=40, pady=(0, 20))
        self.log_message("Ready to scan for duplicate files.\n")

        self.log_box.tag_config("warning", foreground="#E6B800")
        self.log_box.tag_config("error", foreground="#FF4D4D")

        root = self.winfo_toplevel()
        def on_mousewheel(event):
            ToolTip.hide_all()     # hide any visible tooltip
            return None            # allow the scroll event to propagate normally

        root.bind_all("<MouseWheel>", on_mousewheel, add="+")


    # ---FUNCTIONS---
    def browse_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder to Scan")
        if folder_path:
            # Update entry field
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder_path)
            self.log_message(f"📁 Folder set to: {folder_path}")

            # Save to configs
            self.config_data["last_scan_path"] = folder_path
            save_config(self.config_data)

        # Validate the folder path
        if not folder_path or not os.path.exists(folder_path):
            self.log_message("⚠️ Selected folder does not exist.", "warning")
            return


    def start_scan(self):
        folder = self.folder_path_var.get().strip()
        if not folder or not os.path.exists(folder):
            self.log_message("⚠️ Please select a valid folder first.\n", "warning")
            return

        self.log_message(f"🔍 Scanning folder: {folder}\n")
        duplicates = self.scan_for_duplicates(folder)
        self.duplicates = duplicates

        self.display_duplicates(duplicates)

        if duplicates:
            self.remove_selected_btn.configure(state="normal")
            self.remove_all_btn.configure(state="normal")
            self.log_message("✅ Scan complete. Duplicates listed.\n")
        else:
            self.log_message("✨ No duplicates found!\n")

    def scan_for_duplicates(self, folder):
        size_map = {}
        hash_map = {}
        duplicates = {}

        # Step 1: Group files by size
        for root, _, files in os.walk(folder):
            for file in files:
                try:
                    path = os.path.join(root, file)
                    size = os.path.getsize(path)
                    size_map.setdefault(size, []).append(path)
                except Exception as e:
                    self.log_message(f"⚠️ Failed to read {file}: {e}\n", "warning")

        # Step 2: For each group with >1 file, compute hashes
        for size, paths in size_map.items():
            if len(paths) < 2:
                continue

            for path in paths:
                try:
                    file_hash = self.hash_file(path)
                    hash_map.setdefault(file_hash, []).append(path)
                except Exception as e:
                    self.log_message(f"⚠️ Hash error for {path}: {e}\n", "warning")

        # Step 3: Collect duplicates
        for file_hash, files in hash_map.items():
            if len(files) > 1:
                duplicates[file_hash] = files

        return duplicates

    def hash_file(self, filepath, block_size=65536):
        hasher = hashlib.md5()
        with open(filepath, "rb") as f:
            while chunk := f.read(block_size):
                hasher.update(chunk)
        return hasher.hexdigest()

    def display_duplicates(self, duplicates):
        for widget in self.result_frame.winfo_children():
            widget.destroy()  # Clear old results

        self.file_check_vars.clear()

        if not duplicates:
            label = ctk.CTkLabel(self.result_frame, text="🎉 No duplicates found.", font=("Inter", 13))
            label.pack(pady=5)
            return

        for hash_val, files in duplicates.items():
            group_label = ctk.CTkLabel(
                self.result_frame,
                text=f"🔁 Duplicate Group (hash={hash_val[:8]}...):",
                font=("Inter", 13, "bold")
            )
            group_label.pack(anchor="w", padx=10, pady=(5, 0))

            for f in files:
                var = ctk.IntVar()
                self.file_check_vars[f] = var
                # Truncate the display text if it's too long
                max_len = 70
                if len(f) <= max_len:
                    display_name = f
                else:
                    display_name = "..." + f[-(max_len - 3):]

                cb = ctk.CTkCheckBox(self.result_frame, text=display_name, variable=var)
                cb.pack(anchor="w", padx=30, pady=2)

                # Tooltip to show full path on hover
                ToolTip(cb, f)

    def refresh_file_list(self):
        """Refresh the duplicate file list display after deletions."""
        # Filter out deleted files
        remaining_duplicates = {
            h: [f for f in files if os.path.exists(f)]
            for h, files in self.duplicates.items()
            if any(os.path.exists(f) for f in files)
        }

        # Update stored duplicates
        self.duplicates = remaining_duplicates

        # Rebuild the checkboxes / display
        self.display_duplicates(remaining_duplicates)
        self.log_message("♻️ Refreshed file list after deletion.\n")

    def delete_selected_files(self):
        selected_files = [file for file, var in self.file_check_vars.items() if var.get() == 1]

        if not selected_files:
            messagebox.showinfo("No Selection", "Please select at least one file to delete.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", 
                                    f"Are you sure you want to delete {len(selected_files)} selected file(s)?\n"
                                    "They will be moved to the Recycle Bin.")
        if not confirm:
            return

        deleted, failed = 0, 0
        for file_path in selected_files:
            try:
                file_path = os.path.normpath(file_path)
                if os.path.exists(file_path):
                    send2trash(file_path)
                    deleted += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"⚠️ Failed to delete {file_path}: {e}")
                failed += 1

        # Feedback message
        messagebox.showinfo("Deletion Complete", 
                            f"✅ {deleted} file(s) moved to Recycle Bin.\n"
                            f"⚠️ {failed} failed or missing files.")

        # Remove deleted ones from UI
        for file_path in selected_files:
            if file_path in self.file_check_vars:
                del self.file_check_vars[file_path]

        self.refresh_file_list()

    def delete_all_duplicates(self):
        if not self.duplicates:
            messagebox.showinfo("No Duplicates", "There are no duplicates to remove.")
            return

        confirm = messagebox.askyesno(
            "Confirm Mass Deletion",
            "⚠️ This will remove all duplicate copies, keeping only one file from each group.\n"
            "All removed files will be moved to the Recycle Bin.\n\n"
            "Proceed?"
        )
        if not confirm:
            return

        deleted, failed = 0, 0

        for hash_val, files in self.duplicates.items():
            to_delete = files[1:] if len(files) > 1 else []
            for file_path in to_delete:
                try:
                    # --- Normalize file path properly ---
                    abs_path = os.path.abspath(os.path.normpath(file_path))

                    # --- Extra safety: check existence ---
                    if not os.path.exists(abs_path):
                        self.log_message(f"⚠️ File not found: {abs_path}\n", "warning")
                        failed += 1
                        continue

                    # --- Attempt deletion ---
                    send2trash(abs_path)
                    deleted += 1
                    self.log_message(f"🗑️ Sent to Recycle Bin: {abs_path}\n")

                except Exception as e:
                    import traceback
                    error_info = traceback.format_exc()
                    self.log_message(f"❌ Failed to delete {file_path}\nReason: {e}\nDetails: {error_info}\n", "error")
                    failed += 1

        self.refresh_file_list()

        messagebox.showinfo(
            "Mass Deletion Complete",
            f"✅ {deleted} duplicate file(s) moved to Recycle Bin.\n"
            f"⚠️ {failed} failed or missing files."
        )

        self.log_message(f"🗑️ Deleted {deleted} duplicates, {failed} failed.\n")


        
    def log_message(self, message, tag=None):
        self.log_box.configure(state="normal")
        if tag:
            self.log_box.insert("end", message, tag)
        else:
            self.log_box.insert("end", message)
        self.log_box.configure(state="disabled")
        self.log_box.see("end")
