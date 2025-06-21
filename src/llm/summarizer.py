"""
Summarizer: Advanced LLM-based summarization for PDF differences.
"""

from typing import Dict, Any
from .local_llm import LocalLLMAnalyzer

class Summarizer:
    """Provides advanced summarization using local LLM."""
    def __init__(self):
        self.llm = LocalLLMAnalyzer()

    def summarize_differences(self, differences: Dict[str, Any]) -> str:
        analysis_data = {"differences": differences}
        return self.llm.generate_summary(analysis_data) 