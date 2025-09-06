import sys
import os
from enum import Enum
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

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
    
    # USER_PROMPT
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
        
    # GENERATE_CONTENT
    generate_content(client, messages, flags)
    
def generate_content(client, messages, flags):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if Flags.VERBOSE in flags:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    print("Response:")
    if not response.function_calls:
        print(response.text)

    func_calls = response.function_calls
    for func in func_calls:
        function_response = call_function(func)
        if not function_response.parts[0].function_response.response:
            raise SystemError("fatal error: no function response")
        if Flags.VERBOSE in flags:
            print(f"-> {function_response.parts[0].function_response.response}")


if __name__ == "__main__":
    main()
