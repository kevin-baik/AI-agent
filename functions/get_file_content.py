import os
from config import CHARACTER_LIMIT

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.join(abs_working_dir, file_path)
    abs_target_file = os.path.abspath(target_file)

    if not abs_target_file.startswith(abs_working_dir):
       return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_target_file, "r") as f:
            file_content = f.read(CHARACTER_LIMIT)
            if os.path.getsize(abs_target_file) > CHARACTER_LIMIT:
                file_content += f'[...File "{file_path}" truncated at 10000 characters]'
            return file_content

    except Exception as e:
        return f"\tError: {e}"
