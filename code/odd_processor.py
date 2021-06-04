# -*- coding: utf-8 -*-

from collections import defaultdict
import re

from setup import TT_CFG


PREDICATES = '|'.join(TT_CFG["XPATH"]["predicates"])


class ODDProcessor:

    # @staticmethod
    # def create_ignore_set(xml):
    #     ignore_set = defaultdict(list)
    #     for item in xml.dom.xpath(TT_CFG["XPATH"]["odd_omit"], namespaces=xml.nsmap):
    #         tag = item.getparent().get('ident')
    #         condition = item.get('predicate')
    #         ignore_set[tag].append(condition)
    #     return ignore_set

    @staticmethod
    def create_tag_set(xml, type_='heading'):
        tag_set = defaultdict(list)
        for item in xml.dom.xpath(TT_CFG["XPATH"][type_], namespaces=xml.nsmap):
            tag = item.getparent().get('ident')
            condition = item.get('predicate')
            tag_set[tag].append(condition)
        return tag_set

    @staticmethod
    def __create_namespace_pattern(xml):
        names = ':|'.join(xml.nsmap.keys())
        names += ':'
        names_patters = "({})".format(names)
        return names_patters

    @staticmethod
    def preprocess_condition(condition):
        condition = re.sub('\\beq\\b', '=', condition)
        return condition

    @staticmethod
    def add_namespace_predicate(line):
        predicates = re.findall(PREDICATES, line)
        for predicate in predicates:
            new = "{}tei_ns:".format(predicate)
            line = re.sub(predicate, new, line)
        return line

    @staticmethod
    def try_condition_delete(result, condition, xml):
        try:
            condition_result = result.xpath(condition, namespaces=xml.nsmap)
            if condition_result:
                result.getparent().remove(result)
        except: pass

    @staticmethod
    def try_condition_add(result, condition, xml, content):
        try:
            condition_result = result.xpath(condition, namespaces=xml.nsmap)
            if condition_result:
                content.append(result)
        except: pass

    def filter_condition_delete(self, result, conditions, xml, names_patters):
        for condition in conditions:
            condition = self.preprocess_condition(condition)
            if_ns = re.findall(names_patters, condition)
            if not if_ns:
                condition = self.add_namespace_predicate(condition)
            self.try_condition_delete(result, condition, xml)

    def filter_condition_add(self, result, conditions, xml, names_patters, content):
        for condition in conditions:
            condition = self.preprocess_condition(condition)
            if_ns = re.findall(names_patters, condition)
            if not if_ns:
                condition = self.add_namespace_predicate(condition)
            self.try_condition_add(result, condition, xml, content)

    def check_tag_entries_delete(self, results, conditions, xml, names_patters):
        for result in results:
            if conditions:
                self.filter_condition_delete(result, conditions, xml, names_patters)
            else:
                result.getparent().remove(result)

    def check_tag_entries_collect(self, results, conditions, xml, names_patters, content):
        for result in results:
            if conditions:
                self.filter_condition_add(
                    result, conditions, xml,
                    names_patters, content)
            else:
                content.append(result)

    def delete_ignored(self, xml, ignore_set):
        names_patters = self.__create_namespace_pattern(xml)
        for ignore_tag in ignore_set:
            xpath = '//tei_ns:{}'.format(ignore_tag)
            results = xml.dom.xpath(xpath, namespaces=xml.nsmap)
            conditions = ignore_set[ignore_tag]
            self.check_tag_entries_delete(results, conditions, xml, names_patters)
        return xml

    def form_content(self, xml, header_set):
        names_patters = self.__create_namespace_pattern(xml)
        content = []
        for header_tag in header_set:
            xpath = '//tei_ns:{}'.format(header_tag)
            results = xml.dom.xpath(xpath, namespaces=xml.nsmap)
            conditions = header_set[header_tag]
            self.check_tag_entries_collect(
                results, conditions, xml, names_patters, content)
        return content
