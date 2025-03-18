from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..utils.config_manager import ConfigManager
from ..utils.eolink_client import EolinkClient
from .models import (
    ApiBasicInfo, 
    ApiDetailedInfo, 
    ConfigUpdateRequest, 
    ApiListResponse, 
    ApiDetailResponse, 
    ErrorResponse
)

# Create router
router = APIRouter()

# Dependency to get config manager
def get_config_manager():
    return ConfigManager()

# Dependency to get Eolink client
def get_eolink_client(config_manager: ConfigManager = Depends(get_config_manager)):
    return EolinkClient(config_manager)

@router.get("/api/list", response_model=ApiListResponse, responses={400: {"model": ErrorResponse}})
async def get_api_list(eolink_client: EolinkClient = Depends(get_eolink_client)):
    """
    Get a list of all available APIs from Eolink.
    """
    if not eolink_client.config_manager.eolink_api_key:
        raise HTTPException(status_code=400, detail="Eolink API key not configured")
    
    if not eolink_client.config_manager.space_id or not eolink_client.config_manager.project_id:
        raise HTTPException(status_code=400, detail="Eolink space_id and project_id must be configured")
    
    apis_data = eolink_client.get_all_apis(
        space_id=eolink_client.config_manager.space_id,
        project_id=eolink_client.config_manager.project_id
    )
    
    # Transform Eolink API data to our model format
    api_list = []
    for api_data in apis_data:
        api_info = ApiBasicInfo(
            id=api_data.get("id", ""),
            name=api_data.get("name", ""),
            method=api_data.get("method", "").upper(),
            path=api_data.get("path", ""),
            description=api_data.get("description", ""),
            group=api_data.get("group", "")
        )
        api_list.append(api_info)
    
    return ApiListResponse(apis=api_list)

@router.get("/api/detail/{api_id}", response_model=ApiDetailResponse, responses={404: {"model": ErrorResponse}})
async def get_api_detail(api_id: str, eolink_client: EolinkClient = Depends(get_eolink_client)):
    """
    Get detailed information about a specific API.
    """
    if not eolink_client.config_manager.eolink_api_key:
        raise HTTPException(status_code=400, detail="Eolink API key not configured")
    
    api_detail = eolink_client.get_api_detail(api_id)
    
    if not api_detail:
        raise HTTPException(status_code=404, detail=f"API with ID {api_id} not found")
    
    # Transform Eolink API detail to our model format
    # This is a simplified transformation - adjust according to actual Eolink API response format
    parameters = []
    for param in api_detail.get("parameters", []):
        parameters.append({
            "name": param.get("name", ""),
            "type": param.get("type", "string"),
            "required": param.get("required", False),
            "description": param.get("description", ""),
            "default_value": param.get("default", None)
        })
    
    responses = []
    for status_code, response_data in api_detail.get("responses", {}).items():
        responses.append({
            "status_code": int(status_code),
            "description": response_data.get("description", ""),
            "schema": response_data.get("schema", {})
        })
    
    detailed_info = ApiDetailedInfo(
        id=api_detail.get("id", ""),
        name=api_detail.get("name", ""),
        method=api_detail.get("method", "").upper(),
        path=api_detail.get("path", ""),
        description=api_detail.get("description", ""),
        group=api_detail.get("group", ""),
        parameters=parameters,
        request_body=api_detail.get("requestBody", {}),
        responses=responses,
        tags=api_detail.get("tags", []),
        deprecated=api_detail.get("deprecated", False)
    )
    
    return ApiDetailResponse(api=detailed_info)

@router.post("/config", responses={200: {"description": "Configuration updated successfully"}})
async def update_config(config_request: ConfigUpdateRequest, config_manager: ConfigManager = Depends(get_config_manager)):
    """
    Update the configuration settings.
    """
    update_dict = {}
    
    if config_request.eolink_api_key is not None:
        update_dict["eolink_api_key"] = config_request.eolink_api_key
    
    if config_request.eolink_base_url is not None:
        update_dict["eolink_base_url"] = config_request.eolink_base_url
    
    if config_request.cache_ttl is not None:
        update_dict["cache_ttl"] = config_request.cache_ttl
        
    if config_request.space_id is not None:
        update_dict["space_id"] = config_request.space_id
        
    if config_request.project_id is not None:
        update_dict["project_id"] = config_request.project_id
    
    config_manager.update(update_dict)
    config_manager.save_config()
    
    return {"message": "Configuration updated successfully"}

@router.get("/config")
async def get_config(config_manager: ConfigManager = Depends(get_config_manager)):
    """
    Get the current configuration settings.
    """
    return {
        "eolink_api_key": "*****" if config_manager.eolink_api_key else "",
        "eolink_base_url": config_manager.eolink_base_url,
        "cache_ttl": config_manager.cache_ttl,
        "space_id": config_manager.space_id,
        "project_id": config_manager.project_id
    }

@router.post("/clear-cache")
async def clear_cache(eolink_client: EolinkClient = Depends(get_eolink_client)):
    """
    Clear the API cache.
    """
    eolink_client.clear_cache()
    return {"message": "Cache cleared successfully"}

@router.get("/test-connection")
async def test_connection(eolink_client: EolinkClient = Depends(get_eolink_client)):
    """
    Test the connection to Eolink API.
    """
    if not eolink_client.config_manager.eolink_api_key:
        return {"status": "error", "message": "Eolink API key not configured"}
    
    connection_successful = eolink_client.test_connection()
    
    if connection_successful:
        return {"status": "success", "message": "Connection to Eolink API successful"}
    else:
        return {"status": "error", "message": "Failed to connect to Eolink API"}
