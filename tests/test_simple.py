import os

from dtoolcore import DataSet

def test_http_manifest_access():
    uri = "https://jicinformatics.blob.core.windows.net/04c4e3a4-f072-4fc1-881a-602d589b089a"

    dataset = DataSet.from_uri(uri)


def test_workflow():
    uri = "https://jicinformatics.blob.core.windows.net/04c4e3a4-f072-4fc1-881a-602d589b089a"
    example_identifier = "4cdf601a84d32afa820f03546e32b03e0cb5b5af"

    dataset = DataSet.from_uri(uri)

    assert len(dataset.identifiers) != 0
    assert dataset.get_readme_content().startswith('---')

    expected_overlay_names = set(["is_read1", "illumina_metadata"])
    assert set(dataset.list_overlay_names()) == expected_overlay_names

    assert example_identifier in dataset.get_overlay("is_read1")

    fpath = dataset.item_content_abspath(example_identifier)
    assert os.path.isfile(fpath)
