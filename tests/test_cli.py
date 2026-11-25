"""Test the dtool_publish_dataset and dtool_serve_directory scripts."""

import os

import pytest

from . import tmp_disk_dataset_uri  # NOQA
from . import tmp_dtool_server  # NOQA


def test_publish_not_a_dataset(tmp_path, capsys):
    from dtool_http.publish import publish

    with pytest.raises(SystemExit) as exc:
        publish("file://" + str(tmp_path))
    assert exc.value.code == 1
    assert "Not a dataset" in capsys.readouterr().out


def test_publish_dataset_without_http_support(tmp_disk_dataset_uri, capsys):  # NOQA
    from dtool_http.publish import publish

    with pytest.raises(SystemExit) as exc:
        publish(tmp_disk_dataset_uri)
    assert exc.value.code == 2
    assert "cannot be published using HTTP" in capsys.readouterr().out


@pytest.mark.parametrize("quiet", [False, True])
def test_publish_cli(tmp_dtool_server, monkeypatch, capsys, quiet):  # NOQA
    from dtool_http.publish import cli

    argv = ["dtool_publish_dataset", tmp_dtool_server]
    if quiet:
        argv.append("-q")
    monkeypatch.setattr("sys.argv", argv)

    cli()

    out = capsys.readouterr().out.strip()
    if quiet:
        assert out == tmp_dtool_server + "/"
    else:
        assert out == "Dataset accessible at: " + tmp_dtool_server + "/"


def test_serve_cli_rejects_non_directory(tmp_path, monkeypatch, capsys):
    from dtool_http.server import cli

    monkeypatch.setattr(
        "sys.argv", ["dtool_serve_directory", str(tmp_path / "missing")])
    with pytest.raises(SystemExit) as exc:
        cli()
    assert exc.value.code == 2
    assert "Not a directory" in capsys.readouterr().err


@pytest.mark.parametrize("args, port", [([], 8081), (["-p", "9000"], 9000)])
def test_serve_cli(tmp_path, monkeypatch, args, port):
    """The server is started for the directory on the requested port."""
    import dtool_http.server

    started = {}

    class FakeServer:
        def __init__(self, server_address, handler):
            started["address"] = server_address
            started["handler"] = handler

        def serve_forever(self):
            started["serving"] = True

    monkeypatch.setattr(dtool_http.server, "DtoolHTTPServer", FakeServer)
    # serve_dtool_directory changes the working directory; monkeypatch
    # restores it after the test.
    monkeypatch.chdir(tmp_path)
    served = tmp_path / "datasets"
    served.mkdir()
    monkeypatch.setattr(
        "sys.argv", ["dtool_serve_directory", str(served), *args])

    dtool_http.server.cli()

    assert started == {
        "address": ("localhost", port),
        "handler": dtool_http.server.DtoolHTTPRequestHandler,
        "serving": True,
    }
    assert os.path.samefile(os.getcwd(), served)
