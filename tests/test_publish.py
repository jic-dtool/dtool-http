"""Test publish function."""

import dtoolcore

from . import tmp_disk_dataset_uri  # NOQA
from . import tmp_dtool_server  # NOQA


def test_disk_dataset_uri_fixture(tmp_disk_dataset_uri):  # NOQA

    dtoolcore.DataSet.from_uri(tmp_disk_dataset_uri)


def test_publish_command_functional(tmp_dtool_server):  # NOQA

    from dtool_http.publish import publish

    assert tmp_dtool_server + "/" == publish(tmp_dtool_server)
