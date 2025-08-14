import streamlit as st
import os
import sys
from pathlib import Path
import asyncio
import tempfile
import shutil
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import our modules
try:
    from src.agent.neuro_agent import PDFComparisonAgent
    from src.processors.pdf_parser import PDFParser
    from src.processors.text_comparator import TextComparator
    from src.processors.image_comparator import ImageComparator
    from src.processors.font_analyzer import FontAnalyzer
    from src.reports.html_generator import HTMLReportGenerator
    from src.reports.pdf_exporter import PDFExporter
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Please ensure all dependencies are installed and the project structure is correct.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="PDF Comparison Agent - AI-Powered Document Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #ffd700, #ffed4e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
    }
    
    .status-success {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .status-warning {
        background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .status-error {
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #ffd700;
    }
    
    .metric-label {
        color: #e0e0e0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {'reference': [], 'new': []}

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 PDF Comparison Agent</h1>
    <p style="font-size: 1.2rem;">AI-Powered Document Analysis & Regression Testing</p>
    <p style="font-size: 1rem; opacity: 0.8;">Built with Cognizant Neuro AI Framework</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Quick Links")
    st.markdown("""
    - [LinkedIn Profile](https://www.linkedin.com/in/rahuulpande/)
    - [GitHub Portfolio](https://github.com/rahuulpande/)
    - [Email Contact](mailto:rahuulpande@gmail.com)
    """)
    
    st.markdown("## 🚀 About This Project")
    st.markdown("""
    This PDF Comparison Agent demonstrates:
    - **Neuro AI Integration** with intelligent workflows
    - **Advanced PDF Analysis** (text, fonts, images, layout)
    - **Context-Aware Testing** (regression vs SIT)
    - **Professional Reporting** with business insights
    
    Perfect for financial document validation and compliance testing.
    """)

# Main content
st.markdown("## 📁 Upload PDF Files for Comparison")

# File upload section
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📋 Reference Files (Base Documents)")
    reference_files = st.file_uploader(
        "Upload reference PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        key="reference_uploader"
    )
    
    if reference_files:
        st.session_state.uploaded_files['reference'] = reference_files
        st.success(f"✅ {len(reference_files)} reference file(s) uploaded")

with col2:
    st.markdown("### 🆕 New Files (Documents to Compare)")
    new_files = st.file_uploader(
        "Upload new PDF files to compare",
        type=['pdf'],
        accept_multiple_files=True,
        key="new_uploader"
    )
    
    if new_files:
        st.session_state.uploaded_files['new'] = new_files
        st.success(f"✅ {len(new_files)} new file(s) uploaded")

# Configuration section
st.markdown("## ⚙️ Comparison Configuration")

col1, col2, col3 = st.columns(3)

with col1:
    sensitivity_level = st.selectbox(
        "Sensitivity Level",
        ["low", "medium", "high"],
        index=2,
        help="Higher sensitivity detects smaller changes"
    )

with col2:
    testing_mode = st.selectbox(
        "Testing Mode",
        ["regression", "sit"],
        help="Regression: Expect identical files, SIT: Expect some changes"
    )

with col3:
    comparison_type = st.multiselect(
        "Comparison Types",
        ["text", "fonts", "images", "layout"],
        default=["text", "fonts", "images"],
        help="Select what to compare"
    )

# Run comparison button
if st.button("🚀 Run AI-Powered Comparison", type="primary", use_container_width=True):
    if not st.session_state.uploaded_files['reference'] or not st.session_state.uploaded_files['new']:
        st.error("❌ Please upload both reference and new files")
    else:
        with st.spinner("🤖 AI Agent is analyzing your documents..."):
            try:
                # Create temporary directories for processing
                with tempfile.TemporaryDirectory() as temp_dir:
                    ref_dir = os.path.join(temp_dir, "reference")
                    new_dir = os.path.join(temp_dir, "new")
                    os.makedirs(ref_dir, exist_ok=True)
                    os.makedirs(new_dir, exist_ok=True)
                    
                    # Save uploaded files to temp directories
                    for i, file in enumerate(st.session_state.uploaded_files['reference']):
                        with open(os.path.join(ref_dir, f"ref_{i}.pdf"), "wb") as f:
                            f.write(file.getvalue())
                    
                    for i, file in enumerate(st.session_state.uploaded_files['new']):
                        with open(os.path.join(new_dir, f"new_{i}.pdf"), "wb") as f:
                            f.write(file.getvalue())
                    
                    # Initialize agent
                    agent = PDFComparisonAgent()
                    
                    # Run comparison
                    results = asyncio.run(
                        agent.run_comparison_workflow(
                            ref_dir, 
                            new_dir, 
                            sensitivity_level=sensitivity_level,
                            testing_mode=testing_mode
                        )
                    )
                    
                    st.session_state.results = results
                    st.success("✅ AI Analysis Complete!")
                    
            except Exception as e:
                st.error(f"❌ Error during comparison: {str(e)}")
                st.info("This is a demo version. For full functionality, deploy with local dependencies.")

# Display results
if st.session_state.results:
    st.markdown("## 📊 AI Analysis Results")
    
    # Extract results
    results = st.session_state.results
    workflow_status = results.get("workflow_status", "unknown")
    execution_time = results.get("execution_time", 0)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">🤖</div>
            <div class="metric-label">AI Agent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">⚡</div>
            <div class="metric-label">Performance</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">📊</div>
            <div class="metric-label">Analysis</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">📋</div>
            <div class="metric-label">Reports</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Workflow status
    if workflow_status == "completed":
        st.markdown("""
        <div class="status-success">
            <h3>✅ Workflow Completed Successfully</h3>
            <p>Execution Time: {:.2f}s | Status: {}</p>
        </div>
        """.format(execution_time, workflow_status), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-warning">
            <h3>⚠️ Workflow Status: {}</h3>
            <p>Execution Time: {:.2f}s</p>
        </div>
        """.format(workflow_status, execution_time), unsafe_allow_html=True)
    
    # Display summary
    if "summary" in results:
        st.markdown("### 📋 Summary")
        st.info(results["summary"])
    
    # Display differences if available
    if "differences" in results:
        st.markdown("### 🔍 Detected Differences")
        differences = results["differences"]
        
        if isinstance(differences, dict):
            for filename, file_diffs in differences.items():
                with st.expander(f"📄 {filename}", expanded=True):
                    if isinstance(file_diffs, list):
                        for diff in file_diffs:
                            st.markdown(f"- {diff}")
                    else:
                        st.json(file_diffs)
        else:
            st.write(differences)
    
    # Display LLM analysis if available
    if "llm_analysis" in results:
        st.markdown("### 🧠 AI Analysis")
        llm_analysis = results["llm_analysis"]
        
        if isinstance(llm_analysis, dict):
            if "summary" in llm_analysis:
                st.markdown("#### 📝 Intelligent Summary")
                st.markdown(llm_analysis["summary"])
            
            if "severity" in llm_analysis:
                st.markdown("#### ⚠️ Severity Assessment")
                st.markdown(llm_analysis["severity"])
            
            if "patterns" in llm_analysis:
                st.markdown("#### 🔍 Pattern Recognition")
                st.markdown(llm_analysis["patterns"])
        else:
            st.markdown(llm_analysis)
    
    # Download options
    st.markdown("## 📥 Download Reports")
    
    if "report" in results:
        report_data = results["report"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            if "html_report" in report_data:
                st.download_button(
                    label="📄 Download HTML Report",
                    data=report_data["html_report"],
                    file_name="neuro_ai_comparison_report.html",
                    mime="text/html",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ HTML report not available")
        
        with col2:
            if "excel_report" in report_data:
                excel_path = report_data["excel_report"]
                if os.path.exists(excel_path):
                    try:
                        with open(excel_path, "rb") as f:
                            excel_data = f.read()
                        if excel_data:
                            st.download_button(
                                "📊 Download Excel Report",
                                data=excel_data,
                                file_name="neuro_ai_comparison_report.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                        else:
                            st.warning("⚠️ Excel report is empty")
                    except Exception as e:
                        st.error(f"🔥 Error reading Excel report: {str(e)}")
                else:
                    st.warning("⚠️ Excel report not available")

# Demo information
st.markdown("---")
st.markdown("## 🎯 Demo Information")
st.info("""
**This is a demonstration version** of the PDF Comparison Agent designed for Streamlit Cloud deployment.

**For full functionality** including:
- Local LLM integration (Ollama/LlamaCPP)
- Advanced AI analysis
- Complete workflow execution

**Deploy locally** using the original `streamlit_app.py` with all dependencies installed.

**Technologies demonstrated:**
- Streamlit web framework
- PDF processing with PyMuPDF
- AI workflow orchestration
- Professional reporting systems
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 2rem;">
    <p>Built with ❤️ by <strong>Rahuul Pande</strong> | Test Automation Engineer & AI Enthusiast</p>
    <p>PDF Comparison Agent - Showcasing AI-Powered Document Analysis</p>
</div>
""", unsafe_allow_html=True)
