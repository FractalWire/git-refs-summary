import os
import requests
import subprocess
from typing import Any, Dict

def get_gemini_response(prompt: str) -> Dict[str, Any]:
    "send a prompt to gemini AI and return the response"

    api_url = "https://api.gemini.com/v1/generateContent"
    api_key = os.getenv("GEMINI_API_KEY")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
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
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()

def main() -> None:
    "main function"

    diff_command = "git --no-pager diff hotfix"
    diff_output = subprocess.check_output(diff_command, shell=True, text=True)
    prompt = f"Summarize the following git diff output:\n{diff_output}"
    response = get_gemini_response(prompt)
    print(response)

if __name__ == "__main__":
    main()
