"""
LocalLLMAnalyzer: Integrates with local LLM (Ollama/LlamaCPP) for summarization and analysis.
"""

import logging
import requests
import json
import time
from typing import Dict, Any, Optional
from urllib.parse import urljoin

class LocalLLMAnalyzer:
    """Handles LLM-based summarization, severity assessment, and pattern recognition using Ollama."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3:latest", timeout: int = 30):
        self.logger = logging.getLogger(__name__)
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self.api_url = urljoin(base_url, "api/generate")
        
        # Test connection on initialization
        self._test_connection()
    
    def _test_connection(self):
        """Test the connection to Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                self.logger.info(f"Successfully connected to Ollama at {self.base_url}")
                self.logger.info(f"Using model: {self.model}")
            else:
                self.logger.warning(f"Ollama responded with status {response.status_code}")
        except Exception as e:
            self.logger.error(f"Failed to connect to Ollama: {str(e)}")
            self.logger.warning("LLM analysis will fall back to basic summaries")
    
    def _call_llm_api(self, prompt: str, system_prompt: Optional[str] = None) -> Optional[str]:
        """Make a call to the Ollama API."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Lower temperature for more consistent analysis
                    "top_p": 0.9,
                    "max_tokens": 1000
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            self.logger.debug(f"Calling Ollama API with prompt length: {len(prompt)}")
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                self.logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            self.logger.error("Ollama API request timed out")
            return None
        except Exception as e:
            self.logger.error(f"Error calling Ollama API: {str(e)}")
            return None
    
    def _format_differences_for_llm(self, differences: Dict[str, Any]) -> str:
        """Format differences data into a readable format for LLM analysis."""
        if not differences:
            return "No differences found between documents."
        
        formatted_diff = []
        for filename, diff_data in differences.items():
            formatted_diff.append(f"\nFile: {filename}")
            
            if "error" in diff_data:
                formatted_diff.append(f"  Error: {diff_data['error']}")
                continue
            
            # Format text differences
            if "text" in diff_data and diff_data["text"]:
                formatted_diff.append("  Text Changes:")
                for i, change in enumerate(diff_data["text"][:10], 1):  # Limit to first 10 changes
                    formatted_diff.append(f"    {i}. {change}")
                if len(diff_data["text"]) > 10:
                    formatted_diff.append(f"    ... and {len(diff_data['text']) - 10} more text changes")
            
            # Format image differences
            if "images" in diff_data and diff_data["images"]:
                formatted_diff.append("  Image Changes:")
                for change in diff_data["images"]:
                    formatted_diff.append(f"    - {change}")
            
            # Format font differences
            if "fonts" in diff_data and diff_data["fonts"]:
                formatted_diff.append("  Font Changes:")
                for change in diff_data["fonts"]:
                    formatted_diff.append(f"    - {change}")
        
        return "\n".join(formatted_diff)

    def generate_summary(self, analysis_data: Dict[str, Any]) -> str:
        """Generate a business-friendly summary of PDF differences using LLM."""
        differences = analysis_data.get("differences", {})
        testing_mode = analysis_data.get("testing_mode", "regression")
        
        if not differences:
            if testing_mode == "regression":
                return "✅ REGRESSION TEST PASSED: All files are identical. No issues detected."
            else:
                return "✅ SIT TEST COMPLETED: No differences detected between documents."
        
        # Format differences for LLM
        formatted_diff = self._format_differences_for_llm(differences)
        
        # Create context-specific system prompt
        if testing_mode == "regression":
            system_prompt = """You are a senior compliance officer at a major investment bank (like UBS) conducting regression testing on investment proposal documents.
            
            CRITICAL CONTEXT: In regression testing, ANY change is a FAILURE. Even a missing dot, comma, or space is a critical issue that could have legal/compliance implications.
            
            Your role is to:
            1. Identify EVERY change as a potential compliance risk
            2. Provide a clear pass/fail assessment
            3. Highlight specific issues that need immediate attention
            4. Calculate pass percentage (files with NO changes / total files)
            5. Emphasize the business impact of any changes
            
            Focus on:
            - Legal disclaimers and compliance text
            - Financial figures and calculations
            - Document structure and formatting
            - Any deviation from approved templates
            
            Be direct and business-focused. Use terms like "FAILURE", "CRITICAL ISSUE", "COMPLIANCE RISK"."""
        else:
            system_prompt = """You are a senior business analyst conducting SIT (System Integration Testing) on investment proposal documents.
            
            CONTEXT: In SIT testing, some changes are expected and intentional. Focus on validating that changes are appropriate and expected.
            
            Your role is to:
            1. Distinguish between expected and unexpected changes
            2. Validate that changes align with business requirements
            3. Identify any unintended modifications
            4. Provide insights on change patterns and business impact
            
            Focus on:
            - Whether changes appear intentional and appropriate
            - Business logic and functionality validation
            - Risk assessment of any unexpected changes
            - Overall system integration success"""
        
        # Create analysis prompt
        total_files = len(differences)
        files_with_changes = sum(1 for diff in differences.values() if isinstance(diff, dict) and any(diff.get(cat, []) for cat in ["text", "images", "fonts"]))
        pass_percentage = ((total_files - files_with_changes) / total_files * 100) if total_files > 0 else 100
        
        if testing_mode == "regression":
            prompt = f"""REGRESSION TEST ANALYSIS - Investment Proposal Documents

