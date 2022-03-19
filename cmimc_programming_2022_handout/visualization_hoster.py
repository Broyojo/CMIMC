import http.server
import socketserver
import os

# change to an available port on your system.  this port will be used by your
# browser to retrieve local games for visualization.  no local game data is
# sent to any server
PORT = 8080
# change (if needed) to the location of your replays relative to this
# script on your system
DIR_TO_HOST = "replays"

# for the curious, this just does the standard 'python3 -m http.server <port>'
# but adds a cross-origin request policy so that javascript on cmimc-online
# can access the page.
class corp_handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin","https://cmimconline.org")
        http.server.SimpleHTTPRequestHandler.end_headers(self)

os.chdir(os.path.join(os.path.dirname(__file__), DIR_TO_HOST))
with socketserver.TCPServer(("localhost", PORT), corp_handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
