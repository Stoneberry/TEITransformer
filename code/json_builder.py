# -*- coding: utf-8 -*-
from lxml import etree
from collections import defaultdict
import json
from tei_auxiliary import write_json


class JSONBuilder:

    """
    Interface for JSON transformation.
    """

    @staticmethod
    def parse_attributes(element):
        """
        Parse node attributes.
        :param element: lxml element
        :return: dict
        """
        attrs = element.attrib
        return {
            etree.QName(at).localname: attrs[at]
            for at in attrs
        }

    def parse_elements(self, root, children, output_data):
        """
        Parse lxml element.
        :param root: lxml object
        :param children: list of lxml objects
        :param output_data: {}
        :return:
        """
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
        output_data[key] = d
        return output_data

    def parse_tree(self, root, output_data=None):
        """
        Parse lxml tree.
        :param root: lxml object root
        :param output_data: dict
        :return: dict
        """
        if not output_data:
            output_data = defaultdict(list)
        children = root.getchildren()
        if children:
            output_data = self.parse_elements(root, children, output_data)
        elif root.text and root.text.strip():
            return {
                "value": root.text.strip(),
                "attr": self.parse_attributes(root)
            }
        return output_data

    def transform(self, dom, output_filename=None):
        """
        Transforms lxml tree to JSON
        :param dom: lxml object
        :param output_filename: str
        :return: None/dict
        """
        output_data = defaultdict(list)
        root = dom.root
        output_data = self.parse_tree(root, output_data=output_data)
        if output_filename:
            write_json(output_filename, output_data)
            return None
        return json.dumps(output_data, ensure_ascii=False)
