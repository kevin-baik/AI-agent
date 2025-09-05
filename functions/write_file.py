import os
from google.genai import types

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


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Opens and overwrite contents with new content at the specified file path, if no file or directory exists at specified file path, creates new directory and file upto file path.", 
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path, relative to the working directory, to the file to be written to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written into the file.",
            ),
        },
    ),
)
