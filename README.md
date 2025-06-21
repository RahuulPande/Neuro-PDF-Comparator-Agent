# Cognizant Neuro AI - PDF Comparison Agent

This is an advanced PDF comparison agent that leverages local Large Language Models (LLMs) and a sophisticated workflow to intelligently compare PDF documents, analyze differences, and generate insightful reports. It is designed to be a powerful tool for regression testing, system integration testing (SIT), and any scenario where detailed, context-aware document comparison is required.

![Agent UI](https://github.com/RahuulPande/Neuro-PDF-Comparator-Agent/blob/main/screenshot.png?raw=true)

## ✨ Key Capabilities

- **Intelligent PDF Parsing:** Goes beyond simple text extraction to analyze text content, fonts, and images on a per-page basis.
- **Multi-faceted Comparison:** Compares documents across three dimensions:
    1.  **Text Content:** Line-by-line comparison with page-aware difference reporting.
    2.  **Images:** Detects added, removed, or altered images.
    3.  **Fonts:** Identifies changes in font styles and families.
- **LLM-Powered Analysis:** Integrates with local LLMs (via Ollama) to provide context-aware analysis of the detected differences. The AI adopts different personas based on the testing mode.
- **Context-Aware Testing Modes:**
    -   **Regression Testing:** A strict "compliance officer" persona where any change is flagged as a critical failure. Ideal for ensuring documents remain unchanged.
    -   **SIT Testing:** A "business analyst" persona that validates expected changes and highlights unintended modifications.
- **Futuristic UI:** A modern, professional user interface built with Streamlit, featuring a dark theme, status indicators, and clear result presentation.
- **Comprehensive Reporting:** Generates detailed comparison reports in multiple formats:
    -   **In-App Display:** Immediate, readable analysis within the UI.
    -   **HTML Report:** A portable, detailed report of all differences.
    -   **Excel Report:** A structured `.xlsx` file detailing every change.

## 🛠️ Getting Started

Follow these steps to set up and run the Neuro PDF Comparison Agent on your local machine.

### Prerequisites

1.  **Python 3.9+:** Ensure you have Python installed. You can check with `python3 --version`.
2.  **Homebrew (macOS):** This is required to install necessary system-level dependencies for PDF report generation. You can install it from [brew.sh](https://brew.sh/).
3.  **Ollama & Llama3:** The agent requires a locally running Ollama instance with a downloaded model.
    -   Install Ollama from [ollama.com](https://ollama.com).
    -   Once installed, run the following command in your terminal to download the `llama3` model:
        ```bash
        ollama pull llama3
        ```

### Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/RahuulPande/Neuro-PDF-Comparator-Agent.git
    cd Neuro-PDF-Comparator-Agent
    ```

2.  **Install System Dependencies (macOS):**
    This step is crucial for the underlying libraries used for PDF processing.
    ```bash
    brew install pango cairo gdk-pixbuf libffi
    ```

3.  **Install Python Packages:**
    A `requirements.txt` file is provided with all necessary Python packages.
    ```bash
    pip3 install -r requirements.txt
    ```

### Running the Agent

A convenience script `run.sh` is provided to handle environment setup and launch the application.

1.  **Make the script executable (only needed once):**
    ```bash
    chmod +x run.sh
    ```

2.  **Launch the agent:**
    ```bash
    ./run.sh
    ```

This will start the Streamlit server. You can access the UI by navigating to the "Local URL" provided in the terminal (usually `http://localhost:8501`).

## usage

1.  **Place your PDFs:**
    -   Put the original or reference versions of your documents in the `test_data/reference` directory.
    -   Put the new or updated versions in the `test_data/new` directory.
    -   Ensure filenames match between the two folders (e.g., `document1.pdf` in both).
2.  **Configure Analysis:**
    -   Use the **Configuration Panel** in the UI to select your **Testing Mode** (`regression` or `sit`) and **Sensitivity Level**.
3.  **Run Comparison:**
    -   Click the **"🚀 Launch Neuro AI Analysis"** button to start the comparison workflow.
4.  **Review Results:**
    -   The results, including the detailed AI analysis, will be displayed directly in the UI.
    -   Use the download buttons to get your comparison reports in HTML or Excel format.

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