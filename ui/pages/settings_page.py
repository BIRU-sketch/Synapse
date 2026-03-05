import customtkinter as ctk

class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Settings", font=("Arial", 28))
        label.pack(pady=40)