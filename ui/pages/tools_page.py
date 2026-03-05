import customtkinter as ctk

class ToolsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Local Tools", font=("Arial", 28))
        label.pack(pady=40)