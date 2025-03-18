/**
 * MCP-APIKit - Main entry point
 * 
 * This file starts the MCP server for Eolink OpenAPI integration
 */
import express from 'express';
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import mcpServer from './services/mcpServer.js';

// Load environment variables
const PORT = process.env.PORT || 3000;
const TRANSPORT = process.env.TRANSPORT || 'http'; // 'http' or 'stdio'

/**
 * Start the MCP server with HTTP/SSE transport
 */
async function startHttpServer() {
  const app = express();
  app.use(express.json());

  // Set up basic routes
  app.get('/', (req, res) => {
    res.send('MCP-APIKit Server is running. Connect via Windsurf IDE.');
  });

  // Set up SSE endpoint for MCP
  app.get('/sse', async (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Access-Control-Allow-Origin', '*');

    const transport = new SSEServerTransport('/messages', res);
    
    // Store the transport in app.locals for message handling
    app.locals.transport = transport;
    
    try {
      await mcpServer.getServer().connect(transport);
    } catch (error) {
      console.error('Error connecting MCP server to transport:', error);
      res.end();
    }
  });

  // Set up message endpoint for client-to-server communication
  app.post('/messages', async (req, res) => {
    const transport = app.locals.transport;
    if (!transport) {
      return res.status(400).json({ error: 'No active SSE connection' });
    }

    try {
      await transport.handlePostMessage(req, res);
    } catch (error) {
      console.error('Error handling message:', error);
      res.status(500).json({ error: 'Failed to process message' });
    }
  });

  // Start the server
  app.listen(PORT, () => {
    console.log(`MCP-APIKit server running on http://localhost:${PORT}`);
    console.log('Connect via Windsurf IDE with the following configuration:');
    console.log(JSON.stringify({
      name: 'API Kit',
      type: 'http',
      url: `http://localhost:${PORT}`
    }, null, 2));
  });
}

/**
 * Start the MCP server with stdio transport
 */
async function startStdioServer() {
  console.log('Starting MCP-APIKit with stdio transport...');
  
  const transport = new StdioServerTransport();
  
  try {
    await mcpServer.getServer().connect(transport);
    console.log('MCP-APIKit server connected via stdio');
  } catch (error) {
    console.error('Error connecting MCP server to stdio transport:', error);
    process.exit(1);
  }
}

// Start the appropriate server based on transport configuration
if (TRANSPORT === 'stdio') {
  startStdioServer();
} else {
  startHttpServer();
}
