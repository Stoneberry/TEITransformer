# -*- coding: utf-8 -*-
from lxml import etree
from collections import defaultdict
import json
from tei_auxiliary import write_json


class JSONBuilder:

    @staticmethod
    def parse_attributes(element):
        attrs = element.attrib
        return {
            etree.QName(at).localname: attrs[at]
            for at in attrs
        }

    def parse_elements(self, root, children, json):
        key = etree.QName(root).localname
        text = root.text
        if text: text = text.strip()
        d = {
            "attr": self.parse_attributes(root),
            "children": [],
            "value": text,
        }
        for element in children:
            value = self.parse_tree(element)
            d["children"].append(value)
        json[key] = d
        return json

    def parse_tree(self, root, data=None):
        if not data:
            data = defaultdict(list)
        children = root.getchildren()
        if children:
            data = self.parse_elements(root, children, data)
        elif root.text and root.text.strip():
            return {
                "value": root.text.strip(),
                "attr": self.parse_attributes(root)
            }
        return data

    def transform(self, dom, output_filename=None):
        data = defaultdict(list)
        root = dom.root
        data = self.parse_tree(root, data=data)
        if output_filename:
            write_json(output_filename, data)
            return None
        return json.dumps(data)
