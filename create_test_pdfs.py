"""
Create test PDF files for testing the PDF comparison agent.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import os

def create_test_pdf(filename, content, title="Test Document"):
    """Create a simple PDF file with given content."""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, title)
    
    # Content
    c.setFont("Helvetica", 12)
    y_position = height - 150
    for line in content.split('\n'):
        if y_position > 100:
            c.drawString(100, y_position, line)
            y_position -= 20
    
    c.save()

# Create reference PDF
ref_content = """This is a reference document.
It contains important information about the project.
The total budget is $50,000.
The deadline is December 31, 2024.
Team members: John, Jane, and Bob."""

create_test_pdf("test_data/reference/document1.pdf", ref_content, "Reference Document 1")

# Create new PDF with changes
new_content = """This is a new document.
It contains updated information about the project.
The total budget is $55,000.
The deadline is January 15, 2025.
Team members: John, Jane, Bob, and Alice."""

create_test_pdf("test_data/new/document1.pdf", new_content, "New Document 1")

# Create another reference PDF
ref_content2 = """Project Status Report
Current Status: In Progress
Completion: 75%
Next Milestone: Testing Phase"""

create_test_pdf("test_data/reference/document2.pdf", ref_content2, "Reference Document 2")

# Create matching new PDF
new_content2 = """Project Status Report
Current Status: In Progress
Completion: 80%
Next Milestone: Testing Phase
Additional Notes: All tests passed."""

create_test_pdf("test_data/new/document2.pdf", new_content2, "New Document 2")

print("Test PDF files created successfully!")
print("Reference files: test_data/reference/")
print("New files: test_data/new/") 