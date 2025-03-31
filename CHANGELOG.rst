CHANGELOG
=========

This project uses `semantic versioning <http://semver.org/>`_.
This change log uses principles from `keep a changelog <http://keepachangelog.com/>`_.

[Unreleased]
------------

Added
^^^^^


Changed
^^^^^^^


Deprecated
^^^^^^^^^^


Removed
^^^^^^^


Fixed
^^^^^


Security
^^^^^^^^

[0.5.2] - 2025-03-31
--------------------

Added
^^^^^

- GitHub CI test and publication workflows
- Dynamic versioning

Changed
^^^^^^^

- Transitoned from ``setup.py`` to ``pyporject.toml``

Fixed
^^^^^

- Generation of HTTP manifest URLs for base uris with signatures


[0.5.1] - 2021-06-23
--------------------

Fixed
^^^^^

- Licence file now included in release thanks to Jan Janssen (https://github.com/jan-janssen)


[0.5.0] - 2020-03-19
--------------------

This code was lost in a local branch, but was reimplemented and added to GitHub on 2021-06-21.

Added
^^^^^

- Added support for dataset tags


[0.4.0] - 2019-10-31
--------------------

Added
^^^^^

- Added support for dataset annotations


[0.3.0] - 2019-04-25
--------------------

Changed
^^^^^^^

- Cache environment variable changed from DTOOL_HTTP_CACHE_DIRECTORY to
  DTOOL_CACHE_DIRECTORY
- Default cache directory changed from ``~/.cache/dtool/http`` to
  ``~/.cache/dtool``


[0.2.1] - 2019-03-29
--------------------

Added
^^^^^

- Added MIT licence file


[0.2.0] - 2018-07-09
--------------------

Added
^^^^^

- Added ability to deal with redirects to enable working with shortened URLs

Fixed
^^^^^

- Made download to DTOOL_HTTP_CACHE_DIRECTORY more robust


[0.1.0] - 2018-07-05
--------------------

Initial release:

- HTTPStorageBackend
- HTTPSStorageBackend
- dtool_publish_dataset command line utility
- dtool_serve_dataset command line utility
