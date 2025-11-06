# ui/license_dialog.py
import customtkinter as ctk
import tkinter.messagebox as msg
from utils import license_manager

class LicenseDialog(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Activate FileBuddy Pro")
        self.geometry("360x220")
        self.resizable(False, False)

        self.transient(master)
        self.grab_set()
        self.attributes("-topmost", True)


        ctk.CTkLabel(self, text="Email:").pack(pady=(18, 6))
        self.email_entry = ctk.CTkEntry(self, width=300)
        self.email_entry.pack()

        ctk.CTkLabel(self, text="License Key:").pack(pady=(12, 6))
        self.key_entry = ctk.CTkEntry(self, width=300)
        self.key_entry.pack()

        ctk.CTkButton(self, text="Activate", command=self.activate).pack(pady=18)

    def activate(self):
        email = self.email_entry.get().strip().lower()
        key = self.key_entry.get().strip().upper()
        if license_manager.activate_license(email, key):
            msg.showinfo("Activated", "FileBuddy Pro activated successfully!\nRestart to apply changes.")
            self.destroy()
        else:
            msg.showerror("Invalid", "License key invalid. Please check your email and key.")
