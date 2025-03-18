/**
 * API models for Eolink OpenAPI integration
 */

// Project model representing an Eolink API project
export interface Project {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
}

// API model representing an individual API endpoint
export interface Api {
  id: string;
  name: string;
  projectId: string;
  path: string;
  method: HttpMethod;
  description?: string;
  requestHeaders?: Header[];
  requestParams?: Parameter[];
  requestBody?: RequestBody;
  responses?: Response[];
  createdAt: string;
  updatedAt: string;
}

// HTTP methods supported by the API
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH' | 'HEAD' | 'OPTIONS';

// Header model for request/response headers
export interface Header {
  name: string;
  value: string;
  description?: string;
  required: boolean;
}

// Parameter model for query/path parameters
export interface Parameter {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'array' | 'object';
  in: 'query' | 'path' | 'header' | 'cookie';
  description?: string;
  required: boolean;
  default?: any;
  example?: any;
}

// Request body model
export interface RequestBody {
  contentType: string;
  schema?: any;
  example?: any;
  required: boolean;
}

// Response model
export interface Response {
  statusCode: number;
  description?: string;
  headers?: Header[];
  contentType?: string;
  schema?: any;
  example?: any;
}

// API test request model
export interface ApiTestRequest {
  projectId: string;
  apiId: string;
  headers?: Record<string, string>;
  queryParams?: Record<string, string>;
  pathParams?: Record<string, string>;
  body?: any;
}

// API test response model
export interface ApiTestResponse {
  statusCode: number;
  headers: Record<string, string>;
  body: any;
  responseTime: number;
}
