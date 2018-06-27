# Requires Python3!

import os
import json
import http.server

PORT = 8000

class DtoolHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def generate_http_manifest(self):
        base_path = os.path.dirname(self.translate_path(self.path))

        admin_metadata_fpath = os.path.join(base_path, ".dtool", "dtool")
        with open(admin_metadata_fpath) as fh:
            admin_metadata = json.load(fh)

        http_manifest = {
            "admin_metadata": admin_metadata,
            "manifest_url": "http://localhost:8000/html-test/.dtool/manifest.json",
            "readme_url": "http://localhost:8000/html-test/README.yml"
        }
        return bytes(json.dumps(http_manifest), "utf-8")

    def do_GET(self):
        if self.path.endswith("http_manifest.json"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(self.generate_http_manifest())
        else:
            super(DtoolHTTPRequestHandler, self).do_GET()



httpd = http.server.HTTPServer(('localhost', PORT), DtoolHTTPRequestHandler)
httpd.serve_forever()
