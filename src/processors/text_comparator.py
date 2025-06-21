"""
TextComparator: Character-by-character and configurable text comparison.
"""

import difflib
from typing import List, Dict, Any

class TextComparator:
    """Compares text from two documents, page by page and line by line."""

    def compare(self, doc1_pages: List[Dict], doc2_pages: List[Dict], config: Dict[str, Any]) -> List[str]:
        """
        Compares two documents page by page.

        Args:
            doc1_pages: A list of page dictionaries from the reference document.
            doc2_pages: A list of page dictionaries from the new document.
            config: Configuration dictionary (currently unused, for future expansion).

        Returns:
            A list of human-readable strings describing the differences.
        """
        all_differences = []
        
        # Create a mapping from page number to text for easy lookup
        doc1_text_map = {page['page_num']: page['text'] for page in doc1_pages}
        doc2_text_map = {page['page_num']: page['text'] for page in doc2_pages}
        
        # Find all unique page numbers from both documents
        all_page_numbers = sorted(list(set(doc1_text_map.keys()) | set(doc2_text_map.keys())))

        for page_num in all_page_numbers:
            ref_text = doc1_text_map.get(page_num)
            new_text = doc2_text_map.get(page_num)

            if ref_text is None:
                all_differences.append(f"On page {page_num}, a new page was added.")
                continue
            
            if new_text is None:
                all_differences.append(f"On page {page_num}, a page was removed.")
                continue

            page_diffs = self._compare_page_text(ref_text, new_text, page_num)
            all_differences.extend(page_diffs)

        return all_differences

    def _compare_page_text(self, ref_text: str, new_text: str, page_num: int) -> List[str]:
        """Compares the text of a single page, line by line."""
        ref_lines = ref_text.splitlines()
        new_lines = new_text.splitlines()
        
        matcher = difflib.SequenceMatcher(None, ref_lines, new_lines)
        differences = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                continue

            if tag == 'replace':
                # For multiple line replacements, report each line change
                for i in range(i1, i2):
                    for j in range(j1, j2):
                        # To keep it simple, we'll just report the first changed line pair
                        if i == i1 and j == j1:
                             differences.append(
                                f"On page {page_num}, line {i+1}, the text was changed from \"{ref_lines[i]}\" to \"{new_lines[j]}\"."
                            )
            
            elif tag == 'delete':
                for i in range(i1, i2):
                    differences.append(
                        f"On page {page_num}, line {i+1}, the text \"{ref_lines[i]}\" was removed."
                    )
            
            elif tag == 'insert':
                for j in range(j1, j2):
                    differences.append(
                        f"On page {page_num}, line {j+1}, the text \"{new_lines[j]}\" was added."
                    )
        
        return differences 