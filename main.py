import customtkinter as ctk
from ui.organizer_tab import OrganizerTab
from ui.duplicate_tab import DuplicateScannerTab

class FileBuddy(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧠 FileBuddy — Your Study File Helper")
        self.geometry("700x750")
        self.resizable(False, False)

        # --- Grid layout for window ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- MAIN TABS ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # --- Organizer Tab ---
        organizer_frame = self.tabview.add("🗂️ Organizer")
        organizer_frame.grid_rowconfigure(0, weight=1)
        organizer_frame.grid_columnconfigure(0, weight=1)

        self.organizer_tab = OrganizerTab(organizer_frame, log_callback=self.log_to_console)
        self.organizer_tab.grid(row=0, column=0, sticky="nsew")

        # --- Duplicate Scanner Tab ---
        duplicate_frame = self.tabview.add("🔍 Duplicate Scanner")
        duplicate_frame.grid_rowconfigure(0, weight=1)
        duplicate_frame.grid_columnconfigure(0, weight=1)

        self.duplicate_tab = DuplicateScannerTab(duplicate_frame)
        self.duplicate_tab.grid(row=0, column=0, sticky="nsew")

    def log_to_console(self, message):
        print(message)


if __name__ == "__main__":
    app = FileBuddy()
    app.mainloop()
