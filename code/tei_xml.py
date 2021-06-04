# -*- coding: utf-8 -*-
from lxml import etree
from setup import TT_CFG


class TEIXML:

    """
    Python object for TEI XML data.
    """

    def __init__(self, path, tei_ns=False):
        """
        Defines XML tree, root element and namespaces.
        :param path: str
        :param tei_ns: bool
        """
        self.dom = self.load_from_file(path)
        self.root = self.dom.getroot()
        self.nsmap = self.root.nsmap
        if tei_ns:
            self.create_namespaces()

    @staticmethod
    def load_from_file(path):
        """
        Loads an XML file
        :param path: str
        :return: None
        """
        return etree.parse(path)

    def create_namespaces(self):
        """
        Defines a name for the default namespace.
        :return: None
        """
        if self.nsmap[None] == TT_CFG["SCHEMA"]['xs_tei']:
            self.nsmap['tei_ns'] = self.nsmap[None]
        else:
            self.nsmap['default'] = self.nsmap[None]
            self.nsmap['tei_ns'] = TT_CFG["SCHEMA"]['xs_tei']
        self.nsmap.pop(None)
