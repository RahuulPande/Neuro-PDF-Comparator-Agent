"""
Streamlit UI for Cognizant Neuro AI PDF Comparison Agent.
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.agent.neuro_agent import PDFComparisonNeuroAgent
from config.settings import get_config

# Page configuration with futuristic theme
st.set_page_config(
    page_title="Cognizant Neuro AI - PDF Comparison Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for futuristic design
st.markdown("""
<style>
    /* Futuristic Theme */
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ffffff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    .tech-badges {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .tech-badge {
        background: rgba(255,255,255,0.1);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.2);
        font-size: 0.9rem;
        color: #e0e7ff;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    /* Card Styling */
    .stCard {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        background: rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
        color: #ffffff !important;
    }
    
    .stSelectbox > div > div > select {
        background: rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
        color: #ffffff;
    }
    
    /* Status Indicators */
    .status-success {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-warning {
        background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .status-error {
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metrics Display */
    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        color: #cbd5e1;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Animation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(90deg, #5a67d8 0%, #6b46c1 100%);
    }

    /* AI Analysis box styling */
    .ai-analysis-container {
        background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
        padding: 1.5rem; 
        border-radius: 15px; 
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #ffffff;
    }

    .ai-analysis-container h3, .ai-analysis-container p {
        color: #ffffff !important;
    }

    .ai-analysis-header {
        color: #ffffff; 
        margin: 0 0 0.5rem 0; 
        font-weight: 600;
    }

    /* Overriding st.info for better readability in AI Analysis */
    .stAlert {
        background-color: rgba(0, 0, 0, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }

    .stAlert > div:first-child {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# App state
if "agent" not in st.session_state:
    st.session_state.agent = PDFComparisonNeuroAgent()
if "results" not in st.session_state:
    st.session_state.results = None
if "progress" not in st.session_state:
    st.session_state.progress = 0

config = get_config()

# Futuristic Header
st.markdown("""
<div class="header-container">
    <div class="header-title">🤖 Cognizant Neuro AI</div>
    <div class="header-subtitle">Advanced PDF Comparison Agent with LLM Intelligence</div>
    <div class="tech-badges">
        <div class="tech-badge">🧠 Neural Networks</div>
        <div class="tech-badge">🔍 AI-Powered Analysis</div>
        <div class="tech-badge">📊 Intelligent Reporting</div>
        <div class="tech-badge">⚡ Real-time Processing</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration Panel")
    st.markdown("---")
    
    # Testing Mode Selection
    st.markdown("### 🎯 Testing Mode")
    testing_mode = st.selectbox(
        "Select Testing Strategy", 
        ["regression", "sit"], 
        index=0,
        help="Regression: Expect identical files (any change = issue). SIT: Expect some intentional changes."
    )
    
    # Visual mode indicator
    if testing_mode == "regression":
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.2); padding: 1rem; border-radius: 10px; border: 1px solid rgba(239, 68, 68, 0.3);">
            <h4 style="color: #ef4444; margin: 0;">🔍 Regression Testing</h4>
            <p style="color: #fca5a5; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Zero tolerance for changes</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.2); padding: 1rem; border-radius: 10px; border: 1px solid rgba(16, 185, 129, 0.3);">
            <h4 style="color: #10b981; margin: 0;">🧪 SIT Testing</h4>
            <p style="color: #a7f3d0; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Expected changes allowed</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sensitivity Configuration
    st.markdown("### 🎚️ Sensitivity Level")
    sensitivity = st.selectbox(
        "Analysis Sensitivity", 
        ["high", "medium", "low"], 
        index=1,
        help="Higher sensitivity detects more subtle changes"
    )
    
    # Sensitivity indicator
    sensitivity_colors = {"high": "#ef4444", "medium": "#f59e0b", "low": "#10b981"}
    st.markdown(f"""
    <div style="background: rgba({sensitivity_colors[sensitivity]}, 0.2); padding: 0.5rem; border-radius: 8px; border: 1px solid rgba({sensitivity_colors[sensitivity]}, 0.3); text-align: center;">
        <span style="color: {sensitivity_colors[sensitivity]}; font-weight: 600;">{sensitivity.upper()} SENSITIVITY</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Status
    st.markdown("### 📊 System Status")
    st.markdown("""
    <div style="background: rgba(16, 185, 129, 0.2); padding: 1rem; border-radius: 10px; border: 1px solid rgba(16, 185, 129, 0.3);">
        <h4 style="color: #10b981; margin: 0;">🟢 Online</h4>
        <p style="color: #a7f3d0; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Neuro AI Agent Ready</p>
    </div>
    """, unsafe_allow_html=True)

# Main Content Area
st.markdown("## 📁 Document Comparison")

# Folder selection with modern styling
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📂 Reference Documents")
    ref_folder = st.text_input(
        "Reference Folder Path", 
        value="/Users/rahuulpande/Documents/pdf-comparison-agent/test_data/reference",
        help="Path to folder containing reference PDF files"
    )
    
with col2:
    st.markdown("### 📂 New Documents")
    new_folder = st.text_input(
        "New Folder Path", 
        value="/Users/rahuulpande/Documents/pdf-comparison-agent/test_data/new",
        help="Path to folder containing new PDF files for comparison"
    )

# Run comparison with enhanced button
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Launch Neuro AI Analysis", type="primary", use_container_width=True):
        if not os.path.isdir(ref_folder) or not os.path.isdir(new_folder):
            st.error("❌ Please provide valid folder paths.")
        else:
            with st.spinner("🤖 Neuro AI Agent is analyzing your documents..."):
                agent = st.session_state.agent
                import asyncio
                results = asyncio.run(agent.run_comparison_workflow(
                    ref_folder, 
                    new_folder, 
                    sensitivity_level=sensitivity,
                    testing_mode=testing_mode
                ))
                st.session_state.results = results
                st.success("✅ Analysis Complete!")

# Progress indicator
if st.session_state.results is None:
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
        <h3 style="color: #cbd5e1;">Neuro AI Agent Ready</h3>
        <p style="color: #94a3b8;">Configure your settings and launch analysis to begin</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.progress(100, text="✅ Analysis Complete!")

# Results Display
if st.session_state.results:
    st.markdown("## 📊 Analysis Results")
    
    # Results summary with metrics
    meta = st.session_state.results.get("metadata", {})
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{meta.get('workflow_name', 'N/A')}</div>
            <div class="metric-label">Workflow</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{meta.get('sensitivity_level', 'N/A').upper()}</div>
            <div class="metric-label">Sensitivity</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{meta.get('execution_time', 0):.2f}s</div>
            <div class="metric-label">Execution Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        status_icon = "🟢" if meta.get('status') == 'completed' else "🟡"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{status_icon}</div>
            <div class="metric-label">Status</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Testing mode context
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if testing_mode == "regression":
            st.markdown("""
            <div class="status-warning">
                <h4 style="margin: 0;">🔍 Regression Testing Mode</h4>
                <p style="margin: 0.5rem 0 0 0;">Any change detected = FAILURE</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-success">
                <h4 style="margin: 0;">🧪 SIT Testing Mode</h4>
                <p style="margin: 0.5rem 0 0 0;">Some changes are expected</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Show AI analysis
        summary = st.session_state.results.get("analyze", {}).get("intelligent_summary", "")
        st.markdown(f"""
        <div class="ai-analysis-container">
            <h4 class="ai-analysis-header">🧠 AI Analysis</h4>
            <p class="ai-analysis-body">{summary}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Report preview
    st.markdown("## 📋 Detailed Report")
    html_report = st.session_state.results.get("report", {}).get("html_report", "")
    if html_report:
        components.html(html_report, height=600, scrolling=True)
    
    # Download options
    st.markdown("## 💾 Export Reports")
    report_data = st.session_state.results.get("report", {})
    html_report_content = report_data.get("html_report", "")
    excel_report_path = report_data.get("excel_report", "")
    
    col1, col2 = st.columns(2)

    # HTML Download
    with col1:
        if html_report_content:
            st.download_button(
                label="📄 Download HTML Report",
                data=html_report_content,
                file_name="neuro_ai_comparison_report.html",
                mime="text/html",
                use_container_width=True
            )
        else:
            st.warning("⚠️ HTML report not available.", icon="⚠️")

    # Excel Download
    with col2:
        if excel_report_path and os.path.exists(excel_report_path):
            try:
                with open(excel_report_path, "rb") as f:
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
                    st.warning("⚠️ Excel report is empty", icon="⚠️")
            except Exception as e:
                st.error(f"🔥 Error reading Excel report: {str(e)}", icon="🔥")
        else:
            st.warning("⚠️ Excel report not available", icon="⚠️")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #94a3b8;">
    <p>Powered by <strong>Cognizant Neuro AI</strong> | Advanced LLM-Powered Document Analysis</p>
    <p style="font-size: 0.9rem;">Enterprise-grade PDF comparison with intelligent insights</p>
</div>
""", unsafe_allow_html=True) 