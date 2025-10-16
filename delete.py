# get.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

data = [
    {
        "id": 1,
        "name": "Sam Larry",
        "track": "AI Developer"
    },
        {
        "id": 2,
        "name": "Tom Thompson",
        "track": "AI Engineer"
    }
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, data, status = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_DELETE(self):
        query = urlparse(self.path)
        params = parse_qs(query.query)
        item_id = params.get("id", [None]) [0]

        if not item_id:
            return self.send_data({"error": " Missing ?id parameter"}, 400)
        
        try:
            item_id = int(item_id)
        except ValueError:
            return self.send_data({"error": " Invalid ID format"}, 400)
        
        global data
        before = len(data)
        data = [item for item in data if item["id"] != item_id]

        if len(data) == before:
            return self.send_data({"error": " Item not found"}, 404)
        self.send_data({"message": f" Item with id {item_id} deleted"}, 200) 

def run():
    HTTPServer(('localhost', 8000), BasicAPI).serve_forever()

print("Application is running")
run()

    