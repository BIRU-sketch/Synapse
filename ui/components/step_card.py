import customtkinter as ctk

class StepCard(ctk.CTkFrame):
    def __init__(self, parent,
                 delete_callback,
                 add_above_callback,
                 add_below_callback,
                 move_up_callback,
                 move_down_callback,
                 mode="offline"):
        super().__init__(parent, border_width=1, corner_radius=8, fg_color="#23232f")

        self.delete_callback = delete_callback
        self.add_above_callback = add_above_callback
        self.add_below_callback = add_below_callback
        self.move_up_callback = move_up_callback
        self.move_down_callback = move_down_callback

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=8, pady=(8,4))

        self.title = ctk.CTkLabel(header, text="Step", font=("Arial", 14, "bold"))
        self.title.pack(side="left")

        self.mode_var = ctk.StringVar(value="Shell")
        self.mode_menu = ctk.CTkOptionMenu(header, variable=self.mode_var, values=["Shell", "Local Tools", "AI"], width=120, command=self._on_step_mode_changed)
        self.mode_menu.pack(side="left", padx=(10,6))

        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")

        self.add_above_btn = ctk.CTkButton(btn_frame, text="＋A", width=42, height=28, command=lambda: self.add_above_callback(self))
        self.add_above_btn.pack(side="left", padx=4)

        self.add_below_btn = ctk.CTkButton(btn_frame, text="＋B", width=42, height=28, command=lambda: self.add_below_callback(self))
        self.add_below_btn.pack(side="left", padx=4)


        self.up_btn = ctk.CTkButton(btn_frame, text="▲", width=34, height=28, command=lambda: self.move_up_callback(self))
        self.up_btn.pack(side="left", padx=4)
        self.down_btn = ctk.CTkButton(btn_frame, text="▼", width=34, height=28, command=lambda: self.move_down_callback(self))
        self.down_btn.pack(side="left", padx=4)

  
        self.del_btn = ctk.CTkButton(btn_frame, text="✕", width=34, height=28, fg_color="#b04646", hover_color="#c95b5b", command=self._on_delete)
        self.del_btn.pack(side="left", padx=(8,0))


        if delete_callback is None:
            self.del_btn.pack_forget()

        self.params_frame = ctk.CTkFrame(self, fg_color="#1f1f24")
        self.params_frame.pack(fill="x", padx=8, pady=(0,8))

        self.shell_entry = ctk.CTkEntry(self.params_frame, placeholder_text="bash command (single line). Use ; to chain.")
        self.shell_entry.pack(fill="x", padx=8, pady=(6,4))

        self.expand_btn = ctk.CTkButton(self.params_frame, text="Expand", width=90, command=self._toggle_expand)
        self.expand_btn.pack(padx=8, pady=(0,8), anchor="e")

        self.multiline = ctk.CTkTextbox(self.params_frame, height=120)

        self.multiline.pack_forget()
        self.expanded = False

        self.tool_frame = ctk.CTkFrame(self.params_frame, fg_color="transparent")
        self.tool_dropdown = ctk.CTkOptionMenu(self.tool_frame, values=["move_file", "create_file", "delete_file", "copy_file"], width=180)
        self.tool_dropdown.pack(side="left", padx=8, pady=6)
        self.tool_params = ctk.CTkEntry(self.tool_frame, placeholder_text="params (json or key=value pairs)")
        self.tool_params.pack(side="left", padx=8, fill="x", expand=True)
        self.tool_frame.pack_forget()

        self.ai_frame = ctk.CTkFrame(self.params_frame, fg_color="transparent")
        self.ai_entry = ctk.CTkEntry(self.ai_frame, placeholder_text="AI instruction (what should AI do for this step?)")
        self.ai_entry.pack(fill="x", padx=8, pady=6)
        self.ai_frame.pack_forget()
        if self.delete_callback is None:
            self.del_btn.pack_forget() 

        self.update_mode(mode)
        try:
            self.mode_var.trace_add("write", lambda *args: self._on_step_mode_changed(self.mode_var.get()))
        except Exception:
            pass
        try:
            self._bind_hover()
        except Exception:
            pass

    def _on_step_mode_changed(self, new=None):
        mode = self.mode_var.get()

        if mode == "Shell":
            self.shell_entry.pack(fill="x", padx=8, pady=(6,4))
            self.expand_btn.pack(padx=8, pady=(0,8), anchor="e")
            self.multiline.pack_forget()
            self.tool_frame.pack_forget()
            self.ai_frame.pack_forget()
        elif mode == "Local Tools":
            self.shell_entry.pack_forget()
            self.expand_btn.pack_forget()
            self.multiline.pack_forget()
            self.tool_frame.pack(fill="x", padx=8, pady=6)
            self.ai_frame.pack_forget()
        else:  
            self.shell_entry.pack_forget()
            self.expand_btn.pack_forget()
            self.multiline.pack_forget()
            self.tool_frame.pack_forget()
            self.ai_frame.pack(fill="x", padx=8, pady=6)

    def update_mode(self, global_mode):

        if global_mode == "offline":

            if self.mode_var.get() == "AI":
                self.mode_var.set("Shell")


    def _toggle_expand(self):
        if not self.expanded:

            self.multiline.pack(fill="x", padx=8, pady=(2,6))
            self.multiline.delete("0.0", "end")
            self.multiline.insert("0.0", self.shell_entry.get())
            self.expand_btn.configure(text="Collapse")
            self.expanded = True
        else:

            text = self.multiline.get("0.0", "end").strip()
            self.shell_entry.delete(0, "end")
            self.shell_entry.insert(0, text.replace("\n", "; "))
            self.multiline.pack_forget()
            self.expand_btn.configure(text="Expand")
            self.expanded = False

    def _bind_hover(self):

        widgets = [self, self.top_frame, self.params_frame]
        for w in widgets:
            try:
                w.bind("<Enter>", lambda e, w=self: self._on_hover(e))
                w.bind("<Leave>", lambda e, w=self: self._on_leave(e))
            except Exception:
                pass

    def _on_hover(self, event):

        try:
            self.configure(fg_color="#2e2e39")
        except Exception:
            pass

    def _on_leave(self, event):

        try:
            self.configure(fg_color="#23232f")
        except Exception:
            pass
    def load_from_dict(self, data: dict):

        t = data.get("type") or data.get("step_type") or data.get("tool") or "Shell"
        if t.lower() in ("shell", "sh"):
            self.mode_var.set("Shell")
            cmd = data.get("params", {}).get("command", "")
            self.shell_entry.delete(0, "end")
            self.shell_entry.insert(0, cmd)
        elif t.lower() in ("tool", "local_tools"):
            self.mode_var.set("Local Tools")
            # assume params as simple string
            self.tool_dropdown.set(data.get("tool", "move_file"))
            self.tool_params.delete(0, "end")
            self.tool_params.insert(0, str(data.get("params", "")))
        else:
            self.mode_var.set("AI")
            self.ai_entry.delete(0, "end")
            self.ai_entry.insert(0, data.get("instruction", ""))

    def _on_delete(self):
        if self.delete_callback:
            self.delete_callback(self)