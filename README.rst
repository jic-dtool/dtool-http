Add HTTP support to dtool for read only access to datasets
==========================================================

.. |dtool| image:: https://github.com/jic-dtool/dtool-http/blob/master/icons/22x22/dtool_logo.png?raw=True
    :height: 20px
    :target: https://github.com/jic-dtool/dtool-http
.. |pypi| image:: https://img.shields.io/pypi/v/dtool-http
    :target: https://pypi.org/project/dtool-http/
.. |tag| image:: https://img.shields.io/github/v/tag/jic-dtool/dtool-http
    :target: https://github.com/jic-dtool/dtool-http/tags
.. |test| image:: https://img.shields.io/github/actions/workflow/status/jic-dtool/dtool-http/test.yml?branch=master&label=tests
    :target: https://github.com/jic-dtool/dtool-http/actions/workflows/test.yml
.. |coverage|  image:: https://codecov.io/github/jic-dtool/dtool-http/coverage.svg?branch=master
    :target: https://codecov.io/github/jic-dtool/dtool-http?branch=master

|dtool| |pypi| |tag| |test| |coverage|

- GitHub: https://github.com/jic-dtool/dtool-http
- Free software: MIT License


Features
--------

- Publish dtool datasets by making them accessible via HTTP(S)
- Interact with dtool datasets over HTTP(S)
- Copy a dataset over HTTP(S)


Installation
------------

To install the dtool-http package.

.. code-block:: bash

    cd dtool-http
    python setup.py install


Usage
-----

To publish a dataset hosted in Amazon S3 or Microsoft Azure Storage use the
``dtool_publish_dataset`` command line utility::

    $ dtool_publish_dataset azure://jicinformatics/c58038a4-3a54-425e-9087-144d0733387f
    Dataset accessible at: https://jicinformatics.blob.core.windows.net/c58038a4-3a54-425e-9087-144d0733387f


To show the descriptive metadata of the published dataset:: 

    $ dtool readme show https://jicinformatics.blob.core.windows.net/c58038a4-3a54-425e-9087-144d0733387f
    ---
    description: Enterobacteria phage lambda, complete genome
    creation_date: 2018-02-06
    accession: NC_001416.1
    link: https://www.ncbi.nlm.nih.gov/nuccore/NC_001416.1
    reference: |
      Nucleotide [Internet]. Bethesda (MD):
      National Library of Medicine (US),
      National Center for Biotechnology Information; [1988] - .
      Accession No. NC_001416.1, Enterobacteria phage lambda, complete genome
      [cited 2018 Feb 06]
      Available from: https://www.ncbi.nlm.nih.gov/nuccore/NC_001416.1


To copy the dataset to local disk::

    $ dtool copy https://jicinformatics.blob.core.windows.net/c58038a4-3a54-425e-9087-144d0733387f ~/my_datasets
    Dataset copied to:
    file:///Users/olssont/my_datasets/lamda-phage-genome


Serving a directory of datasets over HTTP
-----------------------------------------

There is a simple utility for serving datasets in a directory over HTTP called
``dtool_serve_direcotry``. This is mainly useful for testing purposes.

Usage::

    $ dtool_serve_directory ~/my_datasets

The default port used is 8081. To show the descriptive metadata in the README
one can use dtool::

    $ dtool readme show http://localhost:8081/lamda-phage-genome
    ---
    description: Enterobacteria phage lambda, complete genome
    creation_date: 2018-02-06
    accession: NC_001416.1
    link: https://www.ncbi.nlm.nih.gov/nuccore/NC_001416.1
    reference: |
      Nucleotide [Internet]. Bethesda (MD):
      National Library of Medicine (US),
      National Center for Biotechnology Information; [1988] - .
      Accession No. NC_001416.1, Enterobacteria phage lambda, complete genome
      [cited 2018 Feb 06]
      Available from: https://www.ncbi.nlm.nih.gov/nuccore/NC_001416.1


Related packages
----------------

- `dtoolcore <https://github.com/jic-dtool/dtoolcore>`_
- `dtool-cli <https://github.com/jic-dtool/dtool-cli>`_
- `dtool-info <https://github.com/jic-dtool/dtool-info>`_
- `dtool-s3 <https://github.com/jic-dtool/dtool-s3>`_
- `dtool-azure <https://github.com/jic-dtool/dtool-azure>`_
