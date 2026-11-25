"""Test the dtool_http package."""


def test_version_is_string():
    import dtool_http
    assert isinstance(dtool_http.__version__, str)


def test_version_when_not_installed(monkeypatch):
    import importlib
    import importlib.metadata

    import dtool_http

    def not_installed(name):
        raise importlib.metadata.PackageNotFoundError(name)

    monkeypatch.setattr(importlib.metadata, "version", not_installed)
    try:
        importlib.reload(dtool_http)
        assert dtool_http.__version__ == "unknown"
    finally:
        monkeypatch.undo()
        importlib.reload(dtool_http)
    assert dtool_http.__version__ != "unknown"
