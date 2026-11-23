"""Test that the package registers the expected entry points."""

from importlib.metadata import distribution


def _entry_points(group):
    eps = distribution("dtool-http").entry_points
    return {ep.name: ep.value for ep in eps if ep.group == group}


def test_console_scripts_registered():
    assert _entry_points("console_scripts") == {
        "dtool_serve_directory": "dtool_http.server:cli",
        "dtool_publish_dataset": "dtool_http.publish:cli",
    }


def test_no_dtool_cli_plugins_registered():
    # The utilities are argparse based, not click commands, so they must not
    # be registered as dtool-cli plugins.
    assert _entry_points("dtool.cli") == {}


def test_storage_brokers_registered():
    assert _entry_points("dtool.storage_brokers") == {
        "HTTPStorageBroker": "dtool_http.storagebroker:HTTPStorageBroker",
        "HTTPSStorageBroker": "dtool_http.storagebroker:HTTPSStorageBroker",
    }
