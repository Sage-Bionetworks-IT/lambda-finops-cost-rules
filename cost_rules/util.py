import os
import re


def get_os_var(varnam):
    try:
        return os.environ[varnam]
    except KeyError as exc:
        raise Exception(f"The environment variable '{varnam}' must be set")


def parse_env_list(string):
    '''
    Unpack a CSV into a list of strings.

    In order to pass a list of strings through an environment variable,
    it needs to be encoded in a single string, use CSV.
    '''
    return string.split(',')


def strip_special_chars(value):
    '''
    The name of a cost category must adhere to: ^(?! )[\p{L}\p{N}\p{Z}-_]*(?<! )$

    Replace any disallowed characters with '_'
    '''
    return re.sub('[^a-zA-Z0-9 -]', '_', value)
