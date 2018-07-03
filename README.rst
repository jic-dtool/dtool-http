Add HTTP support to dtool for read only access to datasets
==========================================================

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
