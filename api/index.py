from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import os

def load_marks():
    """Load student marks from the JSON file."""
    # Get the absolute path to the JSON file
    # Since index.py is in /api/, we need to go up one level to reach repo_root
    current_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(current_dir, 'public', 'q-vercel-python.json')
    
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading marks: {e}")
        return {}  # Return empty dict if file can't be loaded

def get_marks(names):
    """Get marks for given names, returning 0 for unknown names."""
    student_marks = load_marks()
    ret_val = {"marks" : []}
    for name in names:
        for data in student_marks:
            if data["name"] == name:
                ret_val["marks"].append(data["marks"])
    return ret_val

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
        response_data = json.dumps(result)
        
        # Send the response
        self.wfile.write(response_data.encode())
        
        return
