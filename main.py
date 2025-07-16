import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from call_function import avaliable_functions, call_function


SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def generate_content(client: genai.Client, messages :list, verbose: bool, user_prompt: str):
    model_response: types.GenerateContentResponse = client.models.generate_content( 
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools =[avaliable_functions], system_instruction=SYSTEM_PROMPT)
    )

    if model_response.function_calls:
        calling_message = " \n".join([f"{f_call.name} ({f_call.args})" for f_call in model_response.function_calls])
        print(f"Calling function: {calling_message}")
        # assume calling one function
        function_call_result = call_function(function_call_part=model_response.function_calls[0], verbose=verbose)
        try:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        except:
            raise Exception("Called Function response does not have result")
            exit(1)

    else:
        print(f"Model response: {model_response.text} \n ")
    
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Model metadata: \n Prompt tokens: {model_response.usage_metadata.prompt_token_count} \n Response tokens: {model_response.usage_metadata.candidates_token_count} \n")

        


def main():
    print("Hello from al-agent!")

    if len(sys.argv) < 2:
        print("Prompt not provided in arguments. Exiting...")
        exit(1)

    load_dotenv()
    API_KEY = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=API_KEY)
    
    verbose_flag = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    user_prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    generate_content(client, messages, verbose_flag, user_prompt) 



if __name__ == "__main__":
    main()
