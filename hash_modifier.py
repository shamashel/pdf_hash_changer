#!/usr/bin/env python3
"""
Script to create a copy of a PDF file with modified hash by appending random text.
"""

import os
import random
import string
import sys
from pathlib import Path

try:
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import io
except ImportError:
    print("Required dependencies not found. Install with:")
    print("pip install PyPDF2 reportlab")
    sys.exit(1)


def generate_random_text(length=50):
    """Generate random text with letters, numbers, and spaces."""
    chars = string.ascii_letters + string.digits + ' '
    return ''.join(random.choice(chars) for _ in range(length))


def create_text_overlay(text, page_size):
    """Create a PDF overlay with random text."""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=page_size)
    
    # Add text at bottom of page in very small, light gray font
    can.setFont("Helvetica", 6)
    can.setFillGray(0.9)
    can.drawString(50, 30, text)
    
    can.save()
    packet.seek(0)
    return PdfReader(packet)


def modify_pdf_hash(input_path, output_path=None, random_text_length=50):
    """
    Create a copy of PDF with modified hash by appending random text to last page.
    
    Args:
        input_path: Path to original PDF
        output_path: Path for modified copy (optional)
        random_text_length: Length of random text to append
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"PDF file not found: {input_path}")
    
    # Generate output path if not provided
    if output_path is None:
        stem = input_path.stem
        suffix = input_path.suffix
        counter = 1
        while True:
            output_path = input_path.parent / f"{stem}_modified_{counter}{suffix}"
            if not output_path.exists():
                break
            counter += 1
    else:
        output_path = Path(output_path)
    
    # Read the original PDF
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    # Copy all pages except the last one
    for i in range(len(reader.pages) - 1):
        writer.add_page(reader.pages[i])
    
    # Get the last page
    last_page = reader.pages[-1]
    
    # Generate random text and create overlay
    random_text = generate_random_text(random_text_length)
    
    # Get page size for overlay
    page_size = (float(last_page.mediabox.width), float(last_page.mediabox.height))
    text_overlay = create_text_overlay(random_text, page_size)
    
    # Merge overlay with last page
    last_page.merge_page(text_overlay.pages[0])
    writer.add_page(last_page)
    
    # Write the modified PDF
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"Modified PDF created: {output_path}")
    print(f"Random text added: {random_text}")
    return output_path


def main():
    """Main function to handle command line usage."""
    if len(sys.argv) < 2:
        print("Usage: python hash_modifier.py <input_pdf> [output_pdf] [text_length]")
        print("Example: python hash_modifier.py ECA_Compressor1.pdf")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else None
    text_length = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    
    try:
        modify_pdf_hash(input_pdf, output_pdf, text_length)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()