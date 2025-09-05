import os
from config import CHARACTER_LIMIT

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.join(abs_working_dir, directory)
        abs_target_dir = os.path.abspath(target_dir)

        if not abs_target_dir.startswith(abs_working_dir):
           return f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_target_dir):
            return f'\tError: "{directory}" is not a directory'

        content_info = []
        for content in os.listdir(abs_target_dir):
            content_path = os.path.join(abs_target_dir, content)
            content_info.append(f"- {content}: file_size={os.path.getsize(content_path)} bytes, is_dir={os.path.isdir(content_path)}")

        return "\n".join(content_info)

    except Exception as e:
        return f"\tError: {e}"

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
