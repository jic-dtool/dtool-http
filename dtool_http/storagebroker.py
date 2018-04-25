import os
import json
import shutil
import requests

import xml.etree.ElementTree as ET

try:
    from urlparse import urlunparse
except ImportError:
    from urllib.parse import urlunparse

from dtoolcore.utils import (
    generate_identifier,
    get_config_value,
    mkdir_parents,
    generous_parse_uri,
)

class HTTPStorageBroker(object):

    key = "https"

    def __init__(self, uri, admin_metadata, config_path=None):

        scheme, netloc, path, _, _, _ = generous_parse_uri(uri)

        self.scheme = scheme
        self.netloc = netloc
        self.uuid = path[1:]

        self.structure_parameters = self.get_json_encoded_structure_by_suffix(
            'structure.json'
        )

        self.overlays_key_prefix = self.structure_parameters['overlays_key_prefix']

        self._cache_abspath = get_config_value(
            "DTOOL_HTTP_CACHE_DIRECTORY",
            config_path=config_path,
            default=os.path.expanduser("~/.cache/dtool/http")
        )

    # Helper functions
    def get_text_by_suffix(self, suffix):
        path = self.uuid + '/' + suffix

        uri = urlunparse((self.scheme, self.netloc, path, None, None, None))

        r = requests.get(uri)

        return r.text

    def get_json_encoded_structure_by_suffix(self, suffix):

        text = self.get_text_by_suffix(suffix)

        return json.loads(text)

    # Funtions to allow dataset retrieval
    def get_admin_metadata(self):
        admin_metadata_suffix = self.structure_parameters['admin_metadata_key']

        return self.get_json_encoded_structure_by_suffix(admin_metadata_suffix)

    def get_manifest(self):
        path = self.uuid + '/manifest.json'
        manifest_uri = urlunparse((self.scheme, self.netloc, path, None, None, None))

        r = requests.get(manifest_uri)

        return json.loads(r.text)

    def get_readme_content(self):
        self.readme_suffix = self.structure_parameters['dataset_readme_key']
        return self.get_text_by_suffix(self.readme_suffix)

    def has_admin_metadata(self):
        """Return True if the administrative metadata exists.

        This is the definition of being a "dataset".
        """

        try:
            self.get_admin_metadata()
            return True
        except:
            raise("Oops")

    def get_item_abspath(self, identifier):
        """Return absolute path at which item content can be accessed.

        :param identifier: item identifier
        :returns: absolute path from which the item content can be accessed
        """

        dataset_cache_abspath = os.path.join(
            self._cache_abspath,
            self.uuid
        )
        mkdir_parents(dataset_cache_abspath)

        manifest = self.get_manifest()
        relpath = manifest['items'][identifier]['relpath']
        _, ext = os.path.splitext(relpath)

        local_item_abspath = os.path.join(
            dataset_cache_abspath,
            identifier + ext
        )

        if not os.path.isfile(local_item_abspath):

            path = self.uuid + '/' + identifier
            url = urlunparse((self.scheme, self.netloc, path, None, None, None))
            r = requests.get(url, stream=True)
            with open(local_item_abspath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        return local_item_abspath

    def get_overlay(self, overlay_name):
        """Return overlay as a dictionary.

        :param overlay_name: name of the overlay
        :returns: overlay as a dictionary
        """

        overlay_suffix = self.overlays_key_prefix + overlay_name + '.json'

        return self.get_json_encoded_structure_by_suffix(overlay_suffix)

    def list_overlay_names(self):
        """Return list of overlay names."""

        md = {'restype': 'container', 'comp': 'list', 'prefix': 'overlays'}
        path = self.uuid
        url = urlunparse((self.scheme, self.netloc, path, None, None, None))

        r = requests.get(url, params=md)

        tree = ET.fromstring(r.text)

        overlay_names = []
        for blob in tree[1]:
            overlay_file = blob[0].text.rsplit('/', 1)[-1]
            overlay_name, ext = overlay_file.split('.')
            overlay_names.append(overlay_name)

        return overlay_names
