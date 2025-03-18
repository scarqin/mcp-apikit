/**
 * MCP Server implementation for API Kit
 * 
 * This file creates and configures the MCP server for Eolink OpenAPI integration
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import eolinkService from './eolinkService.js';
import { Api, Project } from '../models/api.js';

class Server {
  private server: McpServer;
  private projects: Project[] = [];
  private apis: Record<string, Api[]> = {};

  constructor() {
    // Initialize the MCP server
    this.server = new McpServer({
      name: 'API Kit',
      version: '1.0.0',
      description: 'MCP server for Eolink OpenAPI integration',
      capabilities: {
        // Define server capabilities here
        api_testing: true,
        api_documentation: true
      }
    });

    // Register handlers for MCP methods
    this.registerHandlers();

    // Load initial data
    this.loadProjects();
  }

  /**
   * Get the MCP server instance
   */
  getServer(): McpServer {
    return this.server;
  }

  /**
   * Register handlers for MCP methods
   */
  private registerHandlers(): void {
    // Register tool handlers using the new SDK pattern
    this.server.tool(
      "list_projects",
      {}, // No parameters
      async () => {
        const projects = await this.getProjects();
        return {
          content: [{ 
            type: "text", 
            text: JSON.stringify({ projects }, null, 2) 
          }]
        };
      }
    );

    this.server.tool(
      "get_project",
      { projectId: z.string().describe("Project ID") },
      async ({ projectId }) => {
        const project = await eolinkService.getProject(projectId);
        return {
          content: [{ 
            type: "text", 
            text: JSON.stringify({ project }, null, 2) 
          }]
        };
      }
    );

    this.server.tool(
      "list_apis",
      { projectId: z.string().describe("Project ID") },
      async ({ projectId }) => {
        const apis = await this.getApis(projectId);
        return {
          content: [{ 
            type: "text", 
            text: JSON.stringify({ apis }, null, 2) 
          }]
        };
      }
    );

    this.server.tool(
      "get_api",
      { 
        projectId: z.string().describe("Project ID"),
        apiId: z.string().describe("API ID")
      },
      async ({ projectId, apiId }) => {
        const api = await eolinkService.getApi(projectId, apiId);
        return {
          content: [{ 
            type: "text", 
            text: JSON.stringify({ api }, null, 2) 
          }]
        };
      }
    );

    this.server.tool(
      "search_apis",
      { query: z.string().describe("Search query") },
      async ({ query }) => {
        const apis = await eolinkService.searchApis(query);
        return {
          content: [{ 
            type: "text", 
            text: JSON.stringify({ apis }, null, 2) 
          }]
        };
      }
    );

    this.server.tool(
      "test_api",
      { 
        projectId: z.string().describe("Project ID"),
        apiId: z.string().describe("API ID"),
        headers: z.record(z.string()).optional().describe("Request headers"),
        queryParams: z.record(z.string()).optional().describe("Query parameters"),
        pathParams: z.record(z.string()).optional().describe("Path parameters"),
        body: z.any().optional().describe("Request body")
      },
      async (params) => {
        const response = await eolinkService.testApi(params);
        return {
          content: [{ 
            type: "text", 
            text: JSON.stringify({ response }, null, 2) 
          }]
        };
      }
    );

    // Add a resource example for API documentation
    this.server.resource(
      "api-docs",
      "api-docs://{projectId}/{apiId}",
      async (uri) => {
        // Extract parameters from the URI
        const uriParts = uri.pathname.split('/');
        const projectId = uriParts[1] || '';
        const apiId = uriParts[2] || '';
        
        const api = await eolinkService.getApi(projectId, apiId);
        if (!api) {
          return { contents: [] };
        }
        
        // Format API documentation
        const documentation = this.formatApiDocumentation(api);
        
        return {
          contents: [{
            uri: uri.href,
            text: documentation
          }]
        };
      }
    );
  }

  /**
   * Format API documentation as markdown
   */
  private formatApiDocumentation(api: Api): string {
    let doc = `# ${api.name}\n\n`;
    doc += `**Path:** ${api.path}\n`;
    doc += `**Method:** ${api.method}\n`;
    
    if (api.description) {
      doc += `\n## Description\n${api.description}\n`;
    }
    
    if (api.requestHeaders && api.requestHeaders.length > 0) {
      doc += `\n## Request Headers\n`;
      api.requestHeaders.forEach(header => {
        doc += `- **${header.name}** ${header.required ? '(Required)' : '(Optional)'}: ${header.description || ''}\n`;
      });
    }
    
    if (api.requestParams && api.requestParams.length > 0) {
      doc += `\n## Parameters\n`;
      api.requestParams.forEach(param => {
        doc += `- **${param.name}** (${param.in}) ${param.required ? '(Required)' : '(Optional)'}: ${param.description || ''}\n`;
      });
    }
    
    if (api.requestBody) {
      doc += `\n## Request Body\n`;
      doc += `Content Type: ${api.requestBody.contentType}\n`;
      if (api.requestBody.schema) {
        doc += `Schema: ${JSON.stringify(api.requestBody.schema, null, 2)}\n`;
      }
      if (api.requestBody.example) {
        doc += `Example: ${JSON.stringify(api.requestBody.example, null, 2)}\n`;
      }
    }
    
    if (api.responses && api.responses.length > 0) {
      doc += `\n## Responses\n`;
      api.responses.forEach(response => {
        doc += `### Status Code: ${response.statusCode}\n`;
        if (response.description) {
          doc += `${response.description}\n`;
        }
        if (response.contentType) {
          doc += `Content Type: ${response.contentType}\n`;
        }
        if (response.schema) {
          doc += `Schema: ${JSON.stringify(response.schema, null, 2)}\n`;
        }
        if (response.example) {
          doc += `Example: ${JSON.stringify(response.example, null, 2)}\n`;
        }
      });
    }
    
    return doc;
  }

  /**
   * Load all projects from Eolink
   */
  private async loadProjects(): Promise<void> {
    try {
      this.projects = await eolinkService.getProjects();
      console.log(`Loaded ${this.projects.length} projects from Eolink`);
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  }

  /**
   * Get all projects (with caching)
   */
  private async getProjects(): Promise<Project[]> {
    // Refresh projects if needed
    if (this.projects.length === 0) {
      await this.loadProjects();
    }
    return this.projects;
  }

  /**
   * Get all APIs for a project (with caching)
   */
  private async getApis(projectId: string): Promise<Api[]> {
    // Check cache first
    if (!this.apis[projectId]) {
      try {
        this.apis[projectId] = await eolinkService.getApis(projectId);
        console.log(`Loaded ${this.apis[projectId].length} APIs for project ${projectId}`);
      } catch (error) {
        console.error(`Error loading APIs for project ${projectId}:`, error);
        this.apis[projectId] = [];
      }
    }
    return this.apis[projectId];
  }
}

// Export a singleton instance
export default new Server();
