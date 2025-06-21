# Technical Documentation: Neuro PDF Comparison Agent

This document provides a deep dive into the technical architecture, design philosophy, and workflow of the Cognizant Neuro AI PDF Comparison Agent.

## 1. Core Philosophy: The "Neuro AI" Framework

The "Cognizant Neuro AI" concept is not a specific library but an architectural philosophy applied to this project. It treats the application as a cognitive agent that mimics a human expert's workflow. This is achieved through a modular, pipeline-based system where discrete "tasks" are executed in a logical sequence, managed by a central "agent."

The key principles are:
-   **Modularity:** Each component (parsing, comparing, reporting) is a self-contained module with a specific responsibility.
-   **Workflow Orchestration:** A central `PDFComparisonNeuroAgent` orchestrates the entire process, passing context and data between modules, much like a project manager.
-   **Learning & Adaptation:** The system includes a (currently simple) `learning_module` to store results, laying the groundwork for future adaptation based on past results.
-   **Cognitive Analysis:** The final step is not just reporting differences but *analyzing* them using an LLM, which acts as the agent's "brain" to interpret results and provide executive summaries.

## 2. System Architecture & Workflow

The agent operates on a sequential workflow, defined and executed by the `PDFComparisonNeuroAgent` in `src/agent/neuro_agent.py`. Each step is a task performed by a specialized processor.

The workflow is as follows:

1.  **Scan (`scan_folders`):** The agent first scans the `test_data/reference` and `test_data/new` directories to identify pairs of documents with matching filenames.
2.  **Validate (`validate_files`):** Each identified PDF is checked to ensure it's a valid, non-corrupt file.
3.  **Parse (`parse_pdfs`):**
    -   The `PDFParser` (`src/processors/pdf_parser.py`) is used to extract content.
    -   It doesn't just grab text; it extracts it **per page**, which is critical for providing page-aware difference locations.
    -   It also extracts information about fonts and embedded images.
4.  **Compare (`compare_content`):**
    -   The `TextComparator` (`src/processors/text_comparator.py`) performs a line-by-line comparison of the text extracted from each pair of documents. It generates human-readable descriptions of changes, such as, "On page 1, line 5, the text '...' was changed to '...'".
    -   Image and Font comparators perform similar analyses for their respective domains.
5.  **Analyze (`analyze_with_llm`):**
    -   This is the core of the "Neuro AI" intelligence.
    -   The `LocalLLMAnalyzer` (`src/llm/local_llm.py`) takes the structured difference data from the comparison step.
    -   It constructs a detailed prompt based on the selected **Testing Mode** (`regression` or `sit`).
    -   It sends this prompt to a local Ollama server running the `llama3` model.
    -   The prompt instructs the LLM to act as a specific persona (Compliance Officer or Business Analyst) and to format its response using Markdown for professional presentation.
6.  **Report (`generate_report`):**
    -   The agent takes the comparison data and the LLM's formatted analysis.
    -   The `HtmlGenerator` (`src/reports/html_generator.py`) creates a detailed HTML report.
    -   An Excel report is also generated, providing a structured list of all differences.
7.  **Learn (`update_learning`):** The results of the comparison are saved to `models/learning_data.json`. This module can be expanded in the future for more advanced pattern recognition.

## 3. LLM Integration Details

The integration with the Large Language Model is central to the agent's analytical capabilities.

-   **Service:** It uses a locally-hosted Ollama service. This ensures data privacy and removes reliance on external cloud providers.
-   **Model:** It is configured to use the `llama3:latest` model, which provides a strong balance of reasoning and instruction-following capabilities.
-   **Prompt Engineering:** The magic happens in the prompt. Instead of just asking "what are the differences?", the prompts are engineered to be highly specific:
    -   **Persona Adoption:** The LLM is explicitly told to adopt a professional persona relevant to the task.
    -   **Context Injection:** Rich context about the testing mode (e.g., "any change is a failure" for regression) is injected directly into the prompt.
    -   **Format Enforcement:** The prompt demands that the output be structured using Markdown, with specific headings and bullet points. This moves formatting responsibility to the LLM, resulting in clean, readable outputs.
-   **Fallback:** The `LocalLLMAnalyzer` includes error handling. If it cannot connect to the Ollama server, it will fall back to a basic summary and log a warning, preventing the entire application from crashing.

## 4. Codebase Structure

The project is organized into the following key directories:

-   `run.sh`: The main entry point script for end-users. It sets up necessary environment variables (especially for macOS) and launches the Streamlit app.
-   `src/`: Contains all the core source code.
    -   `agent/`: The central agent and workflow logic.
    -   `llm/`: The local LLM integration and prompt engineering.
    -   `processors/`: Modules responsible for specific tasks like parsing and comparing text, images, and fonts.
    -   `reports/`: Generators for HTML and Excel reports.
    -   `ui/`: The Streamlit application code, including all custom CSS for the futuristic theme.
-   `config/`: Configuration files, including YAML files for settings.
-   `test_data/`: Default location for reference and new PDF files for comparison.
-   `models/`: Stores data related to the agent's learning capabilities. 