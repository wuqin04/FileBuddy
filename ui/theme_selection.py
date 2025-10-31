import customtkinter as ctk

class ThemeSection(ctk.CTkFrame):
    def __init__(self, parent, toggle_callback):
        super().__init__(parent, fg_color="transparent")

        self.theme_switch = ctk.CTkSwitch(
            self,
            text="🌙 Dark Mode",
            font=("Inter", 13),
            command=toggle_callback
        )
        self.theme_switch.grid(row=0, column=0, pady=10)
