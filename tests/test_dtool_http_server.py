import os

import pytest

from dtoolcore import DataSet

from . import tmp_dtool_server  # NOQA


def test_http_manifest_access(tmp_dtool_server):  # NOQA
    dataset = DataSet.from_uri(tmp_dtool_server)


def test_http_non_dataset_uri(tmp_dtool_server):  # NOQA
    import dtool_http
    with pytest.raises(dtool_http.storagebroker.HTTPError):
        dataset = DataSet.from_uri(tmp_dtool_server + "not-here")


def test_workflow(tmp_dtool_server):  # NOQA
    example_identifier = "1c10766c4a29536bc648260f456202091e2f57b4"

    dataset = DataSet.from_uri(tmp_dtool_server)

    assert len(dataset.identifiers) != 0
    assert dataset.get_readme_content().startswith('---')

    expected_overlay_names = set(["mimetype"])
    assert set(dataset.list_overlay_names()) == expected_overlay_names

    assert example_identifier in dataset.get_overlay("mimetype")

    fpath = dataset.item_content_abspath(example_identifier)
    assert os.path.isfile(fpath)
