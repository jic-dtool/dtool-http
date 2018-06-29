from dtoolcore import DataSet

from . import tmp_dtool_server  # NOQA


def test_http_manifest_access(tmp_dtool_server):  # NOQA
    dataset = DataSet.from_uri(tmp_dtool_server)
