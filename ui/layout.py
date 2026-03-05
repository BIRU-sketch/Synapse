import customtkinter as ctk

from sidebar import Sidebar

from pages.dashboard import DashboardPage
from pages.workflow_creator import WorkflowCreatorPage
from pages.tools_page import ToolsPage
from pages.agent_console import AgentConsolePage
from pages.settings_page import SettingsPage


class AppLayout(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, self.switch_page)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.page_container = ctk.CTkFrame(self)
        self.page_container.grid(row=0, column=1, sticky="nsew")

        # Create pages
        self.pages = {
            "dashboard": DashboardPage(self.page_container),
            "workflow": WorkflowCreatorPage(self.page_container),
            "tools": ToolsPage(self.page_container),
            "agent": AgentConsolePage(self.page_container),
            "settings": SettingsPage(self.page_container)
        }

        self.current_page = None

        self.switch_page("dashboard")

    def switch_page(self, page_name):

        if self.current_page:
            self.current_page.pack_forget()

        page = self.pages[page_name]
        page.pack(fill="both", expand=True)

        self.fade_in(page)

        self.current_page = page

    def fade_in(self, widget):

        for i in range(0, 11):
            widget.after(i * 15, lambda w=widget: w.update())