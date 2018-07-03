import os
import getpass
import datetime

import pkg_resources

import click

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

import dtoolcore

from dtool_cli.cli import (
    CONFIG_PATH,
)


README_TEMPLATE_FPATH = pkg_resources.resource_filename(
    "dtool_create",
    os.path.join("templates", "README.yml")
)


def _get_readme_template(fpath=None):

    if fpath is None:
        fpath = dtoolcore.utils.get_config_value(
            "DTOOL_README_TEMPLATE_FPATH",
            CONFIG_PATH
        )
    if fpath is None:
        fpath = README_TEMPLATE_FPATH

    with open(fpath) as fh:
        readme_template = fh.read()

    user_email = dtoolcore.utils.get_config_value(
        "DTOOL_USER_EMAIL",
        CONFIG_PATH,
        "you@example.com"
    )

    user_full_name = dtoolcore.utils.get_config_value(
        "DTOOL_USER_FULL_NAME",
        CONFIG_PATH,
        "Your Name"
    )

    readme_template = readme_template.format(
        username=getpass.getuser(),
        DTOOL_USER_FULL_NAME=user_full_name,
        DTOOL_USER_EMAIL=user_email,
        date=datetime.date.today(),
    )

    return readme_template


@click.command()
@click.argument('uri')
def share_dataset(uri):
    azure_base_uri = "azure://jicinformatics"
    azure_uri = dtoolcore.copy(uri, azure_base_uri)
    dataset = dtoolcore.DataSet.from_uri(azure_uri)
    http_access_uri = dataset._storage_broker.http_enable()

    print("Dataset now accessible at: {}".format(http_access_uri))


@click.command()
@click.argument('path')
def create_and_share(path):

    name = path

    base_uri = "azure://jicinformatics"

    admin_metadata = dtoolcore.generate_admin_metadata(name)

    # Create the dataset.
    proto_dataset = dtoolcore.generate_proto_dataset(
        admin_metadata=admin_metadata,
        base_uri=base_uri,
        config_path=CONFIG_PATH)
    try:
        proto_dataset.create()
    except dtoolcore.storagebroker.StorageBrokerOSError as err:
        raise click.UsageError(str(err))

    readme_template = _get_readme_template()

    # Create an CommentedMap representation of the yaml readme template.
    yaml = YAML()
    yaml.explicit_start = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    descriptive_metadata = yaml.load(readme_template)

    def prompt_for_values(d):
        """Update the descriptive metadata interactively.

        Uses values entered by the user. Note that the function keeps recursing
        whenever a value is another ``CommentedMap`` or a ``list``. The
        function works as passing dictionaries and lists into a function edits
        the values in place.
        """
        for key, value in d.items():
            if isinstance(value, CommentedMap):
                prompt_for_values(value)
            elif isinstance(value, list):
                for item in value:
                    prompt_for_values(item)
            else:
                new_value = click.prompt(key, type=type(value), default=value)
                d[key] = new_value

    prompt_for_values(descriptive_metadata)

    stream = StringIO()
    yaml.dump(descriptive_metadata, stream)
    proto_dataset.put_readme(stream.getvalue())

    for filename in os.listdir(path):
        src_fpath = os.path.join(path, filename)
        relpath = filename
        proto_dataset.put_item(src_fpath, relpath)

    proto_dataset.freeze()

    http_access_uri = proto_dataset._storage_broker.http_enable()

    click.secho("\nDataset now accessible at: ", nl=False)
    click.secho("{}".format(http_access_uri), fg="green")


if __name__ == '__main__':
    create_and_share()
