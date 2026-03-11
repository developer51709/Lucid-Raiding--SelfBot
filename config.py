"""
Configuration manager for Lucid Raiding SelfBot.
Loads settings from environment variables and config.json.
"""

import json
import os
from pathlib import Path
from utils.color import gradient_log

class Config:
    """Configuration container for the bot."""
    
    # Defaults
    DEFAULT_PREFIX = "!"
    DEFAULT_STATUS = "Lucid Raiding v1.0"
    DEFAULT_ACTIVITY_TYPE = "playing"  # playing, listening, watching, competing
    
    def __init__(self):
        self.prefix = os.environ.get("PREFIX", self.DEFAULT_PREFIX)
        self.discord_token = os.environ.get("DISCORD_TOKEN")
        self.status = os.environ.get("BOT_STATUS", self.DEFAULT_STATUS)
        self.activity_type = os.environ.get("ACTIVITY_TYPE", self.DEFAULT_ACTIVITY_TYPE).lower()
        
        # Load from config.json if it exists
        self._load_from_file()
    
    def _load_from_file(self):
        """Load settings from config.json if it exists."""
        config_path = Path(__file__).parent / "config.json"
        
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    data = json.load(f)
                
                self.prefix = data.get("prefix", self.prefix)
                self.status = data.get("status", self.status)
                self.activity_type = data.get("activity_type", self.activity_type)
                
                gradient_log(
                    (0, 255, 255),
                    (0, 255, 255),
                    "[CONFIG] Loaded settings from config.json"
                )
            except Exception as e:
                gradient_log(
                    (255, 165, 0),
                    (255, 165, 0),
                    f"[WARNING] Failed to load config.json: {e}"
                )
    
    def save_to_file(self):
        """Save current configuration to config.json."""
        config_path = Path(__file__).parent / "config.json"
        
        data = {
            "prefix": self.prefix,
            "status": self.status,
            "activity_type": self.activity_type,
        }
        
        try:
            with open(config_path, "w") as f:
                json.dump(data, f, indent=2)
            gradient_log(
                (0, 255, 0),
                (0, 255, 0),
                "[CONFIG] Saved configuration to config.json"
            )
        except Exception as e:
            gradient_log(
                (255, 0, 0),
                (255, 0, 0),
                f"[ERROR] Failed to save config.json: {e}"
            )
    
    def validate(self):
        """Validate required configuration."""
        if not self.discord_token:
            gradient_log(
                (255, 0, 0),
                (255, 0, 0),
                "[ERROR] DISCORD_TOKEN environment variable not set"
            )
            return False
        
        if self.activity_type not in ["playing", "listening", "watching", "competing"]:
            gradient_log(
                (255, 165, 0),
                (255, 165, 0),
                f"[WARNING] Unknown activity type '{self.activity_type}', defaulting to 'playing'"
            )
            self.activity_type = "playing"
        
        return True
    
    def __repr__(self):
        return f"<Config prefix='{self.prefix}' status='{self.status}' activity='{self.activity_type}'>"

# Global config instance
config = Config()
