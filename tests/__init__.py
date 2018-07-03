"""Test fixtures."""

import os
import shutil
import tempfile
from urllib.parse import urlunparse
import threading

import dtoolcore
import pytest

_HERE = os.path.dirname(__file__)
_DATA = os.path.join(_HERE, "data")


def create_tmp_dataset(directory):
    admin_metadata = dtoolcore.generate_admin_metadata("tmp_dataset")

    proto_dataset = dtoolcore.generate_proto_dataset(
        admin_metadata=admin_metadata,
        base_uri=directory,
        config_path=None)

    proto_dataset.create()

    proto_dataset.put_readme("---\nproject: testing dtool\n")

    for fn in os.listdir(_DATA):
        fpath = os.path.join(_DATA, fn)
        proto_dataset.put_item(fpath, fn)

        _, ext = os.path.splitext(fn)
        proto_dataset.add_item_metadata(fn, "mimetype", ext)

    proto_dataset.freeze()

    return proto_dataset.uri


@pytest.fixture
def tmp_disk_dataset_uri(request):
    d = tempfile.mkdtemp()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)

    return create_tmp_dataset(d)


@pytest.fixture(scope="session")
def tmp_dtool_server(request):

    d = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(d)

    uri = create_tmp_dataset(d)
    dataset = dtoolcore.DataSet.from_uri(uri)

    server_address = ("localhost", 8081)

    from dtool_http.server import DtoolHTTPServer, DtoolHTTPRequestHandler
    httpd = DtoolHTTPServer(server_address, DtoolHTTPRequestHandler)

    def start_server():
        print("start dtool http server")
        httpd.serve_forever()

    t = threading.Thread(target=start_server)
    t.start()

    @request.addfinalizer
    def teardown():
        httpd.shutdown()
        print("stopping dtool http server")
        os.chdir(curdir)
        shutil.rmtree(d)

    netloc = "{}:{}".format(*server_address)
    path = dataset.name
    return urlunparse((
        "http",
        netloc,
        path,
        "", "", ""))
