# -*- coding: utf-8 -*-

from collections import defaultdict
import re

from setup import TT_CFG


PREDICATES = '|'.join(TT_CFG["XPATH"]["predicates"])


class ODDProcessor:

    """
    Interface for ODD processing.
    """

    # @staticmethod
    # def create_ignore_set(xml):
    #     ignore_set = defaultdict(list)
    #     for item in xml.dom.xpath(TT_CFG["XPATH"]["odd_omit"],
    #           namespaces=xml.nsmap):
    #         tag = item.getparent().get('ident')
    #         condition = item.get('predicate')
    #         ignore_set[tag].append(condition)
    #     return ignore_set

    @staticmethod
    def create_tag_set(xml, type_='heading'):
        """
        Extracts tags and meta information from
            ODD file according to the model function.
        :param xml: lxml object
        :param type_: str
        :return: dict
        """
        tag_set = defaultdict(list)
        for item in xml.dom.xpath(
                TT_CFG["XPATH"][type_],
                namespaces=xml.nsmap):
            tag = item.getparent().get('ident')
            condition = item.get('predicate')
            tag_set[tag].append(condition)
        return tag_set

    @staticmethod
    def __create_namespace_pattern(xml):
        """
        Create namespace pattern.
        :param xml: lxml object
        :return: str
        """
        names = ':|'.join(xml.nsmap.keys())
        names += ':'
        names_patters = "({})".format(names)
        return names_patters

    @staticmethod
    def preprocess_condition(condition):
        """
        Preprocesses XPATH predicate string.
        :param condition: str
        :return: str
        """
        condition = re.sub('\\beq\\b', '=', condition)
        return condition

    @staticmethod
    def add_namespace_predicate(line):
        """
        Inserts namespace to the XPATH predicate string.
        :param line: str
        :return: str
        """
        predicates = re.findall(PREDICATES, line)
        for predicate in predicates:
            new = "{}tei_ns:".format(predicate)
            line = re.sub(predicate, new, line)
        return line

    @staticmethod
    def try_condition_delete(result, condition, xml):
        """
        Deletes node from lxml tree.
        :param result: lxml element
        :param condition: str
        :param xml: lxml object
        :return: None
        """
        try:
            condition_result = result.xpath(condition, namespaces=xml.nsmap)
            if condition_result:
                result.getparent().remove(result)
        except: pass

    @staticmethod
    def try_condition_add(result, condition, xml, content):
        """
        Adds node to content.
        :param result: lxml element
        :param condition: str
        :param xml: lxml object
        :param content: list
        :return: None
        """
        try:
            condition_result = result.xpath(condition, namespaces=xml.nsmap)
            if condition_result:
                content.append(result)
        except: pass

    def filter_condition_delete(self, result, conditions, xml, names_patters):
        """
        Filter found nodes according to the predicate
            condition for delete function.
        :param result: lxml element
        :param conditions: str
        :param xml: lxml object
        :param names_patters: str
        :return: None
        """
        for condition in conditions:
            condition = self.preprocess_condition(condition)
            if_ns = re.findall(names_patters, condition)
            if not if_ns:
                condition = self.add_namespace_predicate(condition)
            self.try_condition_delete(result, condition, xml)

    def filter_condition_add(
            self, result, conditions,
            xml, names_patters, content):
        """
        Filter found nodes according to the predicate
            condition for add function.
        :param result: lxml element
        :param conditions: str
        :param xml: lxml object
        :param names_patters: str
        :return: None
        """
        for condition in conditions:
            condition = self.preprocess_condition(condition)
            if_ns = re.findall(names_patters, condition)
            if not if_ns:
                condition = self.add_namespace_predicate(condition)
            self.try_condition_add(result, condition, xml, content)

    def check_tag_entries_delete(
            self, results, conditions,
            xml, names_patters):
        """
        Checks found results according to delete condition.
        :param results: list
        :param conditions:str
        :param xml: lxml object
        :param names_patters: str
        :return: None
        """
        for result in results:
            if conditions:
                self.filter_condition_delete(
                    result, conditions, xml, names_patters
                )
            else:
                result.getparent().remove(result)

    def check_tag_entries_collect(
            self, results, conditions, xml,
            names_patters, content):
        """
        Checks found results according to header condition.
        :param results: list
        :param conditions:str
        :param xml: lxml object
        :param names_patters: str
        :return: None
        """
        for result in results:
            if conditions:
                self.filter_condition_add(
                    result, conditions, xml,
                    names_patters, content)
            else:
                content.append(result)

    def delete_ignored(self, xml, ignore_set):
        """
        Delete ignored elements.
        :param xml: lxml object
        :param ignore_set: dict
        :return: lxml object
        """
        names_patters = self.__create_namespace_pattern(xml)
        for ignore_tag in ignore_set:
            xpath = '//tei_ns:{}'.format(ignore_tag)
            results = xml.dom.xpath(xpath, namespaces=xml.nsmap)
            conditions = ignore_set[ignore_tag]
            self.check_tag_entries_delete(
                results, conditions, xml, names_patters)
        return xml

    def form_content(self, xml, header_set):
        """
        Form document content.
        :param xml: lxml object
        :param header_set: dict
        :return: list
        """
        names_patters = self.__create_namespace_pattern(xml)
        content = []
        for header_tag in header_set:
            xpath = '//tei_ns:{}'.format(header_tag)
            results = xml.dom.xpath(xpath, namespaces=xml.nsmap)
            conditions = header_set[header_tag]
            self.check_tag_entries_collect(
                results, conditions, xml, names_patters, content)
        return content
