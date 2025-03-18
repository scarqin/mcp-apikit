/**
 * Service for interacting with Eolink OpenAPI
 */
import axios from 'axios';
import { Api, Project, ApiTestRequest, ApiTestResponse } from '../models/api.js';

class EolinkService {
  private apiKey: string;
  private baseUrl: string;

  constructor() {
    this.apiKey = process.env.EOLINK_API_KEY || '';
    this.baseUrl = process.env.EOLINK_BASE_URL || 'https://api.eolink.com';
    
    if (!this.apiKey) {
      console.warn('EOLINK_API_KEY not set. API requests will fail.');
    }
  }

  /**
   * Get all projects from Eolink
   */
  async getProjects(): Promise<Project[]> {
    try {
      const response = await axios.get(`${this.baseUrl}/projects`, {
        headers: this.getHeaders(),
      });
      return response.data.data || [];
    } catch (error) {
      console.error('Error fetching projects:', error);
      return [];
    }
  }

  /**
   * Get a specific project by ID
   */
  async getProject(projectId: string): Promise<Project | null> {
    try {
      const response = await axios.get(`${this.baseUrl}/projects/${projectId}`, {
        headers: this.getHeaders(),
      });
      return response.data.data || null;
    } catch (error) {
      console.error(`Error fetching project ${projectId}:`, error);
      return null;
    }
  }

  /**
   * Get all APIs for a project
   */
  async getApis(projectId: string): Promise<Api[]> {
    try {
      const response = await axios.get(`${this.baseUrl}/v3/api-management/apis?project_id=${projectId}`, {
        headers: this.getHeaders(),
      });
      return response.data.data || [];
    } catch (error) {
      console.error(`Error fetching APIs for project ${projectId}:`, error);
      return [];
    }
  }

  /**
   * Get a specific API by ID
   */
  async getApi(projectId: string, apiId: string): Promise<Api | null> {
    try {
      const response = await axios.get(`${this.baseUrl}/projects/${projectId}/apis/${apiId}`, {
        headers: this.getHeaders(),
      });
      return response.data.data || null;
    } catch (error) {
      console.error(`Error fetching API ${apiId} in project ${projectId}:`, error);
      return null;
    }
  }

  /**
   * Search for APIs across all projects
   */
  async searchApis(query: string): Promise<Api[]> {
    try {
      const response = await axios.get(`${this.baseUrl}/search/apis`, {
        headers: this.getHeaders(),
        params: { q: query },
      });
      return response.data.data || [];
    } catch (error) {
      console.error(`Error searching APIs with query "${query}":`, error);
      return [];
    }
  }

  /**
   * Test an API endpoint
   */
  async testApi(request: ApiTestRequest): Promise<ApiTestResponse> {
    try {
      // First, get the API details to construct the proper request
      const api = await this.getApi(request.projectId, request.apiId);
      if (!api) {
        throw new Error(`API ${request.apiId} not found in project ${request.projectId}`);
      }

      // Construct the URL with path parameters
      let url = api.path;
      if (request.pathParams) {
        Object.entries(request.pathParams).forEach(([key, value]) => {
          url = url.replace(`{${key}}`, encodeURIComponent(value));
        });
      }

      // Start timing the request
      const startTime = Date.now();

      // Make the request
      const response = await axios({
        method: api.method,
        url: url,
        headers: { ...this.getHeaders(), ...request.headers },
        params: request.queryParams,
        data: request.body,
      });

      // Calculate response time
      const responseTime = Date.now() - startTime;

      // Return formatted response
      return {
        statusCode: response.status,
        headers: response.headers as Record<string, string>,
        body: response.data,
        responseTime,
      };
    } catch (error: any) {
      console.error(`Error testing API ${request.apiId}:`, error);
      
      // Handle Axios error response
      if (error.response) {
        return {
          statusCode: error.response.status,
          headers: error.response.headers as Record<string, string>,
          body: error.response.data,
          responseTime: 0,
        };
      }
      
      // Handle other errors
      throw error;
    }
  }

  /**
   * Get common headers for Eolink API requests
   */
  private getHeaders(): Record<string, string> {
    return {
      'project_id': `${this.apiKey}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
  }
}

export default new EolinkService();
