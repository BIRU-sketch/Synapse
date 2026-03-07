import customtkinter as ctk
from components.step_card import StepCard
import json
from pathlib import Path

class WorkflowCreatorPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Top area: workflow name + mode selector + (AI prompt)
        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=20, pady=(20,10))

        ctk.CTkLabel(top, text="Workflow Name:", width=110).pack(side="left")
        self.workflow_name = ctk.CTkEntry(top, placeholder_text="Enter workflow name")
        self.workflow_name.pack(side="left", fill="x", expand=True, padx=(8,20))

        ctk.CTkLabel(top, text="Mode:", width=60).pack(side="left")
        self.mode_var = ctk.StringVar(value="offline")
        self.mode_menu = ctk.CTkOptionMenu(top, variable=self.mode_var, values=["offline","hybrid","online"], command=self.toggle_mode)
        self.mode_menu.pack(side="left", padx=(8,0))
        self.save_btn = ctk.CTkButton(top,text="Save Workflow",width=140,command=self.save_workflow)
        self.save_btn.pack(side="right", padx=(10,0))

        # AI prompt + generate button (hidden unless online mode)
        self.ai_frame = ctk.CTkFrame(self)
        self.ai_prompt = ctk.CTkEntry(self.ai_frame, placeholder_text="Describe the goal for AI to generate a workflow...")
        self.ai_prompt.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.generate_btn = ctk.CTkButton(self.ai_frame, text="Generate Workflow with AI", width=220, command=self.generate_ai_workflow)
        self.generate_btn.pack(side="left")

        # Steps area - scrollable
        self.step_container = ctk.CTkScrollableFrame(self, label_text="Steps", height=420)
        self.step_container.pack(fill="both", expand=True, padx=20, pady=10)

        # internal list of step objects
        self.steps = []
        # Auto-create first step for offline/hybrid modes
        if self.mode_var.get() in ["offline", "hybrid"]:
            first_step = StepCard(self.step_container,delete_callback=None, 
                          add_above_callback=self.add_step_at,
                          add_below_callback=self.add_step_at,
                          move_up_callback=self.move_step_up,
                          move_down_callback=self.move_step_down,
                          mode=self.mode_var.get())
            first_step.pack(fill="x", pady=6, padx=6)
            self.steps.append(first_step)
        # initial UI state
        self.toggle_mode(self.mode_var.get())

    # ---------- Step management helpers ----------
    def add_step_at(self, ref_step=None, position="after"):
        """
        Insert a new step card.
        if ref_step is None -> append at end.
        position: "after" or "before"
        """
        step = StepCard(self.step_container,
                        delete_callback=self.remove_step,
                        add_above_callback=self.add_step_at,
                        add_below_callback=self.add_step_at,
                        move_up_callback=self.move_step_up,
                        move_down_callback=self.move_step_down,
                        mode=self.mode_var.get())
        if ref_step is None:
            # append
            step.pack(fill="x", pady=6, padx=6)
            self.steps.append(step)
        else:
            # insert relative to ref_step
            try:
                idx = self.steps.index(ref_step)
            except ValueError:
                idx = len(self.steps)
            insert_at = idx + 1 if position == "after" else idx
            # insert in UI by repacking in order
            self.steps.insert(insert_at, step)
            self._repack_steps()

    def remove_step(self, step):
        if step in self.steps:
            step.destroy()
            self.steps.remove(step)
            self._repack_steps()

    def move_step_up(self, step):
        try:
            idx = self.steps.index(step)
            if idx > 0:
                self.steps[idx], self.steps[idx-1] = self.steps[idx-1], self.steps[idx]
                self._repack_steps()
        except ValueError:
            pass

    def move_step_down(self, step):
        try:
            idx = self.steps.index(step)
            if idx < len(self.steps)-1:
                self.steps[idx], self.steps[idx+1] = self.steps[idx+1], self.steps[idx]
                self._repack_steps()
        except ValueError:
            pass

    def _repack_steps(self):
        # clear all children then re-pack in order to reflect steps list
        for w in self.step_container.winfo_children():
            w.pack_forget()
        for s in self.steps:
            s.pack(fill="x", pady=6, padx=6)

    # ---------- Mode / AI ----------
    def toggle_mode(self, mode):
        # show/hide AI generator area
        if mode == "online":
            self.ai_frame.pack(fill="x", padx=20, pady=(0,8))
        else:
            self.ai_frame.pack_forget()

        # inform step cards to update their internal UI
        for step in self.steps:
            step.update_mode(mode)

    def generate_ai_workflow(self):
        prompt = self.ai_prompt.get().strip()
        if not prompt:
            return
        # placeholder: call backend planner
        print("[WorkflowCreator] Sending AI prompt:", prompt)
        # example: plan = controller.generate_workflow_from_prompt(prompt)
        # then convert plan to step cards:
        # self._populate_from_plan(plan)

    # ---------- Utility populators ----------
    def _populate_from_plan(self, plan_steps):
        # plan_steps is a list of step dicts (type/tool/params)
        # clear existing
        for s in list(self.steps):
            self.remove_step(s)
        for p in plan_steps:
            # insert at end
            self.add_step_at(None, "after")
            card = self.steps[-1]
            card.load_from_dict(p)
    def collect_workflow_data(self):
        workflow = {
            "name": self.workflow_name.get(),
            "mode": self.mode_var.get(),
            "steps": []
            }
        for step in self.steps:
            step_type = step.mode_var.get()
            if step_type == "Shell":
                workflow["steps"].append({
                    "type": "shell",
                    "params": {
                        "command": step.shell_entry.get()
                        }
                    })
            elif step_type == "Local Tools":
                workflow["steps"].append({
                    "type": "tool",
                    "tool": step.tool_dropdown.get(),
                    "params": step.tool_params.get()
                    })
            elif step_type == "AI":
                workflow["steps"].append({
                    "type": "ai",
                    "instruction": step.ai_entry.get()
                    })
        return workflow
    def save_workflow(self):
        data = self.collect_workflow_data()
        workflow_name = data["name"].strip()
        if not workflow_name:
            print("Workflow must have a name")
            return
        save_dir = Path("workflows")
        save_dir.mkdir(exist_ok=True)
        filepath = save_dir / f"{workflow_name}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            print(f"Workflow saved to {filepath}")