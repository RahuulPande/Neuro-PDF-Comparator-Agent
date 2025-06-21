#!/bin/bash
# This script sets the necessary library path for WeasyPrint on macOS with Homebrew
# and then launches the PDF Comparison Agent.

export DYLD_LIBRARY_PATH=/opt/homebrew/lib
python3 -m streamlit run src/ui/streamlit_app.py --server.runOnSave true 