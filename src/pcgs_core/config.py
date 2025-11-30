"""
PCGS Configuration

Handles environment variables and application settings.
"""

import os
from dataclasses import dataclass

@dataclass
class Config:
    """
    Application configuration container.
    """
    ENV: str = "development"
    APP_NAME: str = "PCGS v2"
    # Storage settings
    STORAGE_TYPE: str = "local" # 'local', 'sqlite', 'postgres'
    DATA_DIR: str = "data"
    
    # API Keys (placeholders)
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

def load_config() -> Config:
    """
    Load configuration from environment variables.
    """
    return Config(
        ENV=os.getenv("PCGS_ENV", "development"),
        STORAGE_TYPE=os.getenv("PCGS_STORAGE_TYPE", "local"),
        DATA_DIR=os.getenv("PCGS_DATA_DIR", "data"),
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY", ""),
        ANTHROPIC_API_KEY=os.getenv("ANTHROPIC_API_KEY", "")
    )







