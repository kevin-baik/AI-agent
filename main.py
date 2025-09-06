import sys
import os
from enum import Enum
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import call_function, available_functions
from config import MAX_ITERATIONS

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
    curr_iteration = 0
    while True:
        curr_iteration += 1
        if curr_iteration > MAX_ITERATIONS:
            print(f"Max attempts ({MAX_ITERATIONS}) reached.")
            sys.exit(1)
        
        try:
            final_response = generate_content(client, messages, flags)
            if final_response:
                print("Final response:")
                print(final_response)
                break
            max_iteration -= 1
        
        except Exception as e:
            print(f"Error while executing generate_content: {e}")

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

    if not response.function_calls:
        return response.text

    for candidate in response.candidates:
        messages.append(candidate.content)

    function_call_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, Flags.VERBOSE in flags)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if Flags.VERBOSE in flags:
            print(f"-> {function_response.parts[0].function_response.response}")

        function_call_responses.append(function_call_result.parts[0])

    if not function_call_responses:
        raise Exception("Error during function call: no function responses.")
        
    messages.append(types.Content(role="user", parts=function_call_responses))

if __name__ == "__main__":
    main()
