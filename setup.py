from setuptools import setup

url = "https://github.com/jic-dtool/dtool-http"
version = "0.1.0"
readme = open('README.rst').read()

setup(
    name="dtool-http",
    packages=["dtool_http"],
    version=version,
    description="Add HTTP read only dataset support to dtool",
    long_description=readme,
    include_package_data=True,
    author="Matthew Hartley",
    author_email="Matthew.Hartley@jic.ac.uk",
    url=url,
    install_requires=[
        "dtoolcore>=3.0"
    ],
    entry_points={
        "dtool.storage_brokers": [
            "HTTPStorageBroker=dtool_http.storagebroker:HTTPStorageBroker",
        ],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
