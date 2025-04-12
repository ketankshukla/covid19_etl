"""
Mock API server for testing the COVID-19 ETL pipeline.
"""
import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

# Sample vaccination data
VACCINATION_DATA = [
    {
        "date": "2023-01-15",
        "region": "California",
        "total_vaccinations": 100000,
        "people_vaccinated": 60000,
        "people_fully_vaccinated": 40000,
        "population": 40000000
    },
    {
        "date": "2023-01-15",
        "region": "New York",
        "total_vaccinations": 80000,
        "people_vaccinated": 50000,
        "people_fully_vaccinated": 30000,
        "population": 20000000
    },
    {
        "date": "2023-01-15",
        "region": "Texas",
        "total_vaccinations": 90000,
        "people_vaccinated": 55000,
        "people_fully_vaccinated": 35000,
        "population": 30000000
    },
    {
        "date": "2023-01-16",
        "region": "California",
        "total_vaccinations": 102000,
        "people_vaccinated": 61000,
        "people_fully_vaccinated": 41000,
        "population": 40000000
    },
    {
        "date": "2023-01-16",
        "region": "New York",
        "total_vaccinations": 82000,
        "people_vaccinated": 51000,
        "people_fully_vaccinated": 31000,
        "population": 20000000
    },
    {
        "date": "2023-01-16",
        "region": "Texas",
        "total_vaccinations": 92000,
        "people_vaccinated": 56000,
        "people_fully_vaccinated": 36000,
        "population": 30000000
    }
]

class MockAPIHandler(http.server.SimpleHTTPRequestHandler):
    """Handler for the mock COVID-19 API server."""
    
    def do_GET(self):
        """Handle GET requests."""
        # Parse URL
        parsed_url = urlparse(self.path)
        
        # Handle different endpoints
        if parsed_url.path == "/covid/vaccinations":
            self._handle_vaccinations()
        else:
            # Default 404 response
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
    
    def _handle_vaccinations(self):
        """Handle requests to the vaccinations endpoint."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        # Return vaccination data
        response_data = {
            "data": VACCINATION_DATA,
            "metadata": {
                "total_records": len(VACCINATION_DATA),
                "source": "Mock API"
            }
        }
        
        self.wfile.write(json.dumps(response_data).encode())

def start_mock_api(port=8000):
    """
    Start the mock API server.
    
    Args:
        port (int): Port to listen on
    """
    handler = MockAPIHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Mock API server running at http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_mock_api()