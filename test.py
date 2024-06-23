import os
import json
import subprocess
from tkinter import *
from tkinter import messagebox as message
from tkinter import filedialog as fd
from tkinter import scrolledtext
import autopep8

class Stack:
    def __init__(self, text):
        self.stack = []
        self.stack.append(text)

    def add(self, dataval):
        if dataval not in self.stack:
            self.stack.append(dataval)
            return True
        else:
            return False

    def remove(self):
        if len(self.stack) <= 1:
            return "No element in the Stack"
        else:
            return self.stack.pop()

    def peek(self):
        if len(self.stack) == 1:
            return self.stack[0]
        else:
            return self.stack[-1]

    def size(self):
        return len(self.stack)

    def clear_stack(self):
        return self.stack.clear()

    def ele(self, index):
        return self.stack[index]

class TextLineNumbers(Canvas):
    def __init__(self, master, text_widget, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        self.text_widget = text_widget
        self.text_widget.bind("<KeyRelease>", self.on_key_release)
        self.text_widget.bind("<MouseWheel>", self.on_key_release)
        self.text_widget.bind("<Button-1>", self.on_key_release)
        self.redraw()

    def on_key_release(self, event=None):
        self.redraw()

    def redraw(self, event=None):
        self.delete("all")

        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, font=("Helvetica", 14))
            i = self.text_widget.index(f"{i}+1line")

class CustomText(scrolledtext.ScrolledText):
    def __init__(self, *args, **kwargs):
        scrolledtext.ScrolledText.__init__(self, *args, **kwargs)

        self.syntax_rules = {}
        self.load_syntax_rules()

        self.bind("<KeyRelease>", self.on_key_release)
        self.bind("<Button-1>", self.on_key_release)

    def load_syntax_rules(self):
        try:
            with open('cpp_syntax_highlighting_rules.json') as f:
                self.syntax_rules = json.load(f)
        except FileNotFoundError:
            print("Syntax highlighting rules file not found.")

    def on_key_release(self, event=None):
        self.highlight_syntax()

    def highlight_syntax(self):
        for tag in self.tag_names():
            self.tag_remove(tag, "1.0", END)
        for rule in self.syntax_rules:
            pattern = rule['pattern']
            color = rule['color']
            tag_name = rule['tag_name']
            self.tag_configure(tag_name, foreground=color)

            start_index = '1.0'
            while True:
                start_index = self.search(pattern, start_index, stopindex=END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(pattern)}c"
                self.tag_add(tag_name, start_index, end_index)
                start_index = end_index

    def format_code(self):
        code = self.get("1.0", "end-1c")
        formatted_code = autopep8.fix_code(code)
        self.delete("1.0", "end")
        self.insert("1.0", formatted_code)

