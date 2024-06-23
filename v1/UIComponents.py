from tkinter import Text
from Linenumber import TextLineNumbers

def create_ui_components(window):
    window.text_editor.TextBox = Text(window.window, highlightthickness=0, font=("Helvetica", 14))
    window.text_editor.TextBox.grid(row=0, column=0, rowspan=2, sticky="nsew")

    window.text_editor.inputText = Text(window.window, highlightthickness=0, font=("Helvetica", 14))
    window.text_editor.inputText.grid(row=0, column=1, sticky="nsew")

    window.text_editor.outputText = Text(window.window, highlightthickness=0, font=("Helvetica", 14))
    window.text_editor.outputText.grid(row=1, column=1, sticky="nsew")

    window.text_editor.line_numbers = TextLineNumbers(window.window, window.text_editor.TextBox, width=30)
    window.text_editor.line_numbers.grid(row=0, column=0, rowspan=2, sticky="nsw")

    window.window.columnconfigure(0, weight=1)
    window.window.columnconfigure(1, weight=1)
    window.window.rowconfigure(0, weight=1)
    window.window.rowconfigure(1, weight=1)

def create_menu(window):
    # Create menus and bind to window
    pass
