from copy import copy
from typing import Any, Union

from functools import reduce

import yaml
from deepmerge import Merger

import os

my_merger = Merger(
    # pass in a list of tuple, with the
    # strategies you are looking to apply
    # to each type.
    [
        (list, ["override"]),
        (dict, ["merge"])
    ],
    # next, choose the fallback strategies,
    # applied to all other types:
    ["override"],
    # finally, choose the strategies in
    # the case where the types conflict:
    ["override"]
)


class MyDumper(yaml.Dumper):
    """
        MyDumper class inherite from yaml.Dumper for generating correct indentation for elements that start with dash
    """

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def dict_set_nested(d: dict, keys: list, value: Any):
    """
        This function set value for a key in nested dictionaries with given list of keys
    :param d: input dictionary
    :param keys: list of keys (index for list should be integer)
    :param value: set value
    :return: None
    """
    node = d
    key_count = len(keys)
    key_idx = 0

    for key in keys:
        key_idx += 1

        if key_idx == key_count:
            # assign value to considered key
            node[key] = value
            return d
        else:
            # replace inner dict to outer node
            if not (key in node):
                node[key] = dict()
                node = node[key]
            else:
                node = node[key]


# result and path related to find_path function
result = []
path = []


def find_path(dict_obj: dict, key: str, i=None) -> list:
    """
        This function find path of key occurrence in a list of keys.
        result and path variables should be outside of the scope of find_path to persist values during recursive calls to the function
    :param dict_obj: target dictionary
    :param key: considered  key
    :param i: i is the index of the list that dict_obj is part of
    - In our solution i is None because main data type is dictionary
    :return: list of paths for specific key
    """
    for k, v in dict_obj.items():
        # add key to path
        path.append(k)
        if isinstance(v, dict):
            # continue searching
            find_path(v, key, i)
        if isinstance(v, list):
            # search through list of dictionaries
            for i, item in enumerate(v):
                # add the index of list that item dict is part of, to path
                path.append(i)
                if isinstance(item, dict):
                    # continue searching in item dict
                    find_path(item, key, i)
                # if reached here, the last added index was incorrect, so removed
                path.pop()
        if k == key:
            # add path to our result
            result.append(copy(path))
        # remove the key added in the first line
        if path:
            path.pop()
    return result


# default starting index is set to None

def deep_get(dictionary: dict, keys: list, default=None) -> Union[str, int]:
    """
        This function is for get value from nested dictionary with list of keys
    :param dictionary: input dictionary
    :param keys: list of keys
    :param default: None
    :return: value of specific key
    """
    return reduce(lambda d, key: d[key] if isinstance(d, dict) or isinstance(d, list) else default, keys, dictionary)


def modify_path(list_of_paths: str, value: str) -> str:
    """
        This function is creating valid path for reading file of reference.
    :param list_of_paths: list of paths including considered key at the end of list
    :param value: file name
    :return: modified path
    """
    if len(list_of_paths) > 2:  # checking for path that has more than 2 elements for create valid file path
        if os.path.isabs(value):  # checking for absolute path
            # small modification on absolute paths and convert them to regular paths
            file_path = os.path.join(list_of_paths[0], '.' + value)
        else:
            file_path = os.path.join(list_of_paths[0], value)
    else:
        file_path = value
    return file_path


def swagger_merger_recursive(swagger_yaml: dict, base_dir: str, key: str = '$ref'):
    """
        This function is for merging swagger files and folders ($ref object and files)
    :param swagger_yaml: input of converted yml file to dict (dict type)
    :param key: referenced key - default value for swagger merging is $ref
    :return: None - modify input dict.
    """
    has_path_ref = True
    while has_path_ref:
        has_path_ref = False
        ref_paths = find_path(swagger_yaml, key)  # get ref paths with $ref at the end of list
        for item in ref_paths:
            ref_value_path = deep_get(swagger_yaml, item[:-1])[key]
            if not ref_value_path.startswith('#'):  # Just check $ref keys that have file paths
                has_path_ref = True
                file_path = modify_path(item, ref_value_path)
                # this part is for splitting ref value with # for some cases that has complex reference
                file_path = file_path.split('#')
                abs_path = file_path[0]
                open_file = open(os.path.join(base_dir, abs_path))
                yml_index_dict = yaml.load(open_file, yaml.FullLoader)
                if len(file_path) > 1:
                    yml_index_dict = yml_index_dict[file_path[1]]
                dict_set_nested(swagger_yaml, item[:-1], yml_index_dict)
        global result
        result = []
        global path
        path = []


def merge(index_file_name: str = 'index.yml', index_file_path: str = '', output_file_name: str = 'swagger.yml',
          output_file_path: str = ''):
    
    main_swagger_file = open(os.path.join('.', index_file_path, index_file_name))
    main_swagger = yaml.load(main_swagger_file, yaml.FullLoader)
    if output_file_path:
        output_file_path = '.' + '/' + output_file_path
    else:
        output_file_path = '.'
    swagger_merger_recursive(main_swagger, output_file_path)
    with open(output_file_name, 'w') as f:
        yaml.dump(main_swagger, f, Dumper=MyDumper, encoding='utf-8', allow_unicode=True,
                  sort_keys=False)