class Window:
    def __init__(self):
        self.isFileOpen = False
        self.File = ""
        self.isFileChange = False
        self.elecnt = 0
        self.mode = "normal"
        self.fileTypes = [('All Files', '*.*'), ('Python Files', '*.py'), ('Text Document', '*.txt')]

        self.window = Tk()
        self.window.geometry("1200x700+200+150")
        self.window.wm_title("Untitled")

        self.create_widgets()
        self.create_menu()
        self.bind_shortcuts()

        self.UStack = Stack(self.TextBox.get("1.0", "end-1c"))
        self.RStack = Stack(self.TextBox.get("1.0", "end-1c"))

        self.window.mainloop()

    def create_widgets(self):
        self.TextBox = CustomText(self.window, highlightthickness=0, font=("Helvetica", 14))
        self.TextBox.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.line_numbers = TextLineNumbers(self.window, self.TextBox, width=30)
        self.line_numbers.grid(row=0, column=0, rowspan=2, sticky="nsw")

        self.inputText = CustomText(self.window, highlightthickness=0, font=("Helvetica", 14))
        self.inputText.grid(row=0, column=1, sticky="nsew")

        self.outputText = CustomText(self.window, highlightthickness=0, font=("Helvetica", 14))
        self.outputText.grid(row=1, column=1, sticky="nsew")

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)

        self.TextBox.insert(END, "")
        self.open_input_file()
        self.open_output_file()

    def create_menu(self):
        self.menuBar = Menu(self.window, bg="#eeeeee", font=("Helvetica", 13), borderwidth=0)
        self.window.config(menu=self.menuBar)

        self.create_file_menu()
        self.create_view_menu()
        self.create_help_menu()
        self.create_run_menu()
        self.create_edit_menu()
        self.create_setting_menu()

    def create_file_menu(self):
        self.fileMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.fileMenu.add_command(label="    New       Ctrl+N", command=self.new_file)
        self.fileMenu.add_command(label="    Open...      Ctrl+O", command=self.open_file)
        self.fileMenu.add_command(label="    Save         Ctrl+S", command=self.retrieve_input)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="  Exit          Ctrl+D", command=self._quit)
        self.menuBar.add_cascade(label="   File   ", menu=self.fileMenu)

    def create_view_menu(self):
        self.viewMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.viewMenu.add_command(label="   Change Mode   ", command=self.change_color)
        self.menuBar.add_cascade(label="   View   ", menu=self.viewMenu)

    def create_help_menu(self):
        self.helpMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.helpMenu.add_command(label="    About   ", command=self.about)
        self.menuBar.add_cascade(label="   Help   ", menu=self.helpMenu)

    def create_run_menu(self):
        self.runMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.runMenu.add_command(label="    Run         Ctrl+R", command=self.run_cpp_script)
        self.menuBar.add_cascade(label="   Run   ", menu=self.runMenu)

    def create_edit_menu(self):
        self.editMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.editMenu.add_command(label="Format Code", command=self.format_code)
        self.menuBar.add_cascade(label="   Edit   ", menu=self.editMenu)

    def create_setting_menu(self):
        self.settings_menu = Menu(self.menuBar, tearoff=0)
        self.tab_size_var = IntVar(value=4)
        self.settings_menu.add_radiobutton(label="Tab Size 2", variable=self.tab_size_var, value=2, command=self.set_tab_size)
        self.settings_menu.add_radiobutton(label="Tab Size 4", variable=self.tab_size_var, value=4, command=self.set_tab_size)
        self.settings_menu.add_radiobutton(label="Tab Size 8", variable=self.tab_size_var, value=8, command=self.set_tab_size)
        self.settings_menu.add_separator()
        self.mode_var = IntVar(value=0)
        self.settings_menu.add_radiobutton(label="Normal Mode", variable=self.mode_var, value=0, command=self.set_mode)
        self.settings_menu.add_radiobutton(label="Dark Mode", variable=self.mode_var, value=1, command=self.set_mode)
        self.menuBar.add_cascade(label="Settings", menu=self.settings_menu)

    def set_tab_size(self):
        tab_size = self.tab_size_var.get()
        self.TextBox.config(tabsize=tab_size)

    def set_mode(self):
        mode = self.mode_var.get()
        if mode == 0:
            self.mode = "normal"
            self.window.configure(bg='white')
            self.TextBox.config(bg='white', fg='black')
        elif mode == 1:
            self.mode = "dark"
            self.window.configure(bg='black')
            self.TextBox.config(bg='black', fg='white')

    def bind_shortcuts(self):
        self.TextBox.bind('<Control-s>', self.retrieve_input)
        self.TextBox.bind('<Control-S>', self.retrieve_input)
        self.TextBox.bind('<Control-o>', self.open_file)
        self.TextBox.bind('<Control-O>', self.open_file)
        self.TextBox.bind('<Control-n>', self.new_file)
        self.TextBox.bind('<Control-N>', self.new_file)
        self.TextBox.bind('<Control-d>', self._quit)
        self.TextBox.bind('<Control-D>', self._quit)
        self.TextBox.bind('<Control-r>', self.run_cpp_script)
        self.TextBox.bind('<Control-R>', self.run_cpp_script)

    def format_code(self):
        self.TextBox.format_code()

    def open_input_file(self):
        self.inputText.delete("1.0", "end")
        try:
            with open("input.txt", "r") as file:
                self.inputText.insert(END, file.read())
        except FileNotFoundError:
            self.inputText.insert(END, "Input file not found.")

    def open_output_file(self):
        self.outputText.delete("1.0", "end")
        try:
            with open("output.txt", "r") as file:
                self.outputText.insert(END, file.read())
        except FileNotFoundError:
            self.outputText.insert(END, "Output file not found.")

    def run_cpp_script(self):
        
        if self.isFileOpen and len(self.File) != 0:
            self.write_file(self.File)
            self.isFileChange = False
        else:
            self.save_new_file("yes")
            self.window.wm_title(self.File)
            self.isFileOpen = True
        print("run cpp")
        if self.File:  # Check if a file is currently open
            input_file = "input.txt"
            output_file = "output.txt"
            bash_command = f"./compile_and_run.sh {self.File} {input_file} {output_file}"
            print("Bash command:", bash_command)  # Debugging print

            # Write input text to input.txt
            input_text = self.inputText.get("1.0", END)
            with open(input_file, "w") as f:
                f.write(input_text)

            # Execute the bash command
            process = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            print("Output:", output.decode("utf-8"))  # Debugging print


            if error:
                print("Error:", error.decode("utf-8"))
            else:
                # Reload the output file
                try:
                    with open(output_file, "r") as f:
                        output_text = f.read()
                        self.outputText.delete('1.0', END)  # Clear previous output
                        self.outputText.insert(END, output_text)  # Update outputText with new output
                        print("Output:", output_text)  # Debugging print
                except FileNotFoundError:
                    print("Output file not found.")
        else:
            print("No file is currently open.")

    def new_file(self):
        if self.isFileChange:
            self.save_change_dialog()
        self.isFileOpen = False
        self.isFileChange = False
        self.TextBox.delete(1.0, END)
        self.window.wm_title("Untitled")

    def open_file(self):
        if self.isFileChange:
            self.save_change_dialog()
        file_path = fd.askopenfilename(filetypes=self.fileTypes)
        if file_path:
            self.load_file(file_path)
        self.window.wm_title(os.path.basename(file_path) + " - Editor")

    def save_change_dialog(self):
        if self.isFileChange:
            if message.askyesno("Save changes", "You have unsaved changes. Do you want to save them?"):
                self.save_file()

    def load_file(self, file_path):
        self.TextBox.delete(1.0, END)
        with open(file_path, "r") as file:
            self.TextBox.insert(END, file.read())
        self.File = file_path
        self.isFileOpen = True
        self.isFileChange = False

    def save_file(self):
        if self.isFileOpen:
            with open(self.File, "w") as file:
                file.write(self.TextBox.get(1.0, END))
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = fd.asksaveasfilename(filetypes=self.fileTypes)
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.TextBox.get(1.0, END))
            self.File = file_path
            self.isFileOpen = True
            self.isFileChange = False
            self.window.wm_title(os.path.basename(file_path) + " - Editor")

    def _quit(self):
        if self.isFileChange:
            self.save_change_dialog()
        self.window.quit()
        self.window.destroy()

    def retrieve_input(self, event=None):
        input_text = self.TextBox.get("1.0", "end-1c")
        with open("output.txt", "w") as file:
            file.write(input_text)
        message.showinfo("Success", "File saved successfully.")

    def about(self):
        message.showinfo("About", "This is a code editor built with Python and Tkinter.")

    def change_color(self):
        if self.mode == "normal":
            self.window.configure(bg='black')
            self.TextBox.configure(bg='black', fg='white')
            self.mode = "dark"
        else:
            self.window.configure(bg='white')
            self.TextBox.configure(bg='white', fg='black')
            self.mode = "normal"

if __name__ == "__main__":
    app = Window()
