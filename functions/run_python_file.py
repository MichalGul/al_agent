import os
import subprocess
from google.genai import types

schema_run_python_file_content = types.FunctionDeclaration(
    name="run_python_file",
    description="Use installed python interpreter to run python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file path to execute, relative to the working directory.",
            )
        }
    )
)


def run_python_file(working_directory, file_path):
        try:
            full_working_directory = os.path.abspath(working_directory)
            full_file_path = os.path.abspath(os.path.join(full_working_directory, file_path))

            if not full_file_path.startswith(full_working_directory):
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            
            if not os.path.exists(full_file_path):
                return f'Error: File "{file_path}" not found'
            

            _, file_ext = os.path.splitext(full_file_path)
            if file_ext != ".py":
                return f'Error: "{file_path}" is not a Python file'
                 

            complete_process: subprocess.CompletedProcess = subprocess.run(["python", full_file_path], capture_output=True, timeout=30, cwd=full_working_directory)
            stdout = complete_process.stdout.decode('utf-8') if complete_process.stdout else ''
            stderr = complete_process.stderr.decode('utf-8') if complete_process.stderr else ''
            return_code = complete_process.returncode

            if not stdout and not stderr and return_code == 0:
                return "No output produced."
            
            # Build the output string
            output_parts = []
            if stdout:
                output_parts.append(f"STDOUT:\n{stdout}")
            if stderr:
                output_parts.append(f"STDERR:\n{stderr}")
            if return_code != 0:
                output_parts.append(f"Process exited with code {return_code}")

            return "\n".join(output_parts)
           
        except Exception as e:
             return f"Error: executing python file: {str(e)}"
        

# print(run_python_file("calculator", "tests.py"))