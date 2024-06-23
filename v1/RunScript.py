import subprocess

def run_cpp_script_extra(event):
    text_editor = event.widget.master.text_editor
    run_cpp_script(text_editor)

def run_cpp_script(text_editor):
    if text_editor.isFileOpen and text_editor.File:
        input_file = "input.txt"
        output_file = "output.txt"
        bash_command = f"./compile_and_run.sh {text_editor.File} {input_file} {output_file}"

        input_text = text_editor.inputText.get("1.0", 'end')
        with open(input_file, "w") as f:
            f.write(input_text)

        process = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if not error:
            try:
                with open(output_file, "r") as f:
                    output_text = f.read()
                    text_editor.outputText.delete('1.0', 'end')
                    text_editor.outputText.insert('end', output_text)
            except FileNotFoundError:
                print("Output file not found.")
        else:
            print("Error:", error.decode("utf-8"))
