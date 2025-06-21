"""
PDFExporter: Exports HTML reports to PDF using WeasyPrint.
"""

from typing import Optional
import tempfile
import os

class PDFExporter:
    """Exports HTML reports to PDF files."""
    def export_report(self, html_report: str, output_path: Optional[str] = None) -> str:
        try:
            from weasyprint import HTML
            if output_path is None:
                fd, output_path = tempfile.mkstemp(suffix='.pdf')
                os.close(fd)
            HTML(string=html_report).write_pdf(output_path)
            return output_path
        except ImportError:
            # Fallback: create a simple text file with HTML content
            if output_path is None:
                fd, output_path = tempfile.mkstemp(suffix='.txt')
                os.close(fd)
            with open(output_path, 'w') as f:
                f.write("PDF export not available. HTML content:\n\n")
                f.write(html_report)
            return output_path
        except Exception as e:
            # Fallback: create error file
            if output_path is None:
                fd, output_path = tempfile.mkstemp(suffix='.txt')
                os.close(fd)
            with open(output_path, 'w') as f:
                f.write(f"PDF export failed: {str(e)}\n\nHTML content:\n{html_report}")
            return output_path 