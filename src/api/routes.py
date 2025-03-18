from fastapi import APIRouter, HTTPException, Depends, Response
from typing import List, Dict, Any, Optional

from ..utils.config_manager import ConfigManager
from ..utils.eolink_client import EolinkClient
from .models import (
    ApiBasicInfo, 
    ApiDetailedInfo, 
    ConfigUpdateRequest, 
    ApiListResponse, 
    ApiDetailResponse, 
    ErrorResponse,
    Paginator,
    StandardResponse
)

# Create router
router = APIRouter()

# Dependency to get config manager
def get_config_manager():
    return ConfigManager()

# Dependency to get Eolink client
def get_eolink_client(config_manager: ConfigManager = Depends(get_config_manager)):
    return EolinkClient(config_manager)

@router.get("/api/list")
async def get_api_list(
    page: int = 1, 
    size: int = 10,
    eolink_client: EolinkClient = Depends(get_eolink_client)
):
    """
    Get a list of all available APIs from Eolink.
    """
    if not eolink_client.config_manager.eolink_api_key:
        return StandardResponse(
            type="error",
            data={"error": "Eolink API key not configured"},
            status="error"
        )
    
    if not eolink_client.config_manager.space_id or not eolink_client.config_manager.project_id:
        return StandardResponse(
            type="error",
            data={"error": "Eolink space_id and project_id must be configured"},
            status="error"
        )
    
    apis_data = eolink_client.get_all_apis(
        space_id=eolink_client.config_manager.space_id,
        project_id=eolink_client.config_manager.project_id,
        page=page,
        size=size
    )
    
    # Transform Eolink API data to our model format
    api_list = []
    for api_data in apis_data:
        # Check if api_data is a dictionary before using .get() method
        if not isinstance(api_data, dict):
            continue  # Skip this item if it's not a dictionary
            
        api_info = ApiBasicInfo(
            api_id=api_data.get("api_id", ""),
            api_name=api_data.get("api_name", ""),
            api_uri=api_data.get("api_uri", ""),
            api_status=api_data.get("api_status", 0),
            api_request_type=api_data.get("api_request_type", 0),
            create_time=api_data.get("create_time", ""),
            group_id=api_data.get("group_id", 0),
            api_update_time=api_data.get("api_update_time", ""),
            starred=api_data.get("starred", 0),
            order_num=api_data.get("order_num", 0),
            remove_time=api_data.get("remove_time"),
            api_protocol=api_data.get("api_protocol", 0),
            api_type=api_data.get("api_type", "http"),
            api_manager_id=api_data.get("api_manager_id", 0),
            update_user_id=api_data.get("update_user_id", 0),
            create_user_id=api_data.get("create_user_id", 0),
            group_path=api_data.get("group_path", ""),
            group_name=api_data.get("group_name", ""),
            customize_list=api_data.get("customize_list", []),
            version_name=api_data.get("version_name", ""),
            mock_enable=api_data.get("mock_enable", True),
            case_cover=api_data.get("case_cover", False),
            message_encoding=api_data.get("message_encoding", "utf-8"),
            api_tag=api_data.get("api_tag", ""),
            manager=api_data.get("manager", ""),
            creator=api_data.get("creator", ""),
            updater=api_data.get("updater", "")
        )
        api_list.append(api_info)
    
    # Create paginator
    paginator = Paginator(
        page=page,
        size=size,
        total=len(api_list)  # This should ideally come from the API response
    )
    
    # Create response
    response_data = {
        "paginator": paginator,
        "items": api_list
    }
    
    return StandardResponse(
        type="array",
        data=response_data,
        status="success"
    )

@router.get("/api/detail/{api_id}")
async def get_api_detail(api_id: str, eolink_client: EolinkClient = Depends(get_eolink_client)):
    """
    Get detailed information about a specific API.
    """
    if not eolink_client.config_manager.eolink_api_key:
        return StandardResponse(
            type="error",
            data={"error": "Eolink API key not configured"},
            status="error"
        )
    
    api_detail = eolink_client.get_api_detail(api_id)
    
    if not api_detail:
        return StandardResponse(
            type="error",
            data={"error": f"API with ID {api_id} not found"},
            status="error"
        )
    
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
        api_id=api_detail.get("id", ""),
        api_name=api_detail.get("name", ""),
        api_uri=api_detail.get("path", ""),
        api_status=api_detail.get("status", 0),
        api_request_type=api_detail.get("request_type", 0),
        create_time=api_detail.get("create_time", ""),
        group_id=api_detail.get("group_id", 0),
        api_update_time=api_detail.get("update_time", ""),
        starred=api_detail.get("starred", 0),
        order_num=api_detail.get("order_num", 0),
        remove_time=api_detail.get("remove_time"),
        api_protocol=api_detail.get("protocol", 0),
        api_type=api_detail.get("type", "http"),
        api_manager_id=api_detail.get("manager_id", 0),
        update_user_id=api_detail.get("update_user_id", 0),
        create_user_id=api_detail.get("create_user_id", 0),
        group_path=api_detail.get("group_path", ""),
        group_name=api_detail.get("group_name", ""),
        customize_list=api_detail.get("customize_list", []),
        version_name=api_detail.get("version_name", ""),
        mock_enable=api_detail.get("mock_enable", True),
        case_cover=api_detail.get("case_cover", False),
        message_encoding=api_detail.get("message_encoding", "utf-8"),
        api_tag=api_detail.get("api_tag", ""),
        manager=api_detail.get("manager", ""),
        creator=api_detail.get("creator", ""),
        updater=api_detail.get("updater", ""),
        parameters=parameters,
        request_body=api_detail.get("requestBody", {}),
        responses=responses,
        tags=api_detail.get("tags", []),
        deprecated=api_detail.get("deprecated", False)
    )
    
    return StandardResponse(
        type="object",
        data={"api": detailed_info},
        status="success"
    )

@router.post("/config")
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
    
    return StandardResponse(
        type="object",
        data={"message": "Configuration updated successfully"},
        status="success"
    )

@router.get("/config")
async def get_config(config_manager: ConfigManager = Depends(get_config_manager)):
    """
    Get the current configuration settings.
    """
    config_data = {
        "eolink_api_key": "*****" if config_manager.eolink_api_key else "",
        "eolink_base_url": config_manager.eolink_base_url,
        "cache_ttl": config_manager.cache_ttl,
        "space_id": config_manager.space_id,
        "project_id": config_manager.project_id
    }
    
    return StandardResponse(
        type="object",
        data=config_data,
        status="success"
    )

@router.post("/clear-cache")
async def clear_cache(eolink_client: EolinkClient = Depends(get_eolink_client)):
    """
    Clear the API cache.
    """
    eolink_client.clear_cache()
    
    return StandardResponse(
        type="object",
        data={"message": "Cache cleared successfully"},
        status="success"
    )

@router.get("/test-connection")
async def test_connection(eolink_client: EolinkClient = Depends(get_eolink_client)):
    """
    Test the connection to Eolink API.
    """
    if not eolink_client.config_manager.eolink_api_key:
        return StandardResponse(
            type="error",
            data={"status": "error", "message": "Eolink API key not configured"},
            status="error"
        )
    
    connection_successful = eolink_client.test_connection()
    
    if connection_successful:
        return StandardResponse(
            type="object",
            data={"status": "success", "message": "Connection to Eolink API successful"},
            status="success"
        )
    else:
        return StandardResponse(
            type="error",
            data={"status": "error", "message": "Failed to connect to Eolink API"},
            status="error"
        )
