"""dtool_http package."""

import logging

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # Package is not installed; dtool-cli's ``dtool --version`` still
    # expects the attribute to exist.
    __version__ = "unknown"

logger = logging.getLogger(__name__)
