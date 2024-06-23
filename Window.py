
import json
from tkinter import *

from tkinter import messagebox as message
from tkinter import filedialog as fd

from Stack import *

import CodeFormatter 

from Linenumber import TextLineNumbers
from Cpp_runner import run_cpp_script

import re
class Window:
    def __init__(self):
        self.File = ""
        self.elecnt = 0
        self.isFileOpen = False
        self.isFileChange = False
        
        self.mode = "normal"
        self.fileTypes = [('All Files', '*.*'),
                          ('Python Files', '*.py'),
                          ('Text Document', '*.txt')]

        self.window = Tk()
        self.window.geometry("1200x700+200+150")
        self.window.wm_title("Untitled")

       
        self.TextBox = Text(self.window, highlightthickness=0, font=("Courier", 12), borderwidth=1, relief="solid")

        self.TextBox.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.TextBox = Text(self.window, wrap='word', undo=True)
     
        # Input file name label
        self.inputFileLabel = Label(self.window, text="Input", font=("Courier", 14))
        self.inputFileLabel.grid(row=0, column=2, sticky="nw")

        # Output file name label
        self.outputFileLabel = Label(self.window, text="Output", font=("Courier", 14))
        self.outputFileLabel.grid(row=1, column=2, sticky="nw")

        # Input text area in the top-right corner
        self.inputText = Text(self.window, highlightthickness=0, font=("Courier", 14))
        self.inputText.grid(row=0, column=2, sticky="nsew", pady=(30, 0))

        # Output text area in the bottom-right corner
        self.outputText = Text(self.window, highlightthickness=0, font=("Courier", 14))
        self.outputText.grid(row=1, column=2, sticky="nsew", pady=(30, 0))

        self.TextBox = Text(self.window, highlightthickness=0, font=("Courier", 14), borderwidth=1, relief="solid")
        self.TextBox.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Line numbers on the left side of the TextBox
        self.line_numbers = TextLineNumbers(self.window, self.TextBox, width=30)
        self.line_numbers.grid(row=0, column=0, rowspan=2, sticky="nsw")

        # Terminal frame for displaying compilation errors/messages
        self.terminalFrame = Frame(self.window, bg="white", height=200)
        self.terminalFrame.grid(row=2, column=0, columnspan=3, sticky="nsew")
        
        self.terminalText = Text(self.terminalFrame, bg="white", fg="black", font=("Courier", 12))
        self.terminalText.pack(expand=True, fill="both")

        # Configure grid weights to allow resizing
        self.window.columnconfigure(1, weight=1)  # TextBox column
        self.window.columnconfigure(2, weight=2)  # Input/Output column
        self.window.rowconfigure(0, weight=1)     # First row
        self.window.rowconfigure(1, weight=1)     # Second row
        self.window.rowconfigure(2, weight=1)     # Third row (for terminal)
   

        # Load empty file in TextBox
        self.TextBox.insert(END, "")  

        # Open input.txt in inputText
        self.open_input_file()

        # Open output.txt in outputText
        self.open_output_file()

        self.window.bind("<F7>", self.run_cpp_script_extra)
        self.TextBox.bind("<FocusOut>", self.save_file_on_focus_out)
        self.window.bind("<Control-s>", self.save_file_shortcut)
    
        self.create_menu()

        self.UStack = Stack(self.TextBox.get("1.0", "end-1c"))
        self.RStack = Stack(self.TextBox.get("1.0", "end-1c"))

        self.window.mainloop()

    def display_error(self, error_message):
        self.terminalText.config(state="normal")
        self.terminalText.delete(1.0, END)  # Clear previous content
        self.terminalText.insert(END, error_message)
        self.terminalText.config(state="disabled")
    def create_menu(self):
        self.menuBar = Menu(self.window, bg="#eeeeee", font=("Helvetica", 13), borderwidth=0)
        self.window.config(menu=self.menuBar)

        self.create_file_menu()
        self.create_view_menu()
        self.create_help_menu()
        self.create_run_menu()

        self.create_edit_menu()

        self.create_setting_menu()

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

    def create_file_menu(self):
        self.fileMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.fileMenu.add_command(label="    New       Ctrl+N", command=self.new_file, )
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
        self.editMenu.add_command(label="Format Code", command=self.format_code)  # Add "Format Code" option
        self.menuBar.add_cascade(label="   Edit   ", menu=self.editMenu)
        
    def new_file(self):
        self.TextBox.config(state=NORMAL)
        if self.isFileOpen:
            if len(self.File) > 0:
                if self.isFileChange:
                    self.save_file(self.File)
                self.window.wm_title("Untitled")
                self.TextBox.delete('1.0', END)
                self.File = ''
            else:
                if self.isFileChange:
                    result = message.askquestion('Window Title', 'Do You Want to Save Changes')
                    self.save_new_file(result)
                self.window.wm_title("Untitled")
                self.TextBox.delete('1.0', END)
        else:
            self.isFileOpen = True
            self.window.wm_title("Untitled")

        self.isFileChange = False

        if self.UStack.size() > 0:
            self.UStack.clear_stack()
            self.UStack.add(self.TextBox.get("1.0", "end-1c"))

    def open_file(self):
        self.configure_syntax_highlighting()
        print("opne file")
        self.TextBox.config(state=NORMAL)
        if self.isFileOpen and self.isFileChange:
            self.save_file(self.File)
        filename = fd.askopenfilename(filetypes=self.fileTypes, defaultextension=".txt")
        if len(filename) != 0:
            self.isFileChange = False
            outfile = open(filename, "r")
            text = outfile.read()
            self.TextBox.delete('1.0', END)
            self.TextBox.insert(END, text)
            self.window.wm_title(filename)
            self.isFileOpen = True
            self.File = filename

        if self.UStack.size() > 0:
            self.UStack.clear_stack()
            self.UStack.add(self.TextBox.get("1.0", "end-1c"))

    def save_file(self, file):
        print("save file click")
        result = message.askquestion('Window Title', 'Do You Want to Save Changes')
        if result == "yes":
            if len(file) == 0:
                saveFile = fd.asksaveasfile(filetypes=self.fileTypes, defaultextension=".txt")
                print(saveFile.name)
                self.write_file(saveFile.name)
                self.TextBox.delete('1.0', END)
            else:
                self.write_file(file)

    def save_new_file(self, result):
        self.isFileChange = False
        if result == "yes":
            saveFile = fd.asksaveasfile(filetypes=self.fileTypes, defaultextension=".txt")
            self.write_file(saveFile.name)
            self.File = saveFile.name
        else:
            self.TextBox.delete('1.0', END)

    def write_file(self, file):
        inputValue = self.TextBox.get("1.0", "end-1c")
        outfile = open(file, "w")
        outfile.write(inputValue)

    def retrieve_input(self):
        self.configure_syntax_highlighting();
        if self.isFileOpen and len(self.File) != 0:
            self.write_file(self.File)
            self.isFileChange = False
        else:
            self.save_new_file("yes")
            self.window.wm_title(self.File)
            self.isFileOpen = True

    def key_pressed(self, event):
        if event.char == "\x1a" and event.keysym == "Z":
            self.redo()
        elif event.char == "\x1a" and event.keysym == "z":
            self.undo()
        elif event.char == "\x13":
            self.retrieve_input()
        elif event.char == "\x0f":
            self.open_file()
        elif event.char == "\x0e":
            self.new_file()
        elif event.char == "\x04":
            self._quit()
        elif event.char == " " or event.char == ".":
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)
        elif event.keysym == 'Return':
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)
        elif event.keysym == 'BackSpace':
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)
        elif (event.keysym == 'Up' or event.keysym == 'Down') or (event.keysym == 'Left' or event.keysym == 'Right'):
            self.isFileChange = True
            self.elecnt = 0
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)
        else:
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            if self.elecnt >= 1:
                self.UStack.remove()
            self.UStack.add(inputValue)
            self.elecnt += 1

        if self.TextBox.get("1.0", "end-1c") == self.UStack.ele(0):
            self.isFileChange = False

    def undo(self):
        self.isFileChange = True
        if self.UStack.size() == 1:
            self.UStack.remove()
            self.UStack.add(self.TextBox.get("1.0", "end-1c"))
        else:
            self.RStack.add(self.UStack.remove())
            text = self.UStack.peek()
            self.TextBox.delete('1.0', END)
            self.TextBox.insert(END, text)

    def redo(self):
        if self.RStack.size() > 1:
            text = self.RStack.peek()
            self.TextBox.delete('1.0', END)
            self.TextBox.insert(END, text)
            self.UStack.add(text)
            self.RStack.remove()

    def on_closing(self):
        if self.isFileOpen and self.isFileChange:
            self.save_file(self.File)
        self._quit()

    def _quit(self):
        self.window.quit()
        self.window.destroy()

    def change_color(self):
        if self.mode == "normal":
            self.mode = "dark"
            self.TextBox.configure(background="#2f2b2b", foreground="#BDBDBD", font=("Helvetica", 14),
                                   insertbackground="white")
        else:
            self.mode = "normal"
            self.TextBox.configure(background="white", foreground="black", font=("Helvetica", 14),
                                   insertbackground="black")

    def about(self):
        outfile = open("About.txt", "r")
        text = outfile.read()
        self.TextBox.insert(END, text)
        self.TextBox.config(state=DISABLED)

    def copy(self):
        self.TextBox.clipboard_clear()
        text = self.TextBox.get("sel.first", "sel.last")
        self.TextBox.clipboard_append(text)

    def cut(self):
        self.copy()
        self.TextBox.delete("sel.first", "sel.last")
        self.UStack.add(self.TextBox.get("1.0", "end-1c"))

    def paste(self):
        text = self.TextBox.selection_get(selection='CLIPBOARD')
        self.TextBox.insert('insert', text)
        self.UStack.add(self.TextBox.get("1.0", "end-1c"))

    def run_cpp_script(self):
            if self.isFileOpen and len(self.File) != 0:
                self.write_file(self.File)
                self.isFileChange = False
            else:
                self.save_new_file("yes")
                self.window.wm_title(self.File)
                self.isFileOpen = True
            
            if self.File:  # Check if a file is currently open
                input_text = self.inputText.get("1.0", END)
                output_text, error_message = run_cpp_script(self.File, input_text)

                if error_message:
                    print("Error:", error_message)
                    self.display_error(error_message)
                else:
                    self.outputText.delete('1.0', END)  # Clear previous output
                    self.outputText.insert(END, output_text)  # Update outputText with new output

            else:
                print("No file is currently open.")
    def open_input_file(self):
        try:
            with open("input.txt", "r") as input_file:
                input_text = input_file.read()
                self.inputText.insert(END, input_text)
            print("done input")
        except FileNotFoundError:
            print("Input file not found.")

    def open_output_file(self):
        try:
            with open("output.txt", "r") as output_file:
                output_text = output_file.read()
                self.outputText.insert(END, output_text)
                print("done output")
        except FileNotFoundError:
            print("Output file not found.")

    def save_file_on_focus_out(self, event):
        # Save the file if it's open and there are changes
        if self.isFileOpen and self.isFileChange:
            self.retrieve_input(self.File)
    def save_file_shortcut(self, event):
        print("save")
        self.format_code()
        self.retrieve_input()

    def run_cpp_script_extra(self,event):
        self.run_cpp_script()
        
    def configure_syntax_highlighting(self):
        try:
            with open('cpp_syntax_highlighting_rules.json') as f:
                syntax_rules = json.load(f)

            for rule in syntax_rules:
                pattern = rule['pattern']
                color = rule['color']
                tag_name = rule['tag_name']
                self.TextBox.tag_configure(tag_name, foreground=color)
               
                code = self.TextBox.get("1.0", "end-1c")

                for match in re.finditer(pattern, code, re.MULTILINE):
                    start_index = f"1.0 + {match.start()}c"
                    end_index = f"1.0 + {match.end()}c"
                    self.TextBox.tag_add(tag_name, start_index, end_index)

        except FileNotFoundError:
            print("Syntax highlighting rules file (cpp_syntax_highlighting_rules.json) not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def format_code(self):

        code = self.TextBox.get("1.0", "end-1c")

        formatted_code =CodeFormatter.format_cpp_code(code) 
        self.TextBox.delete("1.0", "end")
        self.TextBox.insert("1.0", formatted_code)

if __name__ == "__main__":
    TextEditor = Window()
