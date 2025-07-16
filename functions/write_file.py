import os
from google.genai import types


schema_write_file_content = types.FunctionDeclaration(
    name="write_file",
    description="Write content specified in content argument to file specified by path, constrained to the working directory. File is created if not exists",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to file"
            )
        }
    )
)


def write_file(working_directory, file_path, content):
    try:
        full_working_directory = os.path.abspath(working_directory)
        full_file_path = os.path.abspath(os.path.join(full_working_directory, file_path))

        if not full_file_path.startswith(full_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(full_file_path):
            os.makedirs(os.path.abspath(os.path.dirname(full_file_path)),exist_ok=True)

        if os.path.exists(full_file_path) and os.path.isdir(full_file_path):
            return f'Error: "{file_path}" is a directory, not a file'

        with open(full_file_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
   

    except Exception as e:
        return f"Error: writting to file: {str(e)}"
    