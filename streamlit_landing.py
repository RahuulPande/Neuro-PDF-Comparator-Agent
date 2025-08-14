import streamlit as st
import base64

# Page configuration
st.set_page_config(
    page_title="PDF Comparison Agent - AI-Powered Document Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #ffd700, #ffed4e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    .main-header p {
        font-size: 1.5rem;
        color: #e0e0e0;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #b0b0b0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffd700;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #d0d0d0;
        line-height: 1.6;
    }
    
    .developer-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
    }
    
    .developer-avatar {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .developer-name {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .developer-title {
        font-size: 1.2rem;
        color: #ffd700;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    .developer-desc {
        color: #d0d0d0;
        margin-bottom: 1.5rem;
        line-height: 1.8;
    }
    
    .contact-btn {
        display: inline-block;
        padding: 0.8rem 1.5rem;
        margin: 0.5rem;
        border-radius: 25px;
        text-decoration: none;
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .linkedin { background: linear-gradient(45deg, #0077b5, #00a0dc); }
    .email { background: linear-gradient(45deg, #ea4335, #fbbc05); }
    .github { background: linear-gradient(45deg, #333, #666); }
    
    .cta-section {
        text-align: center;
        padding: 3rem 0;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        margin: 2rem 0;
    }
    
    .cta-title {
        font-size: 2.5rem;
        color: #ffd700;
        margin-bottom: 1rem;
    }
    
    .cta-text {
        font-size: 1.2rem;
        color: #d0d0d0;
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .cta-button {
        display: inline-block;
        padding: 1rem 2rem;
        background: linear-gradient(45deg, #ffd700, #ffed4e);
        color: #333;
        text-decoration: none;
        border-radius: 30px;
        font-size: 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #b0b0b0;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 2rem;
    }
    
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Text colors */
    .stMarkdown {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="main-header">
    <h1>PDF Comparison Agent</h1>
    <p>AI-Powered Document Analysis & Regression Testing</p>
    <p class="subtitle">Built with Cognizant Neuro AI Framework and Local LLM Integration</p>
</div>
""", unsafe_allow_html=True)

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="feature-card">
        <h2 style="color: #ffd700; margin-bottom: 1rem;">🚀 Project Overview</h2>
        <p style="font-size: 1.1rem; color: #e0e0e0; line-height: 1.6;">
            A sophisticated PDF comparison tool that leverages artificial intelligence to detect changes, 
            assess compliance risks, and generate intelligent reports for financial document validation.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #ffd700; margin-bottom: 1rem;">✨ Key Features</h3>
    """, unsafe_allow_html=True)
    
    # Features
    features = [
        ("🤖", "Neuro AI Integration", "Built on Cognizant's Neuro AI framework with intelligent workflow orchestration"),
        ("🧠", "Local LLM Analysis", "Ollama/LlamaCPP integration for intelligent summaries and pattern recognition"),
        ("📊", "Context-Aware Testing", "Regression testing (expecting identical files) vs SIT testing (expecting changes)"),
        ("🔍", "Advanced Comparison", "Text, font, image, and layout analysis with page-level change detection"),
        ("📋", "Professional Reports", "HTML and Excel reports with business context and compliance insights"),
        ("⚡", "High Performance", "Handles large PDF files (35-50+ pages) efficiently")
    ]
    
    for icon, title, desc in features:
        st.markdown(f"""
        <div style="margin-bottom: 1rem; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 15px;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>
            <div style="font-weight: 600; color: #ffd700; margin-bottom: 0.5rem;">{title}</div>
            <div style="color: #d0d0d0; font-size: 0.9rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="developer-card">
        <div class="developer-avatar">👨‍💻</div>
        <div class="developer-name">Rahuul Pande</div>
        <div class="developer-title">Test Automation Engineer & AI Enthusiast</div>
        <div class="developer-desc">
            Passionate about leveraging AI tools to solve complex testing challenges. 
            Specialized in automation frameworks and intelligent testing solutions.
        </div>
        
        <div style="margin-top: 1rem;">
            <a href="https://www.linkedin.com/in/rahuulpande/" target="_blank" class="contact-btn linkedin">💼 LinkedIn</a>
            <a href="mailto:rahuulpande@gmail.com" class="contact-btn email">📧 Email</a>
            <a href="https://github.com/rahuulpande/" target="_blank" class="contact-btn github">🐙 GitHub</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Call to Action Section
st.markdown("""
<div class="cta-section">
    <h2 class="cta-title">Ready to Experience AI-Powered PDF Analysis?</h2>
    <p class="cta-text">
        This project demonstrates advanced AI integration, intelligent workflow design, and practical 
        application of machine learning in document validation workflows.
    </p>
    <a href="https://share.streamlit.io/user/rahuulpande" class="cta-button">🚀 View Live Demo</a>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>&copy; 2024 PDF Comparison Agent. Built with ❤️ using Streamlit, Python, and AI technologies.</p>
    <p style="margin-top: 10px; font-size: 0.9rem;">
        Technologies: Python, Streamlit, PyMuPDF, Ollama, OpenCV, OpenPyXL, WeasyPrint
    </p>
</div>
""", unsafe_allow_html=True)

# Add some interactivity
st.sidebar.markdown("## 🎯 Quick Links")
st.sidebar.markdown("""
- [LinkedIn Profile](https://www.linkedin.com/in/rahuulpande/)
- [GitHub Portfolio](https://github.com/rahuulpande/)
- [Email Contact](mailto:rahuulpande@gmail.com)
""")

st.sidebar.markdown("## 🚀 Deploy Your Own")
st.sidebar.markdown("""
This landing page is built with Streamlit and can be easily deployed to Streamlit Cloud for free!
""")
