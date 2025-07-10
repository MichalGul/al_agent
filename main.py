import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentResponse
import sys

load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def main():
    print("Hello from al-agent!")

    if len(sys.argv) < 2:
        print("Prompt not provided in arguments. Exiting...")
        exit(1)

    model_response: GenerateContentResponse = client.models.generate_content( 
        model="gemini-2.0-flash-001",
        contents=sys.argv[1]
    )
    print(f"Model response:\n {model_response.text}")
    print(f"Model metadata: \n Prompt tokens: {model_response.usage_metadata.prompt_token_count} \n Response tokens: {model_response.usage_metadata.candidates_token_count} \n")
    

if __name__ == "__main__":
    main()
