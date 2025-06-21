"""
Main PDF Comparison Neuro AI Agent.
This agent orchestrates the entire PDF comparison workflow using Cognizant's Neuro AI framework.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import time
import sys
import os

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .neuro_ai_mock import Agent, Task, Workflow, WorkflowStep, TaskPriority, LearningModule
from ..processors.pdf_parser import PDFParser
from ..processors.text_comparator import TextComparator
from ..processors.image_comparator import ImageComparator
from ..processors.font_analyzer import FontAnalyzer
from ..llm.local_llm import LocalLLMAnalyzer
from ..reports.html_generator import HTMLReportGenerator
from ..reports.pdf_exporter import PDFExporter
from config.settings import get_config, get_sensitivity_config

logger = logging.getLogger(__name__)

class PDFComparisonNeuroAgent(Agent):
    """Main Neuro AI agent for PDF comparison using Cognizant's framework."""
    
    def __init__(self):
        super().__init__(
            name="PDF_Comparison_Agent",
            description="Sophisticated PDF comparison agent using Neuro AI framework"
        )
        
        # Load configuration
        self.config = get_config()
        
        # Initialize components
        self.pdf_parser = PDFParser()
        self.text_comparator = TextComparator()
        self.image_comparator = ImageComparator()
        self.font_analyzer = FontAnalyzer()
        self.llm_analyzer = LocalLLMAnalyzer()
        self.html_generator = HTMLReportGenerator()
        self.pdf_exporter = PDFExporter()
        self.learning_module = LearningModule()
        
        # Setup tasks and workflows
        self.setup_tasks()
        self.setup_workflows()
        
        logger.info("PDF Comparison Neuro AI Agent initialized successfully")
        
    def setup_tasks(self):
        """Define Neuro AI tasks for the agent."""
        
        # Task 1: Scan folders
        self.add_task(Task(
            name="scan_folders",
            func=self.scan_folders,
            description="Scan reference and new folders for PDF files",
            timeout=60,
            retry_attempts=2,
            priority=TaskPriority.HIGH
        ))
        
        # Task 2: Validate files
        self.add_task(Task(
            name="validate_files",
            func=self.validate_files,
            description="Validate PDF files and check compatibility",
            timeout=30,
            retry_attempts=1,
            priority=TaskPriority.HIGH
        ))
        
        # Task 3: Parse PDFs
        self.add_task(Task(
            name="parse_pdfs",
            func=self.parse_pdfs,
            description="Parse PDF content and extract text, images, fonts",
            timeout=300,
            retry_attempts=2,
            priority=TaskPriority.NORMAL,
            parallel=True,
            max_workers=4
        ))
        
        # Task 4: Compare content
        self.add_task(Task(
            name="compare_content",
            func=self.compare_content,
            description="Compare PDF content using configured sensitivity",
            timeout=600,
            retry_attempts=3,
            priority=TaskPriority.NORMAL,
            parallel=True,
            max_workers=4
        ))
        
        # Task 5: Analyze with LLM
        self.add_task(Task(
            name="analyze_with_llm",
            func=self.analyze_with_llm,
            description="Generate intelligent summaries and assessments",
            timeout=120,
            retry_attempts=2,
            priority=TaskPriority.NORMAL
        ))
        
        # Task 6: Generate report
        self.add_task(Task(
            name="generate_report",
            func=self.generate_report,
            description="Create visual HTML report with differences",
            timeout=180,
            retry_attempts=1,
            priority=TaskPriority.NORMAL
        ))
        
        # Task 7: Update learning
        self.add_task(Task(
            name="update_learning",
            func=self.update_learning,
            description="Update learning module with comparison patterns",
            timeout=60,
            retry_attempts=1,
            priority=TaskPriority.LOW
        ))
        
    def setup_workflows(self):
        """Setup Neuro AI workflows."""
        
        # Main comparison workflow
        workflow = Workflow(
            name="PDF_Comparison_Workflow",
            description="Complete PDF comparison workflow"
        )
        
        # Add workflow steps
        workflow.add_step(WorkflowStep(
            name="scan",
            task="scan_folders",
            description="Scan folders for PDF files"
        ))
        
        workflow.add_step(WorkflowStep(
            name="validate",
            task="validate_files",
            description="Validate PDF files",
            dependencies=["scan"]
        ))
        
        workflow.add_step(WorkflowStep(
            name="parse",
            task="parse_pdfs",
            description="Parse PDF content",
            dependencies=["validate"],
            parallel=True,
            max_workers=4
        ))
        
        workflow.add_step(WorkflowStep(
            name="compare",
            task="compare_content",
            description="Compare PDF content",
            dependencies=["parse"],
            parallel=True,
            max_workers=4
        ))
        
        workflow.add_step(WorkflowStep(
            name="analyze",
            task="analyze_with_llm",
            description="LLM analysis",
            dependencies=["compare"]
        ))
        
        workflow.add_step(WorkflowStep(
            name="report",
            task="generate_report",
            description="Generate reports",
            dependencies=["analyze"]
        ))
        
        workflow.add_step(WorkflowStep(
            name="learn",
            task="update_learning",
            description="Update learning module",
            dependencies=["report"]
        ))
        
        # Set agent and store workflow
        workflow.set_agent(self)
        self.workflows["main"] = workflow
        
    async def run_comparison_workflow(self, ref_folder: str, new_folder: str, 
                                    sensitivity_level: str = "medium", testing_mode: str = "regression") -> Dict[str, Any]:
        """Run the complete PDF comparison workflow using Neuro AI automation."""
        
        logger.info(f"Starting PDF comparison workflow")
        logger.info(f"Reference folder: {ref_folder}")
        logger.info(f"New folder: {new_folder}")
        logger.info(f"Sensitivity level: {sensitivity_level}")
        logger.info(f"Testing mode: {testing_mode}")
        
        # Get sensitivity configuration
        sensitivity_config = get_sensitivity_config(sensitivity_level)
        
        # Prepare workflow context
        context = {
            "ref_folder": ref_folder,
            "new_folder": new_folder,
            "sensitivity_config": sensitivity_config,
            "testing_mode": testing_mode,
            "config": self.config,
            "start_time": time.time()
        }
        
        try:
            # Execute workflow
            workflow = self.workflows["main"]
            results = await workflow.execute(context)
            
            # Add metadata to results
            results["metadata"] = {
                "workflow_name": workflow.name,
                "sensitivity_level": sensitivity_level,
                "execution_time": time.time() - context["start_time"],
                "status": "completed"
            }
            
            logger.info(f"Workflow completed successfully in {results['metadata']['execution_time']:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Workflow failed: {str(e)}")
            raise
            
    def scan_folders(self, ref_folder: str, new_folder: str, **kwargs) -> Dict[str, Any]:
        """Scan reference and new folders for PDF files."""
        logger.info("Scanning folders for PDF files")
        
        ref_path = Path(ref_folder)
        new_path = Path(new_folder)
        
        if not ref_path.exists():
            raise ValueError(f"Reference folder does not exist: {ref_folder}")
        if not new_path.exists():
            raise ValueError(f"New folder does not exist: {new_folder}")
            
        # Find PDF files
        ref_files = list(ref_path.glob("*.pdf"))
        new_files = list(new_path.glob("*.pdf"))
        
        # Create file mapping
        file_mapping = {}
        for ref_file in ref_files:
            new_file = new_path / ref_file.name
            if new_file.exists():
                file_mapping[ref_file.name] = {
                    "reference": str(ref_file),
                    "new": str(new_file)
                }
        
        result = {
            "ref_files": [str(f) for f in ref_files],
            "new_files": [str(f) for f in new_files],
            "file_mapping": file_mapping,
            "total_files": len(file_mapping)
        }
        
        logger.info(f"Found {len(ref_files)} reference files, {len(new_files)} new files")
        logger.info(f"Mapped {len(file_mapping)} files for comparison")
        
        return result
        
    def validate_files(self, ref_files: List[str], new_files: List[str], 
                      file_mapping: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Validate PDF files and check compatibility."""
        logger.info("Validating PDF files")
        
        validated_files = {}
        validation_errors = []
        
        for filename, paths in file_mapping.items():
            try:
                # Validate reference file
                ref_valid = self.pdf_parser.validate_pdf(paths["reference"])
                new_valid = self.pdf_parser.validate_pdf(paths["new"])
                
                if ref_valid and new_valid:
                    validated_files[filename] = paths
                else:
                    validation_errors.append({
                        "filename": filename,
                        "error": "Invalid PDF file",
                        "ref_valid": ref_valid,
                        "new_valid": new_valid
                    })
                    
            except Exception as e:
                validation_errors.append({
                    "filename": filename,
                    "error": str(e)
                })
                
        result = {
            "validated_files": validated_files,
            "validation_errors": validation_errors,
            "valid_count": len(validated_files)
        }
        
        logger.info(f"Validated {len(validated_files)} files, {len(validation_errors)} errors")
        return result
        
    def parse_pdfs(self, validated_files: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Parse PDF content and extract text, images, fonts."""
        logger.info("Parsing PDF content")
        
        parsed_content = {}
        
        for filename, paths in validated_files.items():
            try:
                logger.info(f"Parsing {filename}")
                
                # Parse reference file
                ref_content = self.pdf_parser.parse_pdf(paths["reference"])
                
                # Parse new file
                new_content = self.pdf_parser.parse_pdf(paths["new"])
                
                parsed_content[filename] = {
                    "reference": ref_content,
                    "new": new_content
                }
                
            except Exception as e:
                logger.error(f"Error parsing {filename}: {str(e)}")
                parsed_content[filename] = {
                    "error": str(e)
                }
                
        result = {
            "parsed_content": parsed_content,
            "success_count": len([c for c in parsed_content.values() if "error" not in c])
        }
        
        logger.info(f"Parsed {result['success_count']} files successfully")
        return result
        
    def compare_content(self, parsed_content: Dict[str, Any],
                       sensitivity_config: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Compare PDF content using configured sensitivity."""
        logger.info("Comparing PDF content")
        
        all_differences = {}
        change_summary = {
            "total_files": 0,
            "files_with_changes": 0,
            "total_changes": 0,
        }

        for filename, content in parsed_content.items():
            if "error" in content:
                all_differences[filename] = {"error": content["error"]}
                continue
            
            change_summary["total_files"] += 1
            
            try:
                logger.info(f"Comparing {filename}")
                
                # --- New Text Comparison ---
                text_diff = self.text_comparator.compare(
                    content["reference"]["text"],
                    content["new"]["text"],
                    sensitivity_config["text"]
                )
                
                # --- Simplified Image Comparison ---
                image_diff_count = abs(len(content["reference"]["images"]) - len(content["new"]["images"]))
                image_diff = [f"{image_diff_count} image(s) changed."] if image_diff_count > 0 else []

                # --- Simplified Font Comparison ---
                font_diff_count = abs(len(content["reference"]["fonts"]) - len(content["new"]["fonts"]))
                font_diff = [f"{font_diff_count} font(s) changed."] if font_diff_count > 0 else []

                # Combine all differences into a single list of strings
                file_differences = {
                    "text": text_diff,
                    "images": image_diff,
                    "fonts": font_diff,
                }
                
                total_diffs = len(text_diff) + len(image_diff) + len(font_diff)
                if total_diffs > 0:
                    change_summary["files_with_changes"] += 1
                    change_summary["total_changes"] += total_diffs
                    all_differences[filename] = file_differences

            except Exception as e:
                logger.error(f"Error comparing {filename}: {str(e)}")
                all_differences[filename] = {"error": str(e)}
                
        result = {
            "differences": all_differences,
            "change_summary": change_summary
        }
        
        logger.info(f"Comparison completed: {change_summary['files_with_changes']} files with changes")
        return result
        
    def analyze_with_llm(self, differences: Dict[str, Any], testing_mode: str = "regression", **kwargs) -> Dict[str, Any]:
        """Generate intelligent summaries and assessments using LLM."""
        logger.info("Analyzing differences with LLM")
        
        try:
            # Prepare data for LLM analysis
            analysis_data = {
                "differences": differences,
                "testing_mode": testing_mode,
                "config": self.config["llm"]
            }
            
            # Generate intelligent summary
            intelligent_summary = self.llm_analyzer.generate_summary(analysis_data)
            
            # Assess severity
            severity_assessment = self.llm_analyzer.assess_severity(analysis_data)
            
            # Identify patterns
            pattern_analysis = self.llm_analyzer.identify_patterns(analysis_data)
            
            result = {
                "intelligent_summary": intelligent_summary,
                "severity_assessment": severity_assessment,
                "pattern_analysis": pattern_analysis
            }
            
            logger.info("LLM analysis completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"LLM analysis failed: {str(e)}")
            return {
                "intelligent_summary": "LLM analysis unavailable",
                "severity_assessment": {},
                "pattern_analysis": {},
                "error": str(e)
            }
            
    def generate_report(self, differences: Dict[str, Any], 
                       intelligent_summary: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Create visual HTML report with differences."""
        logger.info("Generating visual report")
        
        try:
            # Extract the actual intelligent summary from the analyze step result
            if isinstance(intelligent_summary, dict) and "intelligent_summary" in intelligent_summary:
                summary_text = intelligent_summary["intelligent_summary"]
            else:
                summary_text = str(intelligent_summary) if intelligent_summary else "No summary available"
            
            # Create a proper intelligent_summary dict for the HTML generator
            intelligent_summary_dict = {
                "intelligent_summary": summary_text
            }
            
            # Generate HTML report
            logger.info("Generating HTML report...")
            html_report = self.html_generator.generate_report(
                differences=differences,
                intelligent_summary=intelligent_summary_dict,
                config=self.config["report"]
            )
            logger.info(f"HTML report generated, length: {len(html_report)}")
            
            # Generate PDF report
            logger.info("Generating PDF report...")
            pdf_report = self.pdf_exporter.export_report(html_report)
            logger.info(f"PDF report generated at: {pdf_report}")
            
            # Generate Excel report
            logger.info("Generating Excel report...")
            excel_report = self.html_generator.generate_excel_report(differences)
            logger.info(f"Excel report generated at: {excel_report}")
            
            # Verify files exist and have content
            if os.path.exists(pdf_report):
                pdf_size = os.path.getsize(pdf_report)
                logger.info(f"PDF file size: {pdf_size} bytes")
            else:
                logger.warning(f"PDF file does not exist: {pdf_report}")
                
            if os.path.exists(excel_report):
                excel_size = os.path.getsize(excel_report)
                logger.info(f"Excel file size: {excel_size} bytes")
            else:
                logger.warning(f"Excel file does not exist: {excel_report}")
            
            result = {
                "html_report": html_report,
                "pdf_report": pdf_report,
                "excel_report": excel_report
            }
            
            logger.info("Report generation completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            return {
                "error": str(e)
            }
            
    def update_learning(self, differences: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Update learning module with comparison patterns."""
        logger.info("Updating learning module")
        
        try:
            # Extract patterns from differences
            for filename, file_diff in differences.items():
                if "error" not in file_diff:
                    self.learning_module.update_patterns({
                        "filename": filename,
                        "differences": file_diff,
                        "timestamp": time.time()
                    })
                    
            # Update statistics
            total_changes = sum(
                diff.get("total_changes", 0) 
                for diff in differences.values() 
                if "error" not in diff
            )
            
            self.learning_module.update_statistics("total_changes", total_changes)
            self.learning_module.update_statistics("files_processed", len(differences))
            
            result = {
                "patterns_updated": len(differences),
                "statistics_updated": True
            }
            
            logger.info("Learning module updated successfully")
            return result
            
        except Exception as e:
            logger.error(f"Learning module update failed: {str(e)}")
            return {
                "error": str(e)
            }
            
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights from the learning module."""
        frequent_patterns = self.learning_module.get_frequent_patterns()
        statistics = self.learning_module.statistics
        
        return {
            "frequent_patterns": frequent_patterns,
            "statistics": statistics
        }
        
    def shutdown(self):
        """Shutdown the agent and cleanup resources."""
        logger.info("Shutting down PDF Comparison Neuro AI Agent")
        self.executor.shutdown(wait=True) 