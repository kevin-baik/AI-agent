import os

def get_files_info(working_directory, directory="."):
    try:
        abs_path_of_working_directory = os.path.abspath(working_directory)
        fullpath = os.path.join(abs_path_of_working_directory, directory)
        abs_fullpath = os.path.abspath(fullpath)

        if not abs_fullpath.startswith(abs_path_of_working_directory):
           return f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_fullpath):
            return f'\tError: "{directory}" is not a directory'

        content_info = []
        for content in os.listdir(abs_fullpath):
            content_path = os.path.join(abs_fullpath, content)
            content_info.append(f"- {content}: file_size={os.path.getsize(content_path)} bytes, is_dir={os.path.isdir(content_path)}")

        return "\n".join(content_info)

    except Exception as e:
        return f"\tError: {e}"
