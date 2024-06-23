import subprocess
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