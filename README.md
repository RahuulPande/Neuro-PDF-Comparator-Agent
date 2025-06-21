# PDF Comparison Agent

A sophisticated PDF comparison agent built using the Cognizant Neuro AI framework that compares PDF files between reference and new folders, generating visually appealing reports with intelligent analysis.

## 🚀 Features

- **Exact PDF Comparison**: Character-by-character text comparison with binary image matching
- **Neuro AI Integration**: Powered by Cognizant's Neuro AI framework for intelligent orchestration
- **Configurable Sensitivity**: Adjustable comparison settings for different use cases
- **Visual Reports**: Modern HTML reports with interactive elements and export options
- **Local LLM Integration**: Intelligent analysis using Ollama/LlamaCPP
- **Learning Module**: Pattern recognition and optimization based on comparison history
- **Parallel Processing**: Efficient batch processing for large document sets
- **Modern UI**: Beautiful Streamlit interface with dark/light themes

## 🏗️ Architecture

```
pdf-comparison-agent/
├── src/
│   ├── agent/              # Neuro AI agent implementation
│   ├── processors/         # PDF processing modules
│   ├── llm/               # Local LLM integration
│   ├── reports/           # Report generation
│   └── ui/                # Streamlit UI
├── config/                # Configuration files
├── models/                # Learning module storage
└── tests/                 # Unit tests
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   cd /Users/rahuulpande/Documents/pdf-comparison-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up local LLM** (optional):
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull a model
   ollama pull llama2
   ```

## 🚀 Usage

### Quick Start

1. **Run the application**:
   ```bash
   python run.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Select folders**:
   - Reference folder (baseline PDFs)
   - New folder (PDFs to compare)

4. **Configure settings** and start comparison

### Advanced Usage

```python
from src.agent.neuro_agent import PDFComparisonNeuroAgent

# Initialize the agent
agent = PDFComparisonNeuroAgent()

# Run comparison workflow
results = await agent.run_comparison_workflow(
    ref_folder="/path/to/reference",
    new_folder="/path/to/new"
)
```

## ⚙️ Configuration

### Sensitivity Levels

```python
# High sensitivity (default)
sensitivity_config = {
    "text": {
        "strict": True,
        "ignore_whitespace": False,
        "ignore_case": False
    },
    "font": {
        "size_tolerance": 0.5,
        "style_check": True,
        "family_check": True
    },
    "image": {
        "method": "binary",
        "hash_algorithm": "sha256"
    }
}
```

### LLM Configuration

```python
llm_config = {
    "model": "llama2",
    "temperature": 0.7,
    "max_tokens": 500,
    "enable_summarization": True,
    "enable_severity_assessment": True
}
```

## 📊 Report Features

- **Visual Diff Viewer**: Side-by-side comparison with highlighted differences
- **Interactive Elements**: Collapsible sections, tooltips, search functionality
- **Export Options**: HTML, PDF, Excel formats
- **Intelligent Summaries**: LLM-generated change summaries
- **Severity Categorization**: Critical/Major/Minor change classification

## 🧠 Neuro AI Integration

This agent showcases Cognizant's Neuro AI capabilities:

- **Agent Orchestration**: Intelligent task management and workflow automation
- **Parallel Processing**: Efficient batch operations using Neuro AI's task system
- **Learning Module**: Pattern recognition and optimization
- **Workflow Automation**: Automated comparison pipelines

## 🔧 Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
flake8 src/
mypy src/
```

### Project Structure

- **`src/agent/`**: Neuro AI agent implementation
- **`src/processors/`**: PDF parsing and comparison logic
- **`src/llm/`**: Local LLM integration and analysis
- **`src/reports/`**: Report generation and templates
- **`src/ui/`**: Streamlit user interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏢 About Cognizant Neuro AI

This agent is built using Cognizant's Neuro AI framework, showcasing advanced AI capabilities for enterprise document processing and analysis.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation in `/docs/`

---

**Built with ❤️ using Cognizant Neuro AI Framework** 