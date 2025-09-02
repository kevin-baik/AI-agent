import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from enum import Enum

class Flags(Enum):
    VERBOSE = 1

def main():
    load_dotenv()

    args = sys.argv[1:]
    
    if not args:
        print("no args, exiting program...")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    user_prompt = args[0]
    prompt_flags = []
    for arg in args:
        if arg.startswith("-") or arg.startswith("--"):
            prompt_flags.append(arg)
    
    flags = []
    for flag in prompt_flags:
        match flag:
            case "-v" | "--verbose":
                flags.append(Flags.VERBOSE)
    
    print("User prompt:", user_prompt)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    generate_content(client, messages, flags)
    
def generate_content(client, messages, flags):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    if Flags.VERBOSE in flags:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    print("Response:")
    print(response.text)
    
if __name__ == "__main__":
    main()
