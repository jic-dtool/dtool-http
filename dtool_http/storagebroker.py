import os
import json
import shutil
import requests


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

    def list_overlay_names(self):
        """Return list of overlay names."""

        return []

def main():

    uri = 'https://jicinformatics.blob.core.windows.net/04c4e3a4-f072-4fc1-881a-602d589b089a'
    # r = requests.get('https://jicinformatics.blob.core.windows.net/04c4e3a4-f072-4fc1-881a-602d589b089a/dtool')

    # print(json.loads(r.text))

    b = HTTPStorageBroker(uri, None)

    identifier = '81b19a651bc43b4a97f0daae27c5bc89b0dedb7c'
    print b.get_item_abspath(identifier)

if __name__ == '__main__':
    main()
