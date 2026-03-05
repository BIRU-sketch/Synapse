import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent, switch_callback):
        super().__init__(parent, width=220)

        self.switch_page = switch_callback

        self.pack_propagate(False)

        title = ctk.CTkLabel(
            self,
            text="Synapse",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=30)

        self.create_button("Dashboard", "dashboard")
        self.create_button("Workflow Creator", "workflow")
        self.create_button("Tools", "tools")
        self.create_button("Agent Console", "agent")
        self.create_button("Settings", "settings")

    def create_button(self, text, page):

        btn = ctk.CTkButton(
            self,
            text=text,
            width=180,
            command=lambda: self.switch_page(page)
        )

        btn.pack(pady=10)