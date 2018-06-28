# Requires Python3!

import os
import json
import http.server
from urllib.parse import urlunparse

import dtoolcore

PORT = 8000

class DtoolHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def generate_url(self, suffix):
        url_base_path = os.path.dirname(self.path)
        netloc = "{}:{}".format(*self.server.server_address)
        return urlunparse((
            "http",
            netloc,
            url_base_path + "/" + suffix,
            "", "", ""))


    def generate_item_urls(self):
        item_urls = {}
        for i in self.dataset.identifiers:
            relpath = self.dataset.item_properties(i)["relpath"]
            url = self.generate_url("data/" + relpath)
            item_urls[i] = url
        return item_urls


    def generate_overlay_urls(self):
        overlays = {}
        for o in self.dataset.list_overlay_names():
            url = self.generate_url(".dtool/overlays/{}.json".format(o))
            overlays[o] = url
        return overlays


    def generate_http_manifest(self):
        base_path = os.path.dirname(self.translate_path(self.path))

        self.dataset = dtoolcore.DataSet.from_uri(base_path)

        admin_metadata_fpath = os.path.join(base_path, ".dtool", "dtool")
        with open(admin_metadata_fpath) as fh:
            admin_metadata = json.load(fh)


        http_manifest = {
            "admin_metadata": admin_metadata,
            "manifest_url": self.generate_url(".dtool/manifest.json"),
            "readme_url": self.generate_url("README.yml"),
            "overlays": self.generate_overlay_urls(),
            "item_urls": self.generate_item_urls()
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