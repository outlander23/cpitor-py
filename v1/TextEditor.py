from Stack import Stack
import autopep8
from SyntaxHighlighter import configure_syntax_highlighting

class TextEditor:
    def __init__(self, window):
        self.window = window
        self.isFileOpen = False
        self.File = ""
        self.isFileChange = False
        self.elecnt = 0
        self.mode = "normal"
        self.fileTypes = [('All Files', '*.*'),
                          ('Python Files', '*.py'),
                          ('Text Document', '*.txt')]

        self.UStack = Stack()
        self.RStack = Stack()

        configure_syntax_highlighting(self)

    def format_code(self):
        code = self.TextBox.get("1.0", "end-1c")
        formatted_code = autopep8.fix_code(code)
        self.TextBox.delete("1.0", "end")
        self.TextBox.insert("1.0", formatted_code)
