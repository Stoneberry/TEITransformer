# -*- coding: utf-8 -*-

import os
import re
import yaml
import json
import logging


SCHEMA_PATH = "data/schema/scenarios"
size_pattern = re.compile("(?P<value>(?:\d|\.)+)(?P<measure>[a-z]+)")
rgb_pattern = re.compile("rgb\((?P<r>.+?), (?P<g>.+?), (?P<b>.+?)\)")
CSS_VALUE_PATTERNS = [size_pattern, rgb_pattern]


def read_yaml(path):
    with open(path) as f:
        data = yaml.safe_load(f)
    return data


def read_file(path):
    with open(path, "r", encoding='utf-8') as f:
        data = f.read()
    return data


def write_html(path, html, full_page=False):
    if full_page:
        html.write(path, pretty_print=True)
    else:
        with open(path, 'w', encoding="utf-8") as f:
            f.write(str(html))


def write_json(path, data):
    with open(path, "w") as outfile:
        json.dump(data, outfile)


def check_extension():
    pass


def load_directories(path):
    dirs = [name
        for name in os.listdir(path)
        if os.path.isdir(os.path.join(path, name))
    ]
    return dirs


def get_filename(path):
    filename = os.path.split(path)[-1]
    filename = os.path.splitext(filename)[0]
    return filename


def prepare_func_name(*args, ftype='parse'):
    name = "_".join((ftype,) + args)
    name = re.sub("-", "_", name)
    return name


def clean_text(text):
    return ' '.join(text.split())


def css_value_parser(line):
    global CSS_VALUE_PATTERNS
    for pattern in CSS_VALUE_PATTERNS:
        res = pattern.search(line)
        if res: return res.groupdict()
    return {}


def check_if_rgb(value):
    try:
        cond1 = isinstance(value, str)
        cond2 = len(value) == 3
        cond3 = all(isinstance(x, int) for x in value)
        if cond1 and cond2 and cond3: return True
        return False
    except:
        return False


def check_bool(value, name):
    if not isinstance(value, bool):
        raise ValueError("Wrong datatype. {} should be bool".format(name))
    return None


def check_str(value, name):
    if not isinstance(value, str):
        raise ValueError("Wrong datatype. {} should be string".format(name))
    return None


def check_iterable(value, name):
    if not isinstance(value, (list, tuple, set)):
        raise ValueError(
            "Wrong datatype. {} should be list, tuple or set".format(name)
        )
    return None


def check_scenario(scenario):
    if not isinstance(scenario, str):
        raise ValueError("Scenario. Wrong datatype.")
    scenarios = load_directories('data/schema/scenarios')
    if scenario in scenarios:
        return scenario
    logging.warning("Wrong senario. Available options: {}".format(*scenarios))
    return 'plain'
