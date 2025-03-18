import requests
import time
from typing import Dict, List, Any, Optional
from .config_manager import ConfigManager

class EolinkClient:
    """
    Client for interacting with Eolink OpenAPI.
    Handles API requests and response parsing.
    """
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.cache = {}
        self.cache_timestamps = {}
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get the headers for Eolink API requests.
        """
        return {
            "Content-Type": "application/json",
            "Eo-Secret-Key": self.config_manager.eolink_api_key
        }
    
    def _make_request(self, endpoint: str, method: str = "GET", params: Dict[str, Any] = None, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a request to the Eolink API.
        """
        url = f"{self.config_manager.eolink_base_url}{endpoint}"
        headers = self._get_headers()
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to Eolink API: {e}")
            return {"error": str(e)}
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """
        Check if the cache for a given key is still valid.
        """
        if cache_key not in self.cache_timestamps:
            return False
        
        cache_time = self.cache_timestamps[cache_key]
        current_time = time.time()
        return (current_time - cache_time) < self.config_manager.cache_ttl
    
    def get_all_apis(self, space_id: str, project_id: str, page: int = 1, size: int = 20, 
                     keyword: str = None, group_id: int = None, 
                     project_version_id: str = None, branch_id: str = None) -> List[Dict[str, Any]]:
        """
        Get all APIs from Eolink.
        Returns a list of API objects.
        """
        cache_key = f"all_apis_{space_id}_{project_id}_{page}_{size}_{keyword}_{group_id}_{project_version_id}_{branch_id}"
        
        # Check cache first
        if cache_key in self.cache and self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        # Make API request if cache is invalid or missing
        endpoint = "/v3/api-management/apis"
        params = {
            "space_id": space_id,
            "project_id": project_id,
            "page": page,
            "size": size,
        }
        if keyword:
            params["keyword"] = keyword
        if group_id:
            params["group_id"] = group_id
        if project_version_id:
            params["project_version_id"] = project_version_id
        if branch_id:
            params["branch_id"] = branch_id
        
        response = self._make_request(endpoint, params=params)
        
        if "error" in response:
            return []
        
        # Cache the response
        apis = response.get("data", [])
        self.cache[cache_key] = apis
        self.cache_timestamps[cache_key] = time.time()
        
        return apis
    
    def get_api_detail(self, api_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific API.
        """
        cache_key = f"api_detail_{api_id}"
        
        # Check cache first
        if cache_key in self.cache and self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        # Make API request if cache is invalid or missing
        endpoint = f"/openapi/apis/{api_id}"
        response = self._make_request(endpoint)
        
        if "error" in response:
            return None
        
        # Cache the response
        api_detail = response.get("data", {})
        self.cache[cache_key] = api_detail
        self.cache_timestamps[cache_key] = time.time()
        
        return api_detail
    
    def clear_cache(self) -> None:
        """
        Clear the API cache.
        """
        self.cache = {}
        self.cache_timestamps = {}
    
    def test_connection(self) -> bool:
        """
        Test the connection to Eolink API.
        Returns True if connection is successful, False otherwise.
        """
        try:
            endpoint = "/openapi/status"
            response = self._make_request(endpoint)
            return "error" not in response
        except Exception:
            return False
