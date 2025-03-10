import os
import requests
import subprocess
from typing import Any, Dict, Optional, Tuple
from rich.console import Console
from rich.markdown import Markdown


def get_gemini_response(prompt: str) -> Dict[str, Any]:
    """Send a prompt to gemini AI and return the response"""

    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")

    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    data = {"system_instruction": {
        "parts": {"text": "You will give a summary of the git diff between two git references (SHA, branch, etc.). You will give an appropriate title for the changes. As for the summary, you will avoid being too exhaustive and will focus mostly on the new features or key refactoring introduced by the changes. Don't give too much importance on file potentially automatically generated or new tests. Finally, you will list a short TODO list that could include if applicable: missing tests for new features or behaviours introduced in the changes, simplification of complicated code, modification of code that might introduce errors."}},
            "contents": {"parts": {"text": prompt}}}
    response = requests.post(api_url, headers=headers, params=params, json=data)
    return response.json()


def parse_gemini_response(
    response: Dict[str, Any]
) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """Parse the Gemini API response and return the text content and usage metadata"""
    if "error" in response:
        raise ValueError(f"Error from Gemini API: {response['error']}")

    if not ("candidates" in response and len(response["candidates"]) > 0):
        return None, None

    candidate = response["candidates"][0]
    if not ("content" in candidate and "parts" in candidate["content"]):
        return None, None

    for part in candidate["content"]["parts"]:
        if "text" in part:
            usage = response.get("usageMetadata")
            return part["text"], usage

    return None, None


def parse_args():
    """Parse command line arguments"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Summarize git diff changes using Gemini AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  git-refs-summary                    # Show unstaged changes
  git-refs-summary --from main        # Compare with main branch
  git-refs-summary --from HEAD~3      # Compare with 3 commits ago
  git-refs-summary --from v1.0 --to v2.0  # Compare two refs""",
    )
    parser.add_argument(
        "--from",
        dest="from_ref",
        help="Git reference to diff from (branch, commit SHA, etc). If not provided, shows unstaged changes",
    )
    parser.add_argument(
        "--to",
        dest="to_ref",
        help="Git reference to diff to (branch, commit SHA, etc). If not provided, uses current working tree",
    )
    parser.add_argument(
        "--no-term",
        action="store_true",
        help="Disable terminal formatting and markdown rendering",
    )
    return parser.parse_args()


def print_summary(
    text: str,
    usage: Optional[Dict[str, Any]],
    no_term: bool,
    from_ref: Optional[str] = None,
    to_ref: Optional[str] = None,
) -> None:
    """Print the summary with optional formatting and usage statistics"""
    # Print the git refs being used
    refs_msg = "\nAnalyzing changes "
    if not from_ref:
        refs_msg += f"for unstage changes"
    elif from_ref:
        refs_msg += f"from '{from_ref}'"
        if to_ref:
            refs_msg += f" to '{to_ref}'"
    print(refs_msg)

    if not no_term:
        console = Console()
        md = Markdown(text)
        console.print(md)
    else:
        print("-" * 40)
        print(text)

    # Print token usage if available
    if usage:
        print("\nToken Usage:")
        print(f"Prompt tokens:    {usage.get('promptTokenCount', 'N/A')}")
        print(f"Response tokens:  {usage.get('candidatesTokenCount', 'N/A')}")
        print(f"Total tokens:     {usage.get('totalTokenCount', 'N/A')}")


def main() -> None:
    """Main function"""
    try:
        args = parse_args()

        if args.from_ref:
            if args.to_ref:
                diff_command = f"git --no-pager diff {args.from_ref}..{args.to_ref}"
            else:
                diff_command = f"git --no-pager diff {args.from_ref}"
        else:
            diff_command = "git --no-pager diff"

        diff_output = subprocess.check_output(diff_command, shell=True, text=True)
        prompt = f"Here is the git diff:\n{diff_output}"
        response = get_gemini_response(prompt)

        text, usage = parse_gemini_response(response)
        if text is None:
            print("No summary content found in response")
            return

        print_summary(text, usage, args.no_term, args.from_ref, args.to_ref)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
