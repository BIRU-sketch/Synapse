import customtkinter as ctk
from layout import AppLayout


class SynapseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Synapse")
        self.geometry("900x700")

        # layout container
        self.layout = AppLayout(self)
        self.layout.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = SynapseApp()
    app.mainloop()