# -*- coding: utf-8 -*-

from lxml import etree
import os
import re

from tei_auxiliary import write_html, load_directories, check_iterable,\
    check_bool, check_str, check_scenario
from css_builder import CSSBuilder
from path_validator import PathValidator
from tei_xml import TEIXML
from odd_processor import ODDProcessor
from setup import HTMLT_CFG, TT_CFG

from qwikidata.entity import WikidataItem
from qwikidata.linked_data_interface import get_entity_dict_from_api

ODD = ODDProcessor()
PV = PathValidator()


class XSLTransformer:

    # def __get_scema_name(self, scenario, keep_all):
    #     if scenario == "plain":
    #         filename, ftype = "plain", "all"
    #     elif scenario == "file-desc":
    #         filename, ftype = "fileDesc", "all"
    #     else:
    #         filename = "base"
    #         ftype = HTMLT_CFG['META']['ftypes'].get(keep_all)
    #     return filename, ftype

    @staticmethod
    def create_xslt_model(xsl_path):
        xslt = etree.parse(xsl_path)
        xslt_model = etree.XSLT(xslt)
        return xslt_model

    def __get_xslt_name(self, scenario, keep_all=False):
        if scenario not in ("plain", "file-desc"):
            return "{}_{}".format("base", keep_all)
        return scenario

    def get_xsl_schema_path(self, scenario="drama", keep_all=False):
        schema_name = self.__get_xslt_name(scenario, keep_all=keep_all)
        filename = HTMLT_CFG["PATTERNS"]["xsl_filename"].format(schema_name)
        xsl_path = os.path.join(HTMLT_CFG["PATHS"]["xsl_dir"], filename)
        return xsl_path

    def add_module(self, root, module, keep_all=False):
        xml = etree.Element("{http://www.w3.org/1999/XSL/Transform}include")
        xml.attrib['href'] = HTMLT_CFG['INCLUDE'][keep_all][module]
        root.insert(0, xml)
        return root

    def add_modules(self, xslt_model, modules, keep_all=False):
        root = xslt_model.getroot()
        for module in modules:
            root = self.add_module(root, module, keep_all=keep_all)
        return xslt_model

    def load_xslt(self, scenario="drama", keep_all=False, modules=[]):
        xsl_path = self.get_xsl_schema_path(scenario=scenario, keep_all=keep_all)
        xslt = etree.parse(xsl_path)
        xslt = self.add_modules(xslt, modules, keep_all=keep_all)
        xslt_model = etree.XSLT(xslt)
        return xslt_model


