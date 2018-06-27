"""Test publish function."""

import dtoolcore

from click.testing import CliRunner

from . import tmp_disk_dataset_uri  # NOQA


def test_disk_dataset_uri_fixture(tmp_disk_dataset_uri):

    dtoolcore.DataSet.from_uri(tmp_disk_dataset_uri)


def test_publish_command_functional(tmp_disk_dataset_uri):

    from dtool_http.publish import publish

    runner = CliRunner()

    result = runner.invoke(publish, [tmp_disk_dataset_uri])

    assert result.exit_code == 401
