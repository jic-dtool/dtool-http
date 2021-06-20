"""Test fixtures."""

import os
import random
import shutil
import tempfile
import threading
from contextlib import contextmanager

import dtoolcore
from dtoolcore.utils import urlunparse

import pytest


_HERE = os.path.dirname(__file__)
_DATA = os.path.join(_HERE, "data")


@contextmanager
def tmp_env_var(key, value):
    os.environ[key] = value
    yield
    del os.environ[key]


@contextmanager
def tmp_directory():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


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

    proto_dataset.put_annotation("project", "dtool-testing")
    proto_dataset.put_tag("amazing")
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

    port = random.randint(6000, 9000)
    server_address = ("localhost", port)

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