class HTMLBuilder(XSLTransformer):

    def __init__(self, scenario="drama", format='html'):
        self.scenario = check_scenario(scenario)
        self.CB = CSSBuilder(scenario=scenario, format=format)
        self.format = format
        self.modules_available = load_directories(HTMLT_CFG['PATHS']['xsl_dir'])

    def add_css(self, html_tree, custom_css_path=None):
        style_tag = etree.Element("style")
        self.css = self.CB.create_css(custom_css_path=custom_css_path)
        style_tag.text = self.css.css_text()
        html_tree.find("/head").append(style_tag)
        return html_tree

    def get_modules_list(self):
        return self.modules_available

    @staticmethod
    def get_modules_by_scenario(scenario):
        return HTMLT_CFG['MODULES'][scenario]

    def check_modules(self, modules, scenario):
        if modules:
            modules = set(modules) & set(self.modules_available)
        else:
            modules = self.get_modules_by_scenario(scenario)
        return modules

    def create_template(self, scenario="drama", keep_all=False, modules=[]):
        modules = self.check_modules(modules, self.scenario)
        xslt_model = self.load_xslt(scenario=scenario, keep_all=keep_all, modules=modules)
        return xslt_model

    @staticmethod
    def parse_odd(tei, odd_path):
        odd = TEIXML(odd_path, tei_ns=True)
        ignore_set = ODD.create_tag_set(odd, type_='odd_omit')
        tei = ODD.delete_ignored(tei, ignore_set)
        header_set = ODD.create_tag_set(odd, type_='heading')
        header_set = ODD.form_content(tei, header_set)
        return tei, header_set

    @staticmethod
    def parse_tei_header(dom, content):
        text_content, index = [], 0
        for item in content:
            name = etree.QName(item).localname
            path = HTMLT_CFG['XPATH']['header'].format(item.text, name)
            results = dom.xpath(path)
            for result in results:
                if result.text and result.text.strip():
                    result.attrib['id'] = "c{}".format(index)
                    text_content.append(result.text)
                    index += 1
        return text_content

    @staticmethod
    def get_text_content(dom):
        text_content = []
        content = dom.xpath(HTMLT_CFG['XPATH']['text_content'])
        for index, item in enumerate(content):
            if item.text and item.text.strip():
                item.attrib['id'] = "c{}".format(index)
                text_content.append(item.text)
        return text_content

    def create_text_content(self, dom, content):
        if content:
            text_content = self.parse_tei_header(dom, content)
        else:
            text_content = self.get_text_content(dom)
        return dom, text_content

    @staticmethod
    def add_document(html, dom):
        div_content = html.xpath(HTMLT_CFG['XPATH']['div_content'])[0]
        document = dom.xpath(HTMLT_CFG['XPATH']['tei_document'])[0]
        div_content.append(document)
        return html

    @staticmethod
    def add_content(html, text_content):
        nav_content = html.xpath(HTMLT_CFG['XPATH']['ul_content'])[0]
        for index, content in enumerate(text_content):
            id_ = "c{}".format(index)
            temp = HTMLT_CFG['PATTERNS']['content'].format(id_, content)
            temp = etree.XML(temp)
            nav_content.append(temp)
        return html

    def get_file_description(self, tei):
        file_desc = tei.xpath(HTMLT_CFG['XPATH']['xml_file_desc'])
        if file_desc:
            xslt_model = self.load_xslt(scenario="file-desc", keep_all=True)
            html_tree = xslt_model(file_desc[0])
            html_tree = html_tree.xpath(HTMLT_CFG['XPATH']['html_file_desc'])[0]
            return html_tree
        return etree.XML(HTMLT_CFG['PATTERNS']['file_desc_dummy'])

    def add_file_description(self, tei, html):
        file_desc = self.get_file_description(tei)
        div_content = html.xpath(HTMLT_CFG['XPATH']['fileinfo-content'])[0]
        div_content.append(file_desc)
        return html

    def create_full_page(self, tei, dom, content):
        dom, text_content = self.create_text_content(dom, content)
        html = etree.parse(HTMLT_CFG['PATHS']['doc_temp'])
        html = self.add_document(html, dom)
        html = self.add_content(html, text_content)
        html = self.add_file_description(tei, html)
        return html

    @staticmethod
    def get_wiki_link(qid):
        try:
            q_dict = get_entity_dict_from_api(qid)
            q_item = WikidataItem(q_dict)
            links = q_item.get_sitelinks()
            if not links:
                links = q_dict.get('sitelinks', {})
            if links:
                url = next(iter(links.values()))['url']
                return url
            return None
        except: return None

    def parse_wiki_results(self, results):
        for item in results:
            if not item.text: item.text = ''
            wiki_ids1 = re.findall("(Q\d+)\\b", item.text)
            wiki_ids2 = re.findall("(Q\d+)\\b", item.attrib.get('key', ''))
            wiki_ids = wiki_ids1 + wiki_ids2
            for wiki_id in wiki_ids:
                wiki_url = self.get_wiki_link(wiki_id)
                line = HTMLT_CFG['PATTERNS']['ref'].format(wiki_url, 'Wikipedia')
                line = etree.XML(line)
                item.text = ""
                item.append(line)

    def find_wiki_references(self, dom):
        for pattern in ['type', 'key']:
            qname = "wikidata_id_{}".format(pattern)
            results = dom.xpath(HTMLT_CFG['XPATH'][qname])
            if results:
                self.parse_wiki_results(results)
        return dom

    @staticmethod
    def find_ref_references(dom):
        for item in dom.xpath(HTMLT_CFG['XPATH']['ref_reference']):
            url = item.attrib['ref']
            line = HTMLT_CFG['PATTERNS']['ref'].format(url, item.text)
            line = etree.XML(line)
            item.text = ""
            item.append(line)
        return dom

    @staticmethod
    def find_type_references(dom):
        for item in dom.xpath(HTMLT_CFG['XPATH']['type_reference']):
            url = item.text
            if url:
                line = HTMLT_CFG['PATTERNS']['ref'].format(url, item.text)
                line = etree.XML(line)
                item.text = ""
                item.append(line)
        return dom

    def find_references(self, html_tree):
        html_tree = self.find_ref_references(html_tree)
        html_tree = self.find_type_references(html_tree)
        html_tree = self.find_wiki_references(html_tree)
        return html_tree

    @staticmethod
    def check_transform_params(
            modules, keep_all,full_page, links,
            output_filename, custom_css_path, odd_path):
        if modules: check_iterable(modules, 'modules')
        if custom_css_path: PV.validate_path(custom_css_path, 'css')
        if odd_path: PV.validate_path(odd_path, 'odd')
        check_bool(keep_all, 'keep_all')
        check_bool(full_page, 'full_page')
        check_bool(links, 'links')
        PV.check_extension(output_filename, 'html_output')

    def transform(self, tei, modules=[],
                  keep_all=False, output_filename='output.html',
                  odd_path=None, custom_css_path=None,
                  links=True, full_page=False):

        self.check_transform_params(
            modules, keep_all, full_page, links,
            output_filename, custom_css_path, odd_path)

        content = []
        if odd_path: tei, content = self.parse_odd(tei, odd_path)

        html_template = self.create_template(
            scenario=self.scenario, keep_all=keep_all, modules=modules)
        html_tree = html_template(tei.dom)

        if self.format == 'html':
            if links: self.find_references(html_tree)
            if full_page: html_tree = self.create_full_page(tei.dom, html_tree, content)

        html_tree = self.add_css(html_tree, custom_css_path=custom_css_path)

        if self.format == 'html' and output_filename:
            write_html(output_filename, html_tree, full_page=full_page)
        return html_tree
