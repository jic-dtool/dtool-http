import os

import pytest

from dtoolcore import DataSet

from . import tmp_dtool_server  # NOQA
from . import (
    tmp_env_var,
    tmp_directory,
)


def test_http_manifest_access(tmp_dtool_server):  # NOQA
    DataSet.from_uri(tmp_dtool_server)


def test_http_non_dataset_uri(tmp_dtool_server):  # NOQA
    import dtool_http
    with pytest.raises(dtool_http.storagebroker.HTTPError):
        DataSet.from_uri(tmp_dtool_server + "not-here")


def test_workflow(tmp_dtool_server):  # NOQA
    example_identifier = "1c10766c4a29536bc648260f456202091e2f57b4"

    with tmp_directory() as cache_dir:
        with tmp_env_var("DTOOL_CACHE_DIRECTORY", cache_dir):
            dataset = DataSet.from_uri(tmp_dtool_server)

            assert len(dataset.identifiers) != 0
            assert dataset.get_readme_content().startswith('---')

            expected_overlay_names = set(["mimetype"])
            assert set(dataset.list_overlay_names()) == expected_overlay_names
            assert example_identifier in dataset.get_overlay("mimetype")

            assert dataset.list_annotation_names() == ["project"]
            assert dataset.get_annotation("project") == "dtool-testing"
            assert dataset.list_tags() == ["amazing"]

            fpath = dataset.item_content_abspath(example_identifier)
            assert os.path.isfile(fpath)
