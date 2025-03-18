from pydantic import BaseModel, Field, root_validator
from typing import List, Dict, Any, Optional

class ApiBasicInfo(BaseModel):
    """
    Basic information about an API.
    """
    api_id: str = Field(..., description="Unique identifier for the API")
    api_name: str = Field(..., description="Name of the API")
    api_uri: str = Field(..., description="API path")
    api_status: int = Field(0, description="API status")
    api_request_type: int = Field(0, description="API request type")
    create_time: str = Field(None, description="Creation time")
    group_id: int = Field(None, description="Group ID")
    api_update_time: str = Field(None, description="Update time")
    starred: int = Field(0, description="Whether the API is starred")
    order_num: int = Field(0, description="Order number")
    remove_time: Optional[str] = Field(None, description="Remove time")
    api_protocol: int = Field(0, description="API protocol")
    api_type: str = Field("http", description="API type")
    api_manager_id: int = Field(0, description="API manager ID")
    update_user_id: int = Field(0, description="Update user ID")
    create_user_id: int = Field(0, description="Create user ID")
    group_path: str = Field(None, description="Group path")
    group_name: str = Field(None, description="Group name")
    customize_list: List[Any] = Field(default_factory=list, description="Customize list")
    version_name: str = Field("", description="Version name")
    mock_enable: bool = Field(True, description="Mock enable")
    case_cover: bool = Field(False, description="Case cover")
    message_encoding: str = Field("utf-8", description="Message encoding")
    api_tag: str = Field("", description="API tag")
    manager: Optional[str] = Field(None, description="Manager")
    creator: Optional[str] = Field(None, description="Creator")
    updater: Optional[str] = Field(None, description="Updater")

    class Config:
        orm_mode = True

class Paginator(BaseModel):
    """
    Pagination information.
    """
    page: int = Field(1, description="Current page number")
    size: int = Field(10, description="Items per page")
    total: int = Field(0, description="Total number of items")

    class Config:
        orm_mode = True

class ApiParameter(BaseModel):
    """
    API parameter information.
    """
    name: str = Field(..., description="Parameter name")
    type: str = Field(..., description="Parameter type")
    required: bool = Field(False, description="Whether the parameter is required")
    description: Optional[str] = Field(None, description="Parameter description")
    default_value: Optional[Any] = Field(None, description="Default value for the parameter")

    class Config:
        orm_mode = True

class ApiResponse(BaseModel):
    """
    API response information.
    """
    status_code: int = Field(..., description="HTTP status code")
    description: Optional[str] = Field(None, description="Response description")
    response_schema: Optional[Dict[str, Any]] = Field(None, description="Response schema", alias="schema")

    class Config:
        orm_mode = True

class ApiDetailedInfo(ApiBasicInfo):
    """
    Detailed information about an API.
    """
    parameters: List[ApiParameter] = Field(default_factory=list, description="API parameters")
    request_body: Optional[Dict[str, Any]] = Field(None, description="Request body schema")
    responses: List[ApiResponse] = Field(default_factory=list, description="API responses")
    tags: List[str] = Field(default_factory=list, description="API tags")
    deprecated: bool = Field(False, description="Whether the API is deprecated")

    class Config:
        orm_mode = True

class ConfigUpdateRequest(BaseModel):
    """
    Request model for updating configuration.
    """
    eolink_api_key: Optional[str] = Field(None, description="Eolink API key")
    eolink_base_url: Optional[str] = Field(None, description="Eolink base URL")
    cache_ttl: Optional[int] = Field(None, description="Cache TTL in seconds")
    space_id: Optional[str] = Field(None, description="Eolink space ID")
    project_id: Optional[str] = Field(None, description="Eolink project ID")

    class Config:
        orm_mode = True

class ApiListResponse(BaseModel):
    """
    Response model for API list endpoint.
    """
    paginator: Paginator = Field(..., description="Pagination information")
    items: List[ApiBasicInfo] = Field(..., description="List of APIs")

    class Config:
        orm_mode = True

class ApiDetailResponse(BaseModel):
    """
    Response model for API detail endpoint.
    """
    api: ApiDetailedInfo = Field(..., description="Detailed API information")

    class Config:
        orm_mode = True

class ErrorResponse(BaseModel):
    """
    Error response model.
    """
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Error details")

    class Config:
        orm_mode = True

class StandardResponse(BaseModel):
    """
    Standard API response format.
    """
    type: str = Field("array", description="Response type")
    data: Any = Field(..., description="Response data")
    status: str = Field("success", description="Response status")

    class Config:
        orm_mode = True
