"""
Configuration management for AI Fitness Disruption Lab.
Handles environment variables and global settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Global configuration class."""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Project paths
    BASE_DIR = Path(__file__).parent.parent
    DATASETS_DIR = BASE_DIR / "datasets"
    EXPERIMENTS_DIR = BASE_DIR / "experiments"
    
    # Gemini settings
    GEMINI_MODEL = "gemini-2.0-flash-exp"
    GEMINI_TEMPERATURE = 0.7
    GEMINI_MAX_TOKENS = 2048
    
    # Safety settings
    MAX_WORKOUT_DURATION = 120  # minutes
    MIN_WORKOUT_DURATION = 5    # minutes
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in your .env file. "
                "Get your key at https://aistudio.google.com/apikey"
            )
        return True

# Create config instance
config = Config()
