from Window import *

TextEditor = Window()

TextEditor.TextBox.pack(expand=1, fill="both")
TextEditor.window.protocol("WM_DELETE_WINDOW", TextEditor.on_closing)
TextEditor.window.bind("<Key>", TextEditor.key_pressed)

# Add a menu option to run C++ code
TextEditor.viewMenu.add_command(label="Run C++ Code", command=TextEditor.run_cpp_script)

TextEditor.window.mainloop()

