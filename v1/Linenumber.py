from tkinter import Canvas

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