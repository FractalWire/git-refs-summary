# refs-summary

A tool to summarize git diffs using Gemini AI.

## Installation

First, create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Unix/MacOS
# or
.venv\Scripts\activate     # On Windows
```

Then install the package:
```bash
uv pip install git+https://github.com/yourusername/refs-summary.git
```

## Usage

First, set your Gemini API key:
```bash
export GEMINI_API_KEY=your_api_key
```

Then run in any git repository:
```bash
# Show help
refs-summary --help

# Show summary of unstaged changes
refs-summary

# Show summary of changes from a specific reference
refs-summary --from main

# Compare changes between two references
refs-summary --from main --to HEAD

# Disable terminal formatting (plain text output)
refs-summary --no-term
```

## Options

- `--from REF`: Git reference to diff from (branch, commit SHA, etc). If not provided, shows unstaged changes
- `--to REF`: Git reference to diff to (branch, commit SHA, etc). If not provided, uses current working tree
- `--no-term`: Disable terminal formatting and markdown rendering (enabled by default)

## Development

To set up for development:

```bash
# Clone the repository
git clone https://github.com/yourusername/refs-summary.git
cd refs-summary

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Unix/MacOS

# Install in editable mode
uv pip install --editable .
```
