from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = []

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status = 201):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_PUT(self):
        content_size =int(self.headers.get("Content-Length", 0))
        parsed_data = self.rfile.read(content_size)

        post_data = json.loads(parsed_data)
        data.append(post_data)
        self.send_data({
            "Message": "Data updated  successfully",
            "data": post_data
        })

def run():
    HTTPServer(('localhost', 8000), BasicAPI).serve_forever()

print("Application is running")
run()



# from http.server import BaseHTTPRequestHandler, HTTPServer
# import json
# data = [
#     {"name": "Sam Larry", "track": "AI Developer"},
#     {"name": "Jane Doe", "track": "Web Developer"},
# ]
# class BasicAPI(BaseHTTPRequestHandler):
#     def send_data(self, payload, status = 200):
#         self.send_response(status)
#         self.send_header('content-type', "application/json")
#         self.end_headers()
#         self.wfile.write(json.dumps(payload).encode())
#     def do_PUT(self):
#         content_size = int(self.headers.get("content-length", 0))
#         parsed_data = self.rfile.read(content_size)
#         put_data = json.loads(parsed_data)
#         if "index" not in put_data or "data" not in put_data:
#             self.send_data({
#                 "Message": "Invalid request. 'index' and 'data' fields are required."
#             }, status=400)
#             return
#         index = put_data["index"]
#         new_data = put_data["data"]
#         if not isinstance(index, int) or index < 0 or index >= len(data):
#             self.send_data({
#                 "Message": "Index out of range."
#             }, status=400)
#             return
#         data[index] = new_data
#         self.send_data({
#             "Message": "Data Updated",
#             "data": new_data
#         })
# def run():
#     HTTPServer(("localhost", 8000), BasicAPI).serve_forever()
# print("Application is running")
# run()