from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

def get_marks(names):
    """Get marks for given names, returning 0 for unknown names."""
    return {name: 0 for name in names}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse URL and query parameters
        url_parts = urlparse(self.path)
        query_params = parse_qs(url_parts.query)
        
        # Get all names from the query parameters
        names = query_params.get('name', [])
        
        # Get marks for the requested names
        result = get_marks(names)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Convert response to JSON string
        import json
        response_data = json.dumps(result)
        
        # Send the response
        self.wfile.write(response_data.encode())
        
        return
