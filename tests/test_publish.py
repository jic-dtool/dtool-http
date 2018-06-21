"""Test publish function."""

import dtoolcore

from . import tmp_disk_dataset_uri  # NOQA


def test_disk_dataset_uri_fixture(tmp_disk_dataset_uri):

    dtoolcore.DataSet.from_uri(tmp_disk_dataset_uri)
