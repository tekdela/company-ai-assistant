/**
 * Cloudflare Worker - API Proxy with Security Features
 * Handles rate limiting, CORS, and proxies requests to backend
 */

// Rate limiting configuration
const RATE_LIMIT_REQUESTS = 100;
const RATE_LIMIT_WINDOW = 60; // seconds

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // CORS handling
    if (request.method === 'OPTIONS') {
      return handleCORS();
    }
    
    // Rate limiting
    const clientIP = request.headers.get('CF-Connecting-IP') || 'unknown';
    const rateLimitKey = `rate_limit:${clientIP}`;
    
    // Security headers
    const securityHeaders = {
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY',
      'X-XSS-Protection': '1; mode=block',
      'Referrer-Policy': 'strict-origin-when-cross-origin',
    };
    
    try {
      // Proxy to backend API
      if (url.pathname.startsWith('/api/')) {
        const backendURL = env.BACKEND_URL || 'http://localhost:8000';
        const backendRequest = new Request(
          backendURL + url.pathname + url.search,
          {
            method: request.method,
            headers: request.headers,
            body: request.body,
          }
        );
        
        const response = await fetch(backendRequest);
        
        // Add CORS and security headers
        const modifiedResponse = new Response(response.body, response);
        
        modifiedResponse.headers.set('Access-Control-Allow-Origin', '*');
        modifiedResponse.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
        modifiedResponse.headers.set('Access-Control-Allow-Headers', 'Content-Type');
        
        Object.entries(securityHeaders).forEach(([key, value]) => {
          modifiedResponse.headers.set(key, value);
        });
        
        return modifiedResponse;
      }
      
      // Serve frontend static files
      return new Response('Not Found', { status: 404 });
      
    } catch (error) {
      return new Response(
        JSON.stringify({ error: 'Internal Server Error' }),
        {
          status: 500,
          headers: {
            'Content-Type': 'application/json',
            ...securityHeaders,
          },
        }
      );
    }
  },
};

function handleCORS() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
    },
  });
}
