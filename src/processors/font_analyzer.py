"""
FontAnalyzer: Detailed font comparison for PDF files.
"""

from typing import List, Dict, Any

class FontAnalyzer:
    """Compares font lists for size, family, style, and color differences."""
    def compare(self, fonts1: List[Dict[str, Any]], fonts2: List[Dict[str, Any]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
        size_tolerance = config.get("size_tolerance", 0.5)
        diffs = []
        font_dict1 = {f["name"]: f for f in fonts1}
        font_dict2 = {f["name"]: f for f in fonts2}
        # Compare font names
        for name in set(font_dict1.keys()).union(font_dict2.keys()):
            f1 = font_dict1.get(name)
            f2 = font_dict2.get(name)
            if not f1:
                diffs.append({"type": "font", "change": "added", "font_name": name, "severity": "minor"})
            elif not f2:
                diffs.append({"type": "font", "change": "removed", "font_name": name, "severity": "minor"})
            else:
                # Size
                if abs(f1["size"] - f2["size"]) > size_tolerance:
                    diffs.append({"type": "font", "change": "size", "font_name": name, "reference_size": f1["size"], "new_size": f2["size"], "severity": "minor"})
                # Style
                if f1.get("flags") != f2.get("flags"):
                    diffs.append({"type": "font", "change": "style", "font_name": name, "reference_flags": f1.get("flags"), "new_flags": f2.get("flags"), "severity": "minor"})
                # Color
                if f1.get("color") != f2.get("color"):
                    diffs.append({"type": "font", "change": "color", "font_name": name, "reference_color": f1.get("color"), "new_color": f2.get("color"), "severity": "minor"})
        return diffs 