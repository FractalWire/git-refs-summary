import os
import requests
import subprocess
from typing import Any, Dict

def get_gemini_response(prompt: str) -> Dict[str, Any]:
    "send a prompt to gemini AI and return the response"

    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
        
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": api_key
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    response = requests.post(api_url, headers=headers, params=params, json=data)
    return response.json()

def main() -> None:
    "main function"

    try:
        diff_command = "git --no-pager diff"
        diff_output = subprocess.check_output(diff_command, shell=True, text=True)
        prompt = f"Give a title and summarize the following git diff output using a markdown format:\n{diff_output}"
        response = get_gemini_response(prompt)
        
        if "error" in response:
            print(f"Error from Gemini API: {response['error']}")
        else:
            # Extract the text content from the response
            if "candidates" in response and len(response["candidates"]) > 0:
                candidate = response["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "text" in part:
                            print("\nGemini Summary:")
                            print("-" * 40)
                            print(part["text"])
                            print("-" * 40)
                            
                            # Print token usage if available
                            if "usageMetadata" in response:
                                usage = response["usageMetadata"]
                                print("\nToken Usage:")
                                print(f"Prompt tokens:    {usage.get('promptTokenCount', 'N/A')}")
                                print(f"Response tokens:  {usage.get('candidatesTokenCount', 'N/A')}")
                                print(f"Total tokens:     {usage.get('totalTokenCount', 'N/A')}")
            else:
                print("No summary content found in response")
            
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
