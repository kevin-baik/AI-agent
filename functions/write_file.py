import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.join(abs_working_dir, file_path)
    abs_target_file = os.path.abspath(target_file)

    if not abs_target_file.startswith(abs_working_dir):
       return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    dir_to_file = file_path.split("/")
    if len(dir_to_file) > 1:
        os.makedirs(os.path.join(abs_working_dir, *dir_to_file[:-1]), exist_ok=True)

    try:
        with open(abs_target_file, "w") as f:
            f.write(content)
        if os.path.exists(abs_target_file):
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"\tError: {e}"

