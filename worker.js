/**
 * Worker script for Calculator MCP Server
 */

// Cloudflare Workers for Python integration
export default {
  async fetch(request, env, ctx) {
    // Handle CORS preflight requests
    if (request.method === 'OPTIONS') {
      return handleCors();
    }

    try {
      // Forward to the Python endpoint
      const url = new URL(request.url);
      
      // If SSE endpoint is requested, handle it specially
      if (url.pathname === '/messages/' || url.pathname.startsWith('/messages')) {
        // Pass the request to our Python MCP server
        const response = await env.CALCULATOR_SERVICE.fetch(request.clone());
        
        // Add CORS headers to the response
        return addCorsHeaders(response);
      }
      
      // For all other endpoints, just pass through
      return env.CALCULATOR_SERVICE.fetch(request.clone());
    } catch (error) {
      return new Response(`Error: ${error.message}`, { status: 500 });
    }
  }
};

function handleCors() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Max-Age': '86400',
    }
  });
}

function addCorsHeaders(response) {
  const newHeaders = new Headers(response.headers);
  newHeaders.set('Access-Control-Allow-Origin', '*');
  newHeaders.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  newHeaders.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: newHeaders
  });
} 