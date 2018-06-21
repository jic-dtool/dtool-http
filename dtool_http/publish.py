"""Command for enabling HTTP access to a dataset.

TODO: Move into separate package to keep client
code separate from storage broker."""

import sys

import click

import dtoolcore

from dtool_cli.cli import (
    dataset_uri_argument,
    CONFIG_PATH,
)


@click.command()
@click.option("-q", "--quiet", is_flag=True)
@dataset_uri_argument
def publish(quiet, dataset_uri):
    """Enable public HTTP access to a cloud hosted dataset."""

    dataset = dtoolcore.DataSet.from_uri(dataset_uri)

    try:
        access_uri = dataset._storage_broker.http_enable()
    except AttributeError:
        click.secho(
            "Datasets of type '{}' cannot be published using HTTP".format(
                dataset._storage_broker.key
            ),
            fg="red",
            err=True
        )
        sys.exit(401)

    if quiet:
        click.secho(access_uri)
    else:
        click.secho("Dataset accessible at: ", nl=False)
        click.secho("{}".format(access_uri), fg="green")
