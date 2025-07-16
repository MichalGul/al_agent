from google.genai import types

from functions.get_files_info import schema_get_files_info, schema_get_file_content, get_files_info, get_file_content
from functions.write_file import schema_write_file_content, write_file
from functions.run_python_file import schema_run_python_file_content, run_python_file

avaliable_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file_content,
        schema_run_python_file_content
    ]
)

EXECUTABLE_FUNCTIONS = {
    "write_file": write_file,
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file
}



def call_function(function_call_part: types.FunctionCall, verbose: bool=False) -> types.Content:

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    arguments = function_call_part.args
    arguments["working_directory"] = "./calculator"
    
    if function_name not in EXECUTABLE_FUNCTIONS:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_result = EXECUTABLE_FUNCTIONS[function_name](**arguments)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
