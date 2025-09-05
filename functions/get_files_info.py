import os
from google.genai import types

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


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

