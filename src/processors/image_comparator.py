"""
ImageComparator: Binary image comparison using hashlib.
"""

import hashlib
from typing import List, Dict, Any

class ImageComparator:
    """Compares two lists of images using binary hash matching."""
    def compare(self, images1: List[Dict[str, Any]], images2: List[Dict[str, Any]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
        hash_algorithm = config.get("hash_algorithm", "sha256")
        hash_func = hashlib.sha256 if hash_algorithm == "sha256" else hashlib.md5
        diffs = []
        # Compare by index (assume same order)
        for idx, (img1, img2) in enumerate(zip(images1, images2)):
            hash1 = hash_func(img1["data"]).hexdigest() if img1 else None
            hash2 = hash_func(img2["data"]).hexdigest() if img2 else None
            identical = hash1 == hash2
            if not identical:
                diffs.append({
                    "index": idx,
                    "reference_hash": hash1,
                    "new_hash": hash2,
                    "identical": False,
                    "reference_size": len(img1["data"]) if img1 else 0,
                    "new_size": len(img2["data"]) if img2 else 0
                })
        # If different number of images
        if len(images1) != len(images2):
            diffs.append({
                "type": "image_count_mismatch",
                "reference_count": len(images1),
                "new_count": len(images2)
            })
        return diffs 