from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import urllib.parse
import json

class TokenHandler(BaseHTTPRequestHandler):
    token_urls = ['http://localhost:8000/token1', 'http://localhost:8000/token2', 'http://localhost:8000/token3']

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''<!DOCTYPE html>
<html>
<head>
   <title>Token Page</title>
</head>
<body>
    <h1>List of Token URLs:</h1>
    <ul>''')
            for url in self.token_urls:
                self.wfile.write(f'<li><button onclick="getToken(\'{url}\')">Get Token from {url}</button></li>'.encode())
            self.wfile.write(b'''</ul>
    <div>
        <h2>Your Token:</h2>
        <textarea rows="10" textarea cloumn="100"id="token" readonly></textarea>
    </div>
    <script>
        function getToken(url) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
             if (this.readyState == 4 && this.status == 200) {
                 document.getElementById("token").value = this.responseText;
                    }
                };
                xhr.open("GET", url + "?token=true", true);
                xhr.send();
            }
    </script>
 </body>
 </html>''')
        else:
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            if parsed_url.path in self.token_urls and 'token' in query_params:
                token = query_params['token'][0]
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(token.encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Not Found')

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, TokenHandler)
    webbrowser.open('http://localhost:8000/')
    httpd.serve_forever()
