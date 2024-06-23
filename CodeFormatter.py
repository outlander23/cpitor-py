import subprocess,os

def format_cpp_code(code):
    # Command to invoke clang-format
    command = ['clang-format', '-style=file']

    # Run clang-format with input code
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
        formatted_code, error = process.communicate(input=code)
        
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command, output=error)

        return formatted_code.strip()
    
    except FileNotFoundError:
        raise Exception("clang-format not found. Please install clang-format and ensure it is in your PATH.")
