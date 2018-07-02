"""Basic Dtool HTTP server."""

import argparse
import os
import json

from http.server import HTTPServer, SimpleHTTPRequestHandler

import dtoolcore
from dtoolcore.utils import urlunparse


class DtoolHTTPRequestHandler(SimpleHTTPRequestHandler):

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


class DtoolHTTPServer(HTTPServer):
    pass


def serve_dtool_directory(directory, port):

    curdir = os.path.curdir

    os.chdir(directory)
    server_address = ("localhost", port)
    httpd = DtoolHTTPServer(server_address, DtoolHTTPRequestHandler)
    httpd.serve_forever()


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "dataset_directory",
        help="Directory with datasets to be served"
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8081,
        help="Port to serve datasets on (default 8081)"
    )
    args = parser.parse_args()
    if not os.path.isdir(args.dataset_directory):
        parser.error("Not a directory: {}".format(args.dataset_directory))

    serve_dtool_directory(args.dataset_directory, args.port)
