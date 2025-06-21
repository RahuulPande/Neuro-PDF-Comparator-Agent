"""
Configuration settings for the PDF Comparison Agent.
"""

from typing import Dict, Any
import os

# Base configuration
BASE_CONFIG = {
    "app_name": "PDF Comparison Agent",
    "version": "1.0.0",
    "author": "Cognizant AI Lab",
    "description": "Sophisticated PDF comparison using Neuro AI framework"
}

# Comparison settings
COMPARISON_SETTINGS = {
    "parallel_workers": 4,
    "chunk_size": 10,  # PDFs per batch
    "max_file_size_mb": 50,
    "supported_formats": [".pdf"],
    "timeout_seconds": 300,  # 5 minutes per PDF
}

# Sensitivity levels configuration
SENSITIVITY_LEVELS = {
    "high": {
        "text": {
            "strict": True,
            "ignore_whitespace": False,
            "ignore_case": False,
            "ignore_punctuation": False,
            "character_level": True
        },
        "font": {
            "size_tolerance": 0.1,  # Flag differences > 0.1pt
            "style_check": True,
            "family_check": True,
            "color_check": True,
            "weight_check": True
        },
        "image": {
            "method": "binary",
            "hash_algorithm": "sha256",
            "pixel_perfect": True,
            "compression_check": True
        },
        "layout": {
            "position_tolerance": 1,  # pixels
            "size_tolerance": 1,      # pixels
            "margin_check": True,
            "spacing_check": True
        }
    },
    "medium": {
        "text": {
            "strict": True,
            "ignore_whitespace": True,
            "ignore_case": False,
            "ignore_punctuation": False,
            "character_level": False
        },
        "font": {
            "size_tolerance": 0.5,  # Flag differences > 0.5pt
            "style_check": True,
            "family_check": True,
            "color_check": False,
            "weight_check": False
        },
        "image": {
            "method": "binary",
            "hash_algorithm": "md5",
            "pixel_perfect": False,
            "compression_check": False
        },
        "layout": {
            "position_tolerance": 5,  # pixels
            "size_tolerance": 5,      # pixels
            "margin_check": False,
            "spacing_check": False
        }
    },
    "low": {
        "text": {
            "strict": False,
            "ignore_whitespace": True,
            "ignore_case": True,
            "ignore_punctuation": True,
            "character_level": False
        },
        "font": {
            "size_tolerance": 1.0,  # Flag differences > 1.0pt
            "style_check": False,
            "family_check": False,
            "color_check": False,
            "weight_check": False
        },
        "image": {
            "method": "binary",
            "hash_algorithm": "md5",
            "pixel_perfect": False,
            "compression_check": False
        },
        "layout": {
            "position_tolerance": 10,  # pixels
            "size_tolerance": 10,      # pixels
            "margin_check": False,
            "spacing_check": False
        }
    }
}

# LLM Configuration
LLM_CONFIG = {
    "model": "llama2",
    "temperature": 0.7,
    "max_tokens": 500,
    "enable_summarization": True,
    "enable_severity_assessment": True,
    "enable_natural_queries": True,
    "prompts": {
        "summarization": "Analyze these PDF differences and provide a business-friendly summary highlighting the most important changes.",
        "severity_assessment": "Categorize these changes by importance (Critical/Major/Minor) and explain why: {differences}",
        "pattern_recognition": "Identify any patterns or trends in these document changes that might indicate systematic issues.",
        "query_response": "Answer this question about the PDF differences: {query}\n\nDifferences: {differences}"
    }
}

# Report Configuration
REPORT_CONFIG = {
    "include_previews": True,
    "max_preview_size": "500x500",
    "highlight_differences": True,
    "export_formats": ["html", "pdf", "excel"],
    "template_theme": "modern",
    "include_statistics": True,
    "include_charts": True,
    "max_differences_per_page": 100,
    "css_styles": {
        "primary_color": "#1f77b4",
        "secondary_color": "#ff7f0e",
        "success_color": "#2ca02c",
        "warning_color": "#d62728",
        "background_color": "#f8f9fa",
        "text_color": "#212529"
    }
}

# UI Configuration
UI_CONFIG = {
    "theme": "light",  # light, dark, auto
    "page_title": "PDF Comparison Agent",
    "page_icon": "📄",
    "layout": "wide",
    "sidebar_state": "expanded",
    "enable_animations": True,
    "progress_bar_style": "modern",
    "file_uploader_type": "folder",
    "max_upload_size": 200,  # MB
}

# Neuro AI Configuration
NEURO_AI_CONFIG = {
    "agent_name": "PDF_Comparison_Agent",
    "workflow_name": "PDF_Comparison_Workflow",
    "enable_learning": True,
    "learning_storage_path": "models/learning_data.json",
    "task_timeout": 600,  # 10 minutes
    "max_concurrent_tasks": 4,
    "retry_attempts": 3,
    "log_level": "INFO"
}

# Storage Configuration
STORAGE_CONFIG = {
    "base_path": os.path.join(os.path.dirname(__file__), ".."),
    "models_path": "models",
    "reports_path": "reports",
    "temp_path": "temp",
    "logs_path": "logs",
    "cache_path": "cache",
    "max_cache_size": 1000,  # MB
    "cache_ttl": 3600,  # 1 hour
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_handler": True,
    "console_handler": True,
    "max_file_size": 10,  # MB
    "backup_count": 5
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    "memory_limit_mb": 2048,
    "cpu_limit_percent": 80,
    "enable_profiling": False,
    "profile_output": "performance_profile.json",
    "optimization_level": "balanced",  # minimal, balanced, aggressive
}

# Security Configuration
SECURITY_CONFIG = {
    "enable_file_validation": True,
    "allowed_file_types": [".pdf"],
    "max_file_count": 1000,
    "sanitize_filenames": True,
    "enable_encryption": False,
    "session_timeout": 3600,  # 1 hour
}

def get_config() -> Dict[str, Any]:
    """Get the complete configuration dictionary."""
    return {
        "base": BASE_CONFIG,
        "comparison": COMPARISON_SETTINGS,
        "sensitivity": SENSITIVITY_LEVELS,
        "llm": LLM_CONFIG,
        "report": REPORT_CONFIG,
        "ui": UI_CONFIG,
        "neuro_ai": NEURO_AI_CONFIG,
        "storage": STORAGE_CONFIG,
        "logging": LOGGING_CONFIG,
        "performance": PERFORMANCE_CONFIG,
        "security": SECURITY_CONFIG
    }

def get_sensitivity_config(level: str = "medium") -> Dict[str, Any]:
    """Get sensitivity configuration for a specific level."""
    return SENSITIVITY_LEVELS.get(level, SENSITIVITY_LEVELS["medium"])

def update_config(section: str, key: str, value: Any) -> None:
    """Update a specific configuration value."""
    if section in globals():
        config_dict = globals()[section]
        if key in config_dict:
            config_dict[key] = value
        else:
            raise KeyError(f"Key '{key}' not found in section '{section}'")
    else:
        raise KeyError(f"Section '{section}' not found in configuration") 