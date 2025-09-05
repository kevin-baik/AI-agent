import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_file = os.path.abspath(os.path.join(abs_working_dir, file_path))
    
    if not abs_target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_target_file):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(["python", abs_target_file, *args], 
                                capture_output=True, 
                                text=True, 
                                timeout=30)
        result = []
	if completed_process.stdout:
	    result.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
	    result.append(f"STDERR:\n{completed_process.stderr}")

        if completed_process.returncode != 0:
            result.append(f"Process exited with code {completed_process.returncode}")

        return "\n".join(result) if result else "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"

