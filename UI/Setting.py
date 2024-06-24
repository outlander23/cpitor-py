import re
def create_setting_menu(self):
        self.settings_menu = Menu(self.menuBar, tearoff=0)
        self.tab_size_var = IntVar(value=4)  # Default tab size
        self.settings_menu.add_radiobutton(label="Tab Size 2", variable=self.tab_size_var, value=2, command=self.set_tab_size)
        self.settings_menu.add_radiobutton(label="Tab Size 4", variable=self.tab_size_var, value=4, command=self.set_tab_size)
        self.settings_menu.add_radiobutton(label="Tab Size 8", variable=self.tab_size_var, value=8, command=self.set_tab_size)
        self.settings_menu.add_separator()
        self.mode_var = IntVar(value=0)  # 0 for Normal mode, 1 for Dark mode
        self.settings_menu.add_radiobutton(label="Normal Mode", variable=self.mode_var, value=0, command=self.set_mode)
        self.settings_menu.add_radiobutton(label="Dark Mode", variable=self.mode_var, value=1, command=self.set_mode)
        self.menuBar.add_cascade(label="Settings", menu=self.settings_menu)
def set_mode(self):
        mode = self.mode_var.get()
        if mode == 0:  # Normal mode
            self.window.config(bg="white", fg="black")
            self.TextBox.config(bg="white", fg="black", insertbackground="black")
            self.terminalText.config(bg="white", fg="black")
            self.inputText.config(bg="white", fg="black")
            self.outputText.config(bg="white", fg="black")
        else:  # Dark mode
            self.window.config(bg="black", fg="white")
            self.TextBox.config(bg="black", fg="white", insertbackground="white")
            self.terminalText.config(bg="black", fg="white")
            self.inputText.config(bg="black", fg="white")
            self.outputText.config(bg="black", fg="white")
def set_tab_size(self):
        tab_size = self.tab_size_var.get()
        self.TextBox.config(tabsize=tab_size)