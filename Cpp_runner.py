import subprocess

def run_cpp_script(file_path, input_text, input_file="input.txt", output_file="output.txt"):
    # Build the bash command
    bash_command = f"./compile_and_run.sh {file_path} {input_file} {output_file}"
    print("Bash command:", bash_command)  # Debugging print

    # Write input text to input.txt
    with open(input_file, "w") as f:
        f.write(input_text)

    # Execute the bash command
    process = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    print("Output:", output.decode("utf-8"))  # Debugging print

    if error:
        error_message = error.decode("utf-8")
        print("Error:", error_message)
        return None, error_message
    else:
        # Read the output file
        try:
            with open(output_file, "r") as f:
                output_text = f.read()
                print("Output:", output_text)  # Debugging print
                return output_text, None
        except FileNotFoundError:
            print("Output file not found.")
            return None, "Output file not found."