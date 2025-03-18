from jinja2 import Environment, FileSystemLoader
import os

def get_template_env():
    """
    Get the Jinja2 template environment.
    """
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
    os.makedirs(templates_dir, exist_ok=True)
    return Environment(loader=FileSystemLoader(templates_dir))

def create_default_templates():
    """
    Create default templates if they don't exist.
    """
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create index.html template
    index_path = os.path.join(templates_dir, "index.html")
    if not os.path.exists(index_path):
        with open(index_path, "w", encoding="utf-8") as f:
            f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCP-APIKit - Eolink API Integration</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f5f7fa;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background-color: #2c3e50;
            color: white;
            padding: 1rem;
            text-align: center;
        }
        h1 {
            margin: 0;
        }
        .card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            padding: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
        }
        input[type="text"],
        input[type="number"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #2980b9;
        }
        .status {
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
        }
        .tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 1px solid #ddd;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            border: 1px solid transparent;
            border-bottom: none;
            border-radius: 4px 4px 0 0;
            margin-right: 5px;
        }
        .tab.active {
            background-color: white;
            border-color: #ddd;
            border-bottom-color: white;
            margin-bottom: -1px;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .api-list {
            list-style: none;
            padding: 0;
        }
        .api-item {
            padding: 15px;
            border-bottom: 1px solid #eee;
        }
        .api-item:last-child {
            border-bottom: none;
        }
        .api-method {
            display: inline-block;
            padding: 3px 6px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 10px;
        }
        .get { background-color: #d1ecf1; color: #0c5460; }
        .post { background-color: #d4edda; color: #155724; }
        .put { background-color: #fff3cd; color: #856404; }
        .delete { background-color: #f8d7da; color: #721c24; }
        .api-path {
            font-family: monospace;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <header>
        <h1>MCP-APIKit</h1>
        <p>Eolink OpenAPI Integration for MCP Server</p>
    </header>

    <div class="container">
        <div class="tabs">
            <div class="tab active" data-tab="config">Configuration</div>
            <div class="tab" data-tab="apis">API List</div>
            <div class="tab" data-tab="about">About</div>
        </div>

        <div id="config" class="tab-content active card">
            <h2>Configuration</h2>
            <form id="config-form">
                <div class="form-group">
                    <label for="eolink-api-key">Eolink API Key</label>
                    <input type="text" id="eolink-api-key" placeholder="Enter your Eolink API Key" value="{{ config.eolink_api_key }}">
                </div>
                <div class="form-group">
                    <label for="eolink-base-url">Eolink Base URL</label>
                    <input type="text" id="eolink-base-url" placeholder="Enter Eolink Base URL" value="{{ config.eolink_base_url }}">
                </div>
                <div class="form-group">
                    <label for="space-id">Space ID</label>
                    <input type="text" id="space-id" placeholder="Enter Eolink Space ID" value="{{ config.space_id }}">
                </div>
                <div class="form-group">
                    <label for="project-id">Project ID</label>
                    <input type="text" id="project-id" placeholder="Enter Eolink Project ID" value="{{ config.project_id }}">
                </div>
                <div class="form-group">
                    <label for="cache-ttl">Cache TTL (seconds)</label>
                    <input type="number" id="cache-ttl" placeholder="Cache time-to-live in seconds" value="{{ config.cache_ttl }}">
                </div>
                <button type="submit">Save Configuration</button>
                <button type="button" id="test-connection">Test Connection</button>
                <button type="button" id="clear-cache">Clear Cache</button>
                <div id="config-status" class="status" style="display: none;"></div>
            </form>
        </div>

        <div id="apis" class="tab-content card">
            <h2>API List</h2>
            <button id="refresh-apis">Refresh API List</button>
            <div id="api-list-container">
                <p>Click the Refresh button to load APIs from Eolink.</p>
            </div>
        </div>

        <div id="about" class="tab-content card">
            <h2>About MCP-APIKit</h2>
            <p>MCP-APIKit is a microservice control plane service designed to fetch API information from Eolink OpenAPI and provide it to the IDE's MCP Server for API integration scenarios.</p>
            <h3>Features</h3>
            <ul>
                <li>Fetch complete API lists and detailed information from Eolink OpenAPI</li>
                <li>Provide standardized API data format for IDE integration</li>
                <li>Support for API information caching and updates</li>
                <li>Simple configuration interface for setting up Eolink OpenAPI credentials</li>
            </ul>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Tab switching
            const tabs = document.querySelectorAll('.tab');
            const tabContents = document.querySelectorAll('.tab-content');
            
            tabs.forEach(tab => {
                tab.addEventListener('click', function() {
                    const tabId = this.getAttribute('data-tab');
                    
                    // Remove active class from all tabs and contents
                    tabs.forEach(t => t.classList.remove('active'));
                    tabContents.forEach(c => c.classList.remove('active'));
                    
                    // Add active class to current tab and content
                    this.classList.add('active');
                    document.getElementById(tabId).classList.add('active');
                });
            });

            // Configuration form submission
            const configForm = document.getElementById('config-form');
            const configStatus = document.getElementById('config-status');
            
            configForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const apiKey = document.getElementById('eolink-api-key').value;
                const baseUrl = document.getElementById('eolink-base-url').value;
                const spaceId = document.getElementById('space-id').value;
                const projectId = document.getElementById('project-id').value;
                const cacheTtl = document.getElementById('cache-ttl').value;
                
                try {
                    const response = await fetch('/config', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            eolink_api_key: apiKey,
                            eolink_base_url: baseUrl,
                            space_id: spaceId,
                            project_id: projectId,
                            cache_ttl: parseInt(cacheTtl)
                        })
                    });
                    
                    const data = await response.json();
                    
                    configStatus.textContent = data.message;
                    configStatus.className = 'status success';
                    configStatus.style.display = 'block';
                    
                    setTimeout(() => {
                        configStatus.style.display = 'none';
                    }, 3000);
                } catch (error) {
                    configStatus.textContent = 'Error: ' + error.message;
                    configStatus.className = 'status error';
                    configStatus.style.display = 'block';
                }
            });

            // Test connection button
            const testConnectionBtn = document.getElementById('test-connection');
            
            testConnectionBtn.addEventListener('click', async function() {
                try {
                    const response = await fetch('/test-connection');
                    const data = await response.json();
                    
                    configStatus.textContent = data.message;
                    configStatus.className = data.status === 'success' ? 'status success' : 'status error';
                    configStatus.style.display = 'block';
                    
                    setTimeout(() => {
                        configStatus.style.display = 'none';
                    }, 3000);
                } catch (error) {
                    configStatus.textContent = 'Error: ' + error.message;
                    configStatus.className = 'status error';
                    configStatus.style.display = 'block';
                }
            });

            // Clear cache button
            const clearCacheBtn = document.getElementById('clear-cache');
            
            clearCacheBtn.addEventListener('click', async function() {
                try {
                    const response = await fetch('/clear-cache', {
                        method: 'POST'
                    });
                    const data = await response.json();
                    
                    configStatus.textContent = data.message;
                    configStatus.className = 'status success';
                    configStatus.style.display = 'block';
                    
                    setTimeout(() => {
                        configStatus.style.display = 'none';
                    }, 3000);
                } catch (error) {
                    configStatus.textContent = 'Error: ' + error.message;
                    configStatus.className = 'status error';
                    configStatus.style.display = 'block';
                }
            });

            // Refresh API list button
            const refreshApisBtn = document.getElementById('refresh-apis');
            const apiListContainer = document.getElementById('api-list-container');
            
            refreshApisBtn.addEventListener('click', async function() {
                try {
                    apiListContainer.innerHTML = '<p>Loading APIs...</p>';
                    
                    const response = await fetch('/api/list');
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.error || 'Failed to fetch API list');
                    }
                    
                    const data = await response.json();
                    
                    if (data.data && data.data.items && data.data.items.length > 0) {
                        let html = '<ul class="api-list">';
                        
                        data.data.items.forEach(api => {
                            // Determine the HTTP method based on api_request_type
                            let method = 'GET';
                            if (api.api_request_type === 1) {
                                method = 'POST';
                            } else if (api.api_request_type === 2) {
                                method = 'PUT';
                            } else if (api.api_request_type === 3) {
                                method = 'DELETE';
                            }
                            
                            const methodClass = method.toLowerCase();
                            html += `
                                <li class="api-item">
                                    <span class="api-method ${methodClass}">${method}</span>
                                    <span class="api-path">${api.api_uri}</span>
                                    <h3>${api.api_name}</h3>
                                    <p>${api.api_tag || 'No description available'}</p>
                                    <small>Group: ${api.group_name || 'Ungrouped'}</small>
                                </li>
                            `;
                        });
                        
                        html += '</ul>';
                        apiListContainer.innerHTML = html;
                    } else {
                        apiListContainer.innerHTML = '<p>No APIs found. Make sure your Eolink API key is configured correctly.</p>';
                    }
                } catch (error) {
                    apiListContainer.innerHTML = `<p class="error">Error: ${error.message}</p>`;
                }
            });
        });
    </script>
</body>
</html>
            """)
    
    return get_template_env()
