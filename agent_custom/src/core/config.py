"""Configuration management using Pydantic Settings."""

import os
from pathlib import Path
from typing import Dict, List, Optional
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


class ServerConfig(BaseSettings):
    """Server configuration."""
    
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True


class LLMProviderConfig(BaseSettings):
    """LLM provider configuration."""
    
    models: List[str] = Field(default_factory=list)
    default_model: str = ""


class LLMConfig(BaseSettings):
    """LLM configuration."""
    
    default_provider: str = "gemini"
    temperature: float = 0.0
    max_tokens: int = 4096
    providers: Dict[str, dict] = Field(default_factory=dict)


class HotspotConfig(BaseSettings):
    """Hotspot finder configuration."""
    
    keywords: List[str] = Field(default_factory=lambda: ["AI", "technology"])
    lookback_days: int = 7
    top_k: int = 10
    score_weights: Dict[str, float] = Field(
        default_factory=lambda: {
            "views": 0.1,
            "likes": 1.0,
            "comments": 0.8,
            "danmaku": 0.5,
            "gravity": 1.8,
            "duration_weight": 0.25,
        }
    )


class TaskConfig(BaseSettings):
    """Task management configuration."""
    
    max_concurrent: int = 5
    max_retries: int = 2
    retry_delay: int = 3
    cleanup_interval: int = 3600
    history_size: int = 100


class Settings(BaseSettings):
    """Main application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )
    
    # API Keys
    deepseek_api_key: Optional[str] = None
    gemini_api_keys: Optional[str] = None
    veo_api_key: Optional[str] = None
    bili_cookie: Optional[str] = None
    
    # Server
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    debug: bool = True
    
    # Proxy
    http_proxy: Optional[str] = None
    https_proxy: Optional[str] = None
    
    # Paths
    data_dir: Path = Path("./data")
    prompts_dir: Path = Path("./data/prompts")
    videos_dir: Path = Path("./data/videos")
    logs_dir: Path = Path("./logs")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_yaml_config()
        self._ensure_directories()
    
    def _load_yaml_config(self):
        """Load configuration from YAML file."""
        config_path = Path("config/settings.yaml")
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)
                
                # Load nested configs
                if "server" in config_data:
                    self.api_host = config_data["server"].get("host", self.api_host)
                    self.api_port = config_data["server"].get("port", self.api_port)
                    self.debug = config_data["server"].get("reload", self.debug)
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        for path in [self.data_dir, self.prompts_dir, self.videos_dir, self.logs_dir]:
            path.mkdir(parents=True, exist_ok=True)
    
    def get_gemini_keys(self) -> List[str]:
        """Get list of Gemini API keys."""
        if not self.gemini_api_keys:
            return []
        return [key.strip() for key in self.gemini_api_keys.split(",") if key.strip()]
    
    def get_proxy_dict(self) -> Dict[str, Optional[str]]:
        """Get proxy configuration as dictionary."""
        return {
            "http": self.http_proxy,
            "https": self.https_proxy,
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

