import os
from functions.config import MAX_CHARACTERS, TRUNCATE_MESSAGE

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



def get_file_content(working_directory, file_path) -> str:
    try:
        full_working_directory = os.path.abspath(working_directory)
        full_file_path = os.path.abspath(os.path.join(full_working_directory, file_path))

        if not full_file_path.startswith(full_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'


        with open(full_file_path, "r") as file:
            file_content_string = file.read(MAX_CHARACTERS)

        if len(file_content_string) >= MAX_CHARACTERS:
            truncate_message = TRUNCATE_MESSAGE.format(file_path, MAX_CHARACTERS)
            file_content_string = f"{file_content_string} {truncate_message}"
        
        return file_content_string
        

    except Exception as e:
        return f"Error: {str(e)}"
    