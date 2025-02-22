# mr-summary

A tool to summarize git diffs using Gemini AI.

## Installation

```bash
uv pip install git+https://github.com/yourusername/mr-summary.git
```

## Usage

First, set your Gemini API key:
```bash
export GEMINI_API_KEY=your_api_key
```

Then run in any git repository:
```bash
# Show summary of unstaged changes
mr-summary

# Show summary of changes from a specific reference
mr-summary --from main

# Show summary with terminal formatting
mr-summary --term
```
