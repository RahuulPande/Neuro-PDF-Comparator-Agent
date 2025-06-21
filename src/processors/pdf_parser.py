"""
PDFParser: Extracts text, images, and font information from PDF files using PyMuPDF (fitz).
"""

import fitz
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PDFParser:
    """Extracts text, images, and font information from PDF files."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def validate_pdf(self, file_path: str) -> bool:
        try:
            with fitz.open(file_path) as doc:
                return doc.page_count > 0
        except Exception as e:
            self.logger.error(f"PDF validation failed for {file_path}: {e}")
            return False

    def parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extract text, images, and font info from a PDF file."""
        result = {
            "text": "",
            "images": [],
            "fonts": [],
            "layout": {}
        }
        try:
            with fitz.open(file_path) as doc:
                page_texts = []
                images = []
                fonts = set()
                for page_num, page in enumerate(doc):
                    page_texts.append({
                        "page_num": page_num + 1,
                        "text": page.get_text("text")
                    })
                    # Extract images
                    for img in page.get_images(full=True):
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        images.append({
                            "data": base_image["image"],
                            "ext": base_image["ext"],
                            "width": base_image.get("width"),
                            "height": base_image.get("height"),
                            "page": page_num + 1
                        })
                    # Extract font info
                    blocks = page.get_text("dict")["blocks"]
                    for block in blocks:
                        if block["type"] == 0:  # text block
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    fonts.add((span["font"], span["size"], span.get("color", 0), span.get("flags", 0)))
                # Format fonts
                result["fonts"] = [
                    {"name": f[0], "size": f[1], "color": f[2], "flags": f[3]} for f in fonts
                ]
                result["text"] = page_texts
                result["images"] = images
                # Layout info (page size)
                if doc.page_count > 0:
                    page0 = doc[0]
                    result["layout"]["page_size"] = {"width": page0.rect.width, "height": page0.rect.height}
        except Exception as e:
            self.logger.error(f"Failed to parse PDF {file_path}: {e}")
            result["error"] = str(e)
        return result 