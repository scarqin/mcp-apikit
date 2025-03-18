# MCP-APIKit

MCP-APIKit is a microservice control plane (MCP) server designed specifically for Windsurf IDE integration. It fetches API information from Eolink OpenAPI and provides it to the IDE's MCP client, enabling seamless API integration and management within your development environment.

## Features

- Connects to Eolink OpenAPI to retrieve API specifications
- Exposes API information as MCP resources
- Provides tools for API discovery and exploration
- Supports API testing and integration within Windsurf IDE
- Implements the Model Context Protocol (MCP) for standardized communication

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-apikit.git
cd mcp-apikit

# Install dependencies
pnpm install

# Build the project
pnpm run build
```

## Configuration

Create a `.env` file in the root directory with the following variables:

```
EOLINK_API_KEY=your_eolink_api_key
EOLINK_BASE_URL=https://api.eolink.com
SPACE_ID=your_space_id
PROJECT_ID=your_project_id
```

## Usage

### Starting the Server

```bash
pnpm start
```

The server will start on the port specified in your `.env` file (default: 3000).

### Connecting from Windsurf IDE

In your Windsurf IDE settings, add a new MCP server with the following configuration:

```json
{
  "name": "API Kit",
  "type": "http",
  "url": "http://localhost:3000"
}
```

## API Resources

The MCP-APIKit server exposes the following resources:

- `api://projects` - List all API projects
- `api://projects/{projectId}` - Get details for a specific project
- `api://projects/{projectId}/apis` - List all APIs in a project
- `api://projects/{projectId}/apis/{apiId}` - Get details for a specific API

## Tools

The server provides the following tools:

- `search-apis` - Search for APIs across all projects
- `test-api` - Test an API endpoint with custom parameters
- `import-api` - Import an API specification from Eolink to your project

## Development

```bash
# Run in development mode with hot reloading
npm run dev
```

## License

MIT