{formatted_diff}

TEST RESULTS:
- Total Files: {total_files}
- Files with Changes: {files_with_changes}
- Pass Rate: {pass_percentage:.1f}%

ANALYSIS REQUIREMENTS:
Based on the differences, provide a concise, professional summary for a business executive. Use markdown for formatting.
- Start with a clear, bolded verdict: **REGRESSION TEST: FAILURE** or **REGRESSION TEST: PASSED**.
- Use a heading `### Specific Compliance Risks` and list each risk as a bullet point.
- Use a heading `### Issue Locations` and list the exact file, page, and line numbers for each issue.
- Use a heading `### Business Impact and Urgency` to explain the consequences.
- Your entire response must be formatted as clean, readable markdown.

Provide your analysis below:
"""
        else:
            prompt = f"""SIT TEST ANALYSIS - Investment Proposal Documents

{formatted_diff}

TEST RESULTS:
- Total Files: {total_files}
- Files with Changes: {files_with_changes}
- Change Rate: {(files_with_changes/total_files*100):.1f}%

ANALYSIS REQUIREMENTS:
Based on the differences, provide a concise, professional summary for a business analyst. Use markdown for formatting.
- Start with a clear, bolded summary of the findings.
- Use a heading `### Change Validation` and use bullet points to assess if changes seem intentional.
- Use a heading `### Potential Issues` to list any unexpected or problematic modifications.
- Use a heading `### Business Insights` to provide commentary on integration success.
- Your entire response must be formatted as clean, readable markdown.

