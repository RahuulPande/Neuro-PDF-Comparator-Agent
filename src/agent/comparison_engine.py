"""
PDF Comparison Engine - Core comparison logic for the Neuro AI agent.
"""

import logging
from typing import Dict, Any, List, Tuple
from difflib import SequenceMatcher
import hashlib
import re

logger = logging.getLogger(__name__)

class ComparisonEngine:
    """Core comparison engine for PDF content analysis."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def compare_text_exact(self, text1: str, text2: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Character-by-character text comparison with configurable sensitivity."""
        
        differences = []
        
        if config.get("strict", True):
            # Exact character-by-character comparison
            matcher = SequenceMatcher(None, text1, text2)
            
            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                if tag != 'equal':
                    # Found a difference
                    diff = {
                        "type": "text",
                        "operation": tag,
                        "reference_text": text1[i1:i2],
                        "new_text": text2[j1:j2],
                        "reference_position": (i1, i2),
                        "new_position": (j1, j2),
                        "context_before": text1[max(0, i1-50):i1],
                        "context_after": text1[i2:min(len(text1), i2+50)]
                    }
                    differences.append(diff)
        else:
            # Fuzzy comparison
            similarity = SequenceMatcher(None, text1, text2).ratio()
            if similarity < 0.95:  # 95% similarity threshold
                diff = {
                    "type": "text",
                    "operation": "fuzzy",
                    "similarity": similarity,
                    "reference_text": text1,
                    "new_text": text2
                }
                differences.append(diff)
                
        return differences
        
    def compare_text_with_options(self, text1: str, text2: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Text comparison with various options (whitespace, case, punctuation)."""
        
        # Apply preprocessing based on config
        processed_text1 = self._preprocess_text(text1, config)
        processed_text2 = self._preprocess_text(text2, config)
        
        # Perform comparison
        differences = self.compare_text_exact(processed_text1, processed_text2, config)
        
        # Add original text for context
        for diff in differences:
            diff["original_reference"] = text1
            diff["original_new"] = text2
            
        return differences
        
    def _preprocess_text(self, text: str, config: Dict[str, Any]) -> str:
        """Preprocess text based on configuration options."""
        
        if config.get("ignore_whitespace", False):
            # Normalize whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
        if config.get("ignore_case", False):
            # Convert to lowercase
            text = text.lower()
            
        if config.get("ignore_punctuation", False):
            # Remove punctuation
            text = re.sub(r'[^\w\s]', '', text)
            
        return text
        
    def compare_images_binary(self, img1_data: bytes, img2_data: bytes, config: Dict[str, Any]) -> Dict[str, Any]:
        """Binary image comparison using hash algorithms."""
        
        hash_algorithm = config.get("hash_algorithm", "sha256")
        
        if hash_algorithm == "sha256":
            hash_func = hashlib.sha256
        elif hash_algorithm == "md5":
            hash_func = hashlib.md5
        else:
            hash_func = hashlib.sha256
            
        # Calculate hashes
        hash1 = hash_func(img1_data).hexdigest()
        hash2 = hash_func(img2_data).hexdigest()
        
        # Compare hashes
        is_identical = hash1 == hash2
        
        result = {
            "type": "image",
            "identical": is_identical,
            "hash_algorithm": hash_algorithm,
            "reference_hash": hash1,
            "new_hash": hash2,
            "reference_size": len(img1_data),
            "new_size": len(img2_data)
        }
        
        if not is_identical:
            result["difference_type"] = "content"
            if len(img1_data) != len(img2_data):
                result["difference_type"] = "size"
                
        return result
        
    def compare_fonts_detailed(self, fonts1: List[Dict], fonts2: List[Dict], config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detailed font comparison including minor differences."""
        
        differences = []
        size_tolerance = config.get("size_tolerance", 0.5)
        
        # Create font dictionaries for easy lookup
        font_dict1 = {f.get("name", ""): f for f in fonts1}
        font_dict2 = {f.get("name", ""): f for f in fonts2}
        
        # Check for font family differences
        if config.get("family_check", True):
            families1 = set(f.get("family", "") for f in fonts1)
            families2 = set(f.get("family", "") for f in fonts2)
            
            added_families = families2 - families1
            removed_families = families1 - families2
            
            for family in added_families:
                differences.append({
                    "type": "font",
                    "change": "added_family",
                    "family": family,
                    "severity": "medium"
                })
                
            for family in removed_families:
                differences.append({
                    "type": "font",
                    "change": "removed_family",
                    "family": family,
                    "severity": "medium"
                })
                
        # Check for font size differences
        for font_name, font1 in font_dict1.items():
            if font_name in font_dict2:
                font2 = font_dict2[font_name]
                
                size1 = font1.get("size", 0)
                size2 = font2.get("size", 0)
                
                if abs(size1 - size2) > size_tolerance:
                    differences.append({
                        "type": "font",
                        "change": "size",
                        "font_name": font_name,
                        "reference_size": size1,
                        "new_size": size2,
                        "difference": abs(size1 - size2),
                        "severity": "minor" if abs(size1 - size2) <= 1.0 else "medium"
                    })
                    
        # Check for style differences
        if config.get("style_check", True):
            for font_name, font1 in font_dict1.items():
                if font_name in font_dict2:
                    font2 = font_dict2[font_name]
                    
                    style1 = font1.get("style", "")
                    style2 = font2.get("style", "")
                    
                    if style1 != style2:
                        differences.append({
                            "type": "font",
                            "change": "style",
                            "font_name": font_name,
                            "reference_style": style1,
                            "new_style": style2,
                            "severity": "medium"
                        })
                        
        # Check for color differences
        if config.get("color_check", False):
            for font_name, font1 in font_dict1.items():
                if font_name in font_dict2:
                    font2 = font_dict2[font_name]
                    
                    color1 = font1.get("color", "")
                    color2 = font2.get("color", "")
                    
                    if color1 != color2:
                        differences.append({
                            "type": "font",
                            "change": "color",
                            "font_name": font_name,
                            "reference_color": color1,
                            "new_color": color2,
                            "severity": "minor"
                        })
                        
        return differences
        
    def compare_layout_elements(self, layout1: Dict[str, Any], layout2: Dict[str, Any], config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compare layout elements like positioning and sizing."""
        
        differences = []
        position_tolerance = config.get("position_tolerance", 5)
        size_tolerance = config.get("size_tolerance", 5)
        
        # Compare page dimensions
        if "page_size" in layout1 and "page_size" in layout2:
            page1 = layout1["page_size"]
            page2 = layout2["page_size"]
            
            if abs(page1.get("width", 0) - page2.get("width", 0)) > size_tolerance:
                differences.append({
                    "type": "layout",
                    "change": "page_width",
                    "reference_width": page1.get("width", 0),
                    "new_width": page2.get("width", 0),
                    "severity": "major"
                })
                
            if abs(page1.get("height", 0) - page2.get("height", 0)) > size_tolerance:
                differences.append({
                    "type": "layout",
                    "change": "page_height",
                    "reference_height": page1.get("height", 0),
                    "new_height": page2.get("height", 0),
                    "severity": "major"
                })
                
        # Compare margins
        if config.get("margin_check", False):
            margins1 = layout1.get("margins", {})
            margins2 = layout2.get("margins", {})
            
            for margin_type in ["top", "bottom", "left", "right"]:
                margin1 = margins1.get(margin_type, 0)
                margin2 = margins2.get(margin_type, 0)
                
                if abs(margin1 - margin2) > position_tolerance:
                    differences.append({
                        "type": "layout",
                        "change": f"margin_{margin_type}",
                        "reference_margin": margin1,
                        "new_margin": margin2,
                        "severity": "minor"
                    })
                    
        return differences
        
    def calculate_similarity_score(self, differences: List[Dict[str, Any]], total_elements: int) -> float:
        """Calculate overall similarity score based on differences."""
        
        if total_elements == 0:
            return 1.0
            
        # Weight different types of changes
        weights = {
            "text": 1.0,
            "image": 0.8,
            "font": 0.3,
            "layout": 0.5
        }
        
        weighted_changes = 0
        for diff in differences:
            change_type = diff.get("type", "text")
            weight = weights.get(change_type, 1.0)
            weighted_changes += weight
            
        similarity = 1 - (weighted_changes / total_elements)
        return max(0.0, min(1.0, similarity))
        
    def categorize_changes(self, differences: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Categorize changes by type and severity."""
        
        categories = {
            "critical": [],
            "major": [],
            "minor": []
        }
        
        change_types = {
            "text": 0,
            "image": 0,
            "font": 0,
            "layout": 0
        }
        
        for diff in differences:
            # Categorize by severity
            severity = diff.get("severity", "minor")
            categories[severity].append(diff)
            
            # Count by type
            change_type = diff.get("type", "text")
            if change_type in change_types:
                change_types[change_type] += 1
                
        return {
            "by_severity": categories,
            "by_type": change_types,
            "total_changes": len(differences)
        }
        
    def generate_change_summary(self, differences: List[Dict[str, Any]]) -> str:
        """Generate a human-readable summary of changes."""
        
        if not differences:
            return "No differences found between the documents."
            
        categorization = self.categorize_changes(differences)
        
        summary_parts = []
        
        # Add severity summary
        for severity, changes in categorization["by_severity"].items():
            if changes:
                summary_parts.append(f"{len(changes)} {severity} change(s)")
                
        # Add type summary
        type_summary = []
        for change_type, count in categorization["by_type"].items():
            if count > 0:
                type_summary.append(f"{count} {change_type} change(s)")
                
        if type_summary:
            summary_parts.append(f"Types: {', '.join(type_summary)}")
            
        return f"Found {categorization['total_changes']} total changes: {', '.join(summary_parts)}" 