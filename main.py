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

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Model metadata: \n Prompt tokens: {model_response.usage_metadata.prompt_token_count} \n Response tokens: {model_response.usage_metadata.candidates_token_count} \n")

        
    if model_response.candidates:
        for candidate in model_response.candidates:
            messages.append(candidate.content)

    if not model_response.function_calls:
        print(f"Model response: \n {model_response.text} \n ")
        return model_response.text

    for function_call in model_response.function_calls:
        calling_message = " \n".join([f"{function_call.name} ({function_call.args})"])
        print(f"Calling function: {calling_message}")

        function_call_result = call_function(function_call_part=function_call, verbose=verbose)

        if (not function_call_result.parts or not function_call_result.parts[0].function_response):
            raise Exception("empty function call result")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        
        messages.append(function_call_result)
    

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

    MAX_ITERATIONS = 20
    
    for i in range(MAX_ITERATIONS):
        try:
            result = generate_content(client, messages, verbose_flag, user_prompt)
            if result is not None:
                print(result)
                break

        except Exception as e:
            print(e)

     



if __name__ == "__main__":
    main()
