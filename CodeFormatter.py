import subprocess

def format_code(code, style="file"):
    """
    Format the given C++ code using clang-format.

    Args:
        code (str): The C++ code to format.
        style (str): The formatting style to use. Defaults to 'file' to use a .clang-format file if present.

    Returns:
        str: The formatted C++ code.
    """
    try:
        process = subprocess.Popen(
            ['clang-format', '-style', style],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        formatted_code, error = process.communicate(input=code.encode('utf-8'))

        if error:
            print(f"Error formatting code: {error.decode('utf-8')}")
            return code
        
        return formatted_code.decode('utf-8')
    except Exception as e:
        print(f"Exception during code formatting: {e}")
        return code