Provide your analysis below:
"""
        
        # Call LLM
        llm_response = self._call_llm_api(prompt, system_prompt)
        
        if llm_response:
            return llm_response
        else:
            # Fallback to basic summary
            if testing_mode == "regression":
                if files_with_changes == 0:
                    return f"✅ REGRESSION TEST PASSED: All {total_files} files are identical. Pass rate: 100%"
                else:
                    return f"❌ REGRESSION TEST FAILED: {files_with_changes}/{total_files} files have changes. Pass rate: {pass_percentage:.1f}%"
            else:
                return f"SIT TEST COMPLETED: {files_with_changes}/{total_files} files have changes ({pass_percentage:.1f}% unchanged)."

    def assess_severity(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Categorize changes by importance (Critical/Major/Minor) using LLM."""
        differences = analysis_data.get("differences", {})
        testing_mode = analysis_data.get("testing_mode", "regression")
        
        if not differences:
            return {"Critical": [], "Major": [], "Minor": []}
        
        formatted_diff = self._format_differences_for_llm(differences)
        
        if testing_mode == "regression":
            system_prompt = """You are a compliance officer at an investment bank conducting regression testing.
            
            REGRESSION TESTING RULES:
            - ANY change = CRITICAL severity (compliance risk)
            - Missing disclaimers, legal text, or financial figures = CRITICAL
            - Formatting changes that could affect document interpretation = CRITICAL
            - Only truly cosmetic changes (spacing, font size) = MAJOR
            
            In regression testing, we expect ZERO changes. Any deviation is a compliance concern."""
            
            prompt = f"""REGRESSION TEST SEVERITY ASSESSMENT

{formatted_diff}

ASSESSMENT RULES:
- ANY change in investment proposal documents is a compliance risk
- Missing legal disclaimers = CRITICAL
- Changed financial figures = CRITICAL  
- Modified document structure = CRITICAL
- Only minor formatting = MAJOR

Categorize each file:
Critical: [files with ANY changes - compliance risks]
Major: [files with only cosmetic changes]
Minor: [files with no changes]

Analysis:"""
        else:
            system_prompt = """You are a business analyst conducting SIT testing on investment proposal documents.
            
            SIT TESTING RULES:
            - Expected changes = MINOR severity (intentional updates)
            - Unexpected but appropriate changes = MAJOR severity
            - Compliance risks or inappropriate changes = CRITICAL severity
            
            In SIT testing, some changes are expected and intentional."""
            
            prompt = f"""SIT TEST SEVERITY ASSESSMENT

{formatted_diff}

ASSESSMENT RULES:
- Expected/intentional changes = MINOR
- Unexpected but appropriate changes = MAJOR
- Compliance risks or inappropriate changes = CRITICAL

Categorize each file:
Critical: [files with compliance risks or inappropriate changes]
Major: [files with unexpected but acceptable changes]
Minor: [files with expected changes or no changes]

Analysis:"""
        
        llm_response = self._call_llm_api(prompt, system_prompt)
        
        if llm_response:
            # Parse the response to extract severity categories
            severity = {"Critical": [], "Major": [], "Minor": []}
            
            lines = llm_response.split('\n')
            current_category = None
            
            for line in lines:
                line = line.strip()
                if line.startswith("Critical:"):
                    current_category = "Critical"
                    files = line.replace("Critical:", "").strip()
                    if files:
                        severity["Critical"].extend([f.strip() for f in files.split(',')])
                elif line.startswith("Major:"):
                    current_category = "Major"
                    files = line.replace("Major:", "").strip()
                    if files:
                        severity["Major"].extend([f.strip() for f in files.split(',')])
                elif line.startswith("Minor:"):
                    current_category = "Minor"
                    files = line.replace("Minor:", "").strip()
                    if files:
                        severity["Minor"].extend([f.strip() for f in files.split(',')])
            
            return severity
        else:
            # Fallback to context-aware severity assessment
            severity = {"Critical": [], "Major": [], "Minor": []}
            for fname, diff in differences.items():
                if isinstance(diff, dict):
                    total_changes = len(diff.get("text", [])) + len(diff.get("images", [])) + len(diff.get("fonts", []))
                    if testing_mode == "regression":
                        # In regression, any change is critical
                        if total_changes > 0:
                            severity["Critical"].append(fname)
                        else:
                            severity["Minor"].append(fname)
                    else:
                        # In SIT, assess based on change volume
                        if total_changes > 10:
                            severity["Critical"].append(fname)
                        elif total_changes > 3:
                            severity["Major"].append(fname)
                        else:
                            severity["Minor"].append(fname)
            return severity

    def identify_patterns(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify patterns or trends in document changes using LLM."""
        differences = analysis_data.get("differences", {})
        
        if not differences:
            return {"patterns": [], "trends": [], "insights": []}
        
        formatted_diff = self._format_differences_for_llm(differences)
        
        system_prompt = """You are a document analysis expert who identifies patterns and trends in document changes.
        Look for:
        - Recurring types of changes (budget updates, date changes, personnel changes)
        - Document evolution patterns
        - Consistency in formatting or structure changes
        - Business process implications
        
        Provide insights that help understand the document lifecycle and change patterns."""
        
        prompt = f"""Analyze the following document differences and identify patterns, trends, and insights:

{formatted_diff}

Please identify:
1. What patterns or trends do you see in these changes?
2. What types of modifications are most common?
3. What insights can be drawn about the document evolution?
4. Are there any business process implications?

Provide your analysis in a structured format:
Patterns: [list of identified patterns]
Trends: [list of observed trends]
Insights: [list of business insights]"""
        
        llm_response = self._call_llm_api(prompt, system_prompt)
        
        if llm_response:
            # Parse the response to extract patterns, trends, and insights
            patterns = []
            trends = []
            insights = []
            
            lines = llm_response.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if line.startswith("Patterns:"):
                    current_section = "patterns"
                    content = line.replace("Patterns:", "").strip()
                    if content:
                        patterns.append(content)
                elif line.startswith("Trends:"):
                    current_section = "trends"
                    content = line.replace("Trends:", "").strip()
                    if content:
                        trends.append(content)
                elif line.startswith("Insights:"):
                    current_section = "insights"
                    content = line.replace("Insights:", "").strip()
                    if content:
                        insights.append(content)
                elif line and current_section:
                    if current_section == "patterns":
                        patterns.append(line)
                    elif current_section == "trends":
                        trends.append(line)
                    elif current_section == "insights":
                        insights.append(line)
            
            return {
                "patterns": patterns,
                "trends": trends,
                "insights": insights,
                "raw_analysis": llm_response
            }
        else:
            # Fallback to basic pattern analysis
            pattern_counts = {}
            for fname, diff in differences.items():
                if isinstance(diff, dict):
                    for category in diff.keys():
                        if category != "error":
                            pattern_counts[category] = pattern_counts.get(category, 0) + 1
            
            return {
                "patterns": [f"Most common change type: {sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)[0][0] if pattern_counts else 'None'}"],
                "trends": [f"Total files with changes: {len(differences)}"],
                "insights": ["Basic pattern analysis available"],
                "pattern_counts": pattern_counts
            } 