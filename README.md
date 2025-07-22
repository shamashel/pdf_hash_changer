# PDF Hash Changer

A Python utility for creating copies of PDF files with modified hash values by appending random text. This is useful for testing purposes when you need PDFs with identical content but different hash signatures.

## What it does

The application takes an input PDF file and creates a copy with a modified hash by:
- Adding a small, nearly invisible random text overlay to the last page
- Using light gray text (90% gray) in a small font (6pt) positioned at the bottom
- Preserving all original content while changing the file's hash signature

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. Install dependencies with:

```bash
uv sync
```

## Usage

### Command Line

```bash
# Basic usage - creates a copy with "_modified_1" suffix
uv run hash-modifier input.pdf

# Specify output filename
uv run hash-modifier input.pdf output.pdf

# Specify random text length (default: 50 characters)
uv run hash-modifier input.pdf output.pdf 100
```

### As a Module

```python
from hash_modifier import modify_pdf_hash

# Create modified copy
output_path = modify_pdf_hash("input.pdf")

# Specify output path and text length
output_path = modify_pdf_hash("input.pdf", "output.pdf", random_text_length=75)
```

## Requirements

- Python 3.7+
- PyPDF2 >= 3.0.0
- reportlab >= 3.6.0

## Examples

```bash
# Create a modified copy of document.pdf
uv run hash-modifier document.pdf

# Output: document_modified_1.pdf (with different hash than original)
```

The script will automatically generate unique filenames if no output path is specified, incrementing the counter to avoid overwriting existing files.