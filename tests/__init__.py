"""Test fixtures."""

import os
import shutil
import tempfile

import dtoolcore
import pytest

_HERE = os.path.dirname(__file__)
_DATA = os.path.join(_HERE, "data")


@pytest.fixture
def tmp_disk_dataset_uri(request):
    d = tempfile.mkdtemp()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)

    admin_metadata = dtoolcore.generate_admin_metadata("tmp_dataset")

    proto_dataset = dtoolcore.generate_proto_dataset(
        admin_metadata=admin_metadata,
        base_uri=d,
        config_path=None)

    proto_dataset.create()

    for fn in os.listdir(_DATA):
        fpath = os.path.join(_DATA, fn)
        proto_dataset.put_item(fpath, fn)

    proto_dataset.freeze()

    return proto_dataset.uri
