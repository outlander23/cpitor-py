from tkinter import Tk
from UIComponents import create_ui_components, create_menu
from FileOperations import save_file_on_focus_out, save_file_shortcut
from RunScript import run_cpp_script_extra
from TextEditor import TextEditor

class Window:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1200x700+200+150")
        self.window.wm_title("Untitled")

        self.text_editor = TextEditor(self.window)
        create_ui_components(self)
        create_menu(self)

        self.window.bind("<F8>", run_cpp_script_extra)
        self.text_editor.TextBox.bind("<FocusOut>", save_file_on_focus_out)
        self.window.bind("<Control-s>", save_file_shortcut)

        self.window.mainloop()

if __name__ == "__main__":
    TextEditor = Window()