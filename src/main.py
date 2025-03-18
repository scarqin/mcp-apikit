import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .api.routes import router as api_router
from .utils.templates import create_default_templates
from .utils.config_manager import ConfigManager

# Create FastAPI app
app = FastAPI(
    title="MCP-APIKit",
    description="Microservice Control Plane for Eolink OpenAPI Integration",
    version="1.0.0"
)

# Create templates directory and default templates
templates = create_default_templates()

# Mount static files directory if it exists
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include API routes
app.include_router(api_router)

# Create config manager
config_manager = ConfigManager()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the main configuration page.
    """
    template = templates.get_template("index.html")
    
    # Get current configuration
    config = {
        "eolink_api_key": "*****" if config_manager.eolink_api_key else "",
        "eolink_base_url": config_manager.eolink_base_url,
        "cache_ttl": config_manager.cache_ttl,
        "space_id": config_manager.space_id,
        "project_id": config_manager.project_id
    }
    
    return HTMLResponse(template.render(config=config))

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "version": "1.0.0"}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return {"error": "Not Found", "detail": "The requested resource was not found"}

@app.exception_handler(500)
async def server_error_handler(request: Request, exc: HTTPException):
    return {"error": "Internal Server Error", "detail": str(exc)}

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("config", exist_ok=True)
    
    # Run the server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
