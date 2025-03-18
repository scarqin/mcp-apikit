import json
import os
from typing import Dict, Any

class ConfigManager:
    """
    Configuration manager for the MCP-APIKit service.
    Handles loading, saving, and accessing configuration settings.
    """
    
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from the config file.
        If the file doesn't exist, return default configuration.
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    "eolink_api_key": "",
                    "eolink_base_url": "https://api.eolink.com",
                    "cache_ttl": 3600,
                    "space_id": "",
                    "project_id": ""
                }
        except Exception as e:
            print(f"Error loading config: {e}")
            return {
                "eolink_api_key": "",
                "eolink_base_url": "https://api.eolink.com",
                "cache_ttl": 3600,
                "space_id": "",
                "project_id": ""
            }
    
    def save_config(self) -> bool:
        """
        Save current configuration to the config file.
        """
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value by key.
        """
        self.config[key] = value
    
    def update(self, config_dict: Dict[str, Any]) -> None:
        """
        Update multiple configuration values at once.
        """
        self.config.update(config_dict)
    
    @property
    def eolink_api_key(self) -> str:
        """
        Get the Eolink API key.
        """
        return self.get("eolink_api_key", "")
    
    @eolink_api_key.setter
    def eolink_api_key(self, value: str) -> None:
        """
        Set the Eolink API key.
        """
        self.set("eolink_api_key", value)
    
    @property
    def eolink_base_url(self) -> str:
        """
        Get the Eolink base URL.
        """
        return self.get("eolink_base_url", "https://api.eolink.com")
    
    @property
    def cache_ttl(self) -> int:
        """
        Get the cache TTL in seconds.
        """
        return self.get("cache_ttl", 3600)
        
    @property
    def space_id(self) -> str:
        """
        Get the Eolink space ID.
        """
        return self.get("space_id", "")
        
    @space_id.setter
    def space_id(self, value: str) -> None:
        """
        Set the Eolink space ID.
        """
        self.set("space_id", value)
        
    @property
    def project_id(self) -> str:
        """
        Get the Eolink project ID.
        """
        return self.get("project_id", "")
        
    @project_id.setter
    def project_id(self, value: str) -> None:
        """
        Set the Eolink project ID.
        """
        self.set("project_id", value)
