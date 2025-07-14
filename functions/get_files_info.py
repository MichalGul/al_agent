import os

def get_files_info(working_directory, directory=None) -> str:

    try:

        full_working_directory = os.path.abspath(working_directory)
        dir_display = "." if directory is None else directory
        full_path = os.path.abspath(os.path.join(full_working_directory, dir_display))

        if not full_path.startswith(full_working_directory):
            return f'Error: Cannot list "{dir_display}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'Error: "{dir_display}" is not a directory'

        return_message =[]
        for item in os.listdir(full_path):
            abs_item_path = os.path.abspath(os.path.join(full_path, item))
            return_message.append(f"- {item}: file_size={os.path.getsize(abs_item_path)} bytes, is_dir={os.path.isdir(abs_item_path)}")

        return "\n".join(return_message)
    except Exception as e:
        return f"Error: {str(e)}"
