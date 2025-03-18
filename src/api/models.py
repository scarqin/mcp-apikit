from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ApiBasicInfo(BaseModel):
    """
    Basic information about an API.
    """
    id: str = Field(..., description="Unique identifier for the API")
    name: str = Field(..., description="Name of the API")
    method: str = Field(..., description="HTTP method (GET, POST, etc.)")
    path: str = Field(..., description="API path")
    description: Optional[str] = Field(None, description="API description")
    group: Optional[str] = Field(None, description="API group or category")

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

    class Config:
        orm_mode = True

class ApiListResponse(BaseModel):
    """
    Response model for API list endpoint.
    """
    apis: List[ApiBasicInfo] = Field(..., description="List of APIs")

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
