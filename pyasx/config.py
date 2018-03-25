"""
Configuration manager for pyasx. Loads values from pyasx/config.yml.
"""


import os
import yaml
import pprint


# pyasx configuration values, loaded from file
_config = {}


def load():
    """
    Loads the pyasx configuration from the `pyasx/config.yml` file.
    """

    global _config

    # build the config yml file path
    rel_path = os.path.dirname(__file__)
    yaml_path = "%s/config.yml" % rel_path

    # load config file
    with open(yaml_path, "r") as yaml_stream:

        # try:
        _config = yaml.load(yaml_stream)
        # except yaml.YAMLError as ex:
        #     print(ex)


def get(key):
    """
    Returns the value of the given configuration item.
    :param key: The configuration item to get, e.g. pyasx.config.get('endpoints', 'asx_index_csv')
    """

    global _config

    value = None

    # lazy load the config yaml
    if len(_config) == 0:
        load()

    # get value from config dict
    if key in _config:
        value = _config[key]

    return value


def set(key, value):
    """
    Set the value of the given confguration item. Handy to set ASX endpoints
    dynamically if the API endpoints are changed but pyasx hasn't been updated
    to reflect that.
    :param key: The config item to set
    :param value: The value to set the config item to
    """

    global _config

    _config[key] = value;
