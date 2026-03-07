import customtkinter as ctk
from pathlib import Path
from core.workflow_executor import execute_workflow
class WorkflowsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        title = ctk.CTkLabel(self, text="Saved Workflows", font=("Arial", 22, "bold"))
        title.pack(pady=(20, 10))
        # container for workflow cards
        self.workflow_container = ctk.CTkScrollableFrame(self)
        self.workflow_container.pack(fill="both", expand=True, padx=20, pady=10)
        self.load_workflows()
    def load_workflows(self):
        # clear existing
        for widget in self.workflow_container.winfo_children():
            widget.destroy()
        workflows_path = Path("workflows")
        workflows_path.mkdir(exist_ok=True)
        workflow_files = list(workflows_path.glob("*.json"))
        if not workflow_files:
            label = ctk.CTkLabel(self.workflow_container, text="No workflows saved yet.")
            label.pack(pady=20)
            return
        for wf in workflow_files:
            name = wf.stem
            card = ctk.CTkFrame(self.workflow_container)
            card.pack(fill="x", pady=6, padx=10)
            label = ctk.CTkLabel(card, text=name, font=("Arial", 14))
            label.pack(side="left", padx=10, pady=10)
            run_btn = ctk.CTkButton(
                card,
                text="Run Workflow",
                width=140,
                command=lambda n=name: self.run_workflow(n)
            )
            run_btn.pack(side="right", padx=10, pady=10)
    def run_workflow(self, workflow_name):
        print(f"Running workflow: {workflow_name}")
        result = execute_workflow(workflow_name)
        print(result)