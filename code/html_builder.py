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

    """
    Prepares XSLT template for transformation.
    """

    # def __get_scema_name(self, scenario, keep_all):
    #     if scenario == "plain":
    #         filename, ftype = "plain", "all"
    #     elif scenario == "file-desc":
    #         filename, ftype = "fileDesc", "all"
    #     else:
    #         filename = "base"
    #         ftype = HTMLT_CFG['META']['ftypes'].get(keep_all)
    #     return filename, ftype

    # @staticmethod
    # def create_xslt_model(xsl_path):
    #     """
    #     Loads XSLT model.
    #     :param xsl_path: str
    #     :return: lxml object
    #     """
    #     xslt = etree.parse(xsl_path)
    #     xslt_model = etree.XSLT(xslt)
    #     return xslt_model

    @staticmethod
    def __get_xslt_name(scenario, keep_all=False):
        """
        Prepares default XSLT name.
        :param scenario: str
        :param keep_all: bool;
        :return: str
        """
        if scenario not in ("plain", "file-desc"):
            return "{}_{}".format("base", keep_all)
        return scenario

    def get_xsl_schema_path(self, scenario="drama", keep_all=False):
        """
        Prepares default XSLT path.
        :param scenario: str
        :param keep_all: bool
        :return: str
        """
        schema_name = self.__get_xslt_name(scenario, keep_all=keep_all)
        filename = HTMLT_CFG["PATTERNS"]["xsl_filename"].format(schema_name)
        xsl_path = os.path.join(HTMLT_CFG["PATHS"]["xsl_dir"], filename)
        return xsl_path

    @staticmethod
    def add_module(root, module, keep_all=False):
        """
        Adds module to the XSLT template
        :param root: lxml element
        :param module: str
        :param keep_all: bool
        :return: lxml element
        """
        xml = etree.Element("{http://www.w3.org/1999/XSL/Transform}include")
        xml.attrib['href'] = HTMLT_CFG['INCLUDE'][keep_all][module]
        root.insert(0, xml)
        return root

    def add_modules(self, xslt_model, modules, keep_all=False):
        """
        Adds modules to the XSLT template
        :param xslt_model: lxml xslt element
        :param modules: str
        :param keep_all: bool
        :return: lxml object
        """
        root = xslt_model.getroot()
        for module in modules:
            root = self.add_module(root, module, keep_all=keep_all)
        return xslt_model

    def load_xslt(self, scenario="drama", keep_all=False, modules=[]):
        """
        Loads XSLT template.
        :param scenario:
        :param keep_all:
        :param modules:
        :return:
        """
        xsl_path = self.get_xsl_schema_path(
            scenario=scenario, keep_all=keep_all
        )
        xslt = etree.parse(xsl_path)
        xslt = self.add_modules(xslt, modules, keep_all=keep_all)
        xslt_model = etree.XSLT(xslt)
        return xslt_model


class FullPageMaker(XSLTransformer):

    """
    Creates full page representation.
    """

    def create_full_page(self, dom, html, content):
        """
        Creates HTML full page.
        :param dom: TEI XML lxml tree
        :param html: transformed TEI to html lxml tree
        :param content: list
        :return: lxml object
        """
        html, text_content = self.create_text_content(html, content)
        full_page = etree.parse(HTMLT_CFG['PATHS']['doc_temp'])
        full_page = self.add_document(full_page, html)
        full_page = self.add_content(full_page, text_content)
        full_page = self.add_file_description(dom, full_page)
        return full_page

    def create_text_content(self, dom, content):
        """
        Create text content either from ODD or TEI.
        :param dom: lxml tree
        :param content: list
        :return:
        """
        if content:
            text_content = self.parse_tei_header(dom, content)
        else:
            text_content = self.get_text_content(dom)
        return dom, text_content

    @staticmethod
    def add_document(html, dom):
        """
        Adds TEI document to the HTML full page.
        :param html: lxml object of HTML full page
        :param dom: TEI XML lxml tree
        :return: lxml object
        """
        div_content = html.xpath(HTMLT_CFG['XPATH']['div_content'])[0]
        document = dom.xpath(HTMLT_CFG['XPATH']['tei_document'])[0]
        div_content.append(document)
        return html

    @staticmethod
    def add_content(html, text_content):
        """
        Adds text content to the HTML full page.
        :param html: lxml object of HTML full page
        :param text_content: list
        :return: lxml object
        """
        nav_content = html.xpath(HTMLT_CFG['XPATH']['ul_content'])[0]
        for index, content in enumerate(text_content):
            id_ = "c{}".format(index)
            temp = HTMLT_CFG['PATTERNS']['content'].format(id_, content)
            temp = etree.XML(temp)
            nav_content.append(temp)
        return html

    def add_file_description(self, dom, html):
        """
        Adds file description to the lxml HTML full page
        :param dom: TEI XML lxml tree
        :param html: lxml object of HTML full page
        :return: lxml object of HTML full page
        """
        file_desc = self.get_file_description(dom)
        div_content = html.xpath(HTMLT_CFG['XPATH']['fileinfo-content'])[0]
        div_content.append(file_desc)
        return html

    @staticmethod
    def parse_tei_header(dom, content):
        """
        Parse extracted according to ODD head elements.
        Form new IDs for head elements.
        :param dom: lxml tree
        :param content: list
        :return: list
        """
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
        """
        Parse extracted from TEI head elements.
        :param dom: lxml tree
        :return: list
        """
        text_content = []
        content = dom.xpath(HTMLT_CFG['XPATH']['text_content'])
        for index, item in enumerate(content):
            if item.text and item.text.strip():
                item.attrib['id'] = "c{}".format(index)
                text_content.append(item.text)
        return text_content

    def get_file_description(self, dom):
        """
        Extracts file description.
        :param dom: TEI XML lxml tree
        :return: lxml object
        """
        file_desc = dom.xpath(HTMLT_CFG['XPATH']['xml_file_desc'])
        if file_desc:
            xslt_model = self.load_xslt(scenario="file-desc", keep_all=True)
            html_tree = xslt_model(file_desc[0])
            html_tree = html_tree.xpath(
                HTMLT_CFG['XPATH']['html_file_desc'])[0]
            return html_tree
        return etree.XML(HTMLT_CFG['PATTERNS']['file_desc_dummy'])


class ReferenceFinder:

    """
    Finds all links in TEI.
    """

    def find_references(self, html_tree):
        """
        Finds all references.
        :param html: lxml tree
        :return: lxml tree
        """
        html_tree = self.find_ref_references(html_tree)
        html_tree = self.find_type_references(html_tree)
        html_tree = self.find_wiki_references(html_tree)
        return html_tree

    @staticmethod
    def find_ref_references(html):
        """
        Finds <ref> references.
        :param html: lxml tree
        :return: lxml tree
        """
        for item in html.xpath(HTMLT_CFG['XPATH']['ref_reference']):
            url = item.attrib['ref']
            line = HTMLT_CFG['PATTERNS']['ref'].format(url, item.text)
            line = etree.XML(line)
            item.text = ""
            item.append(line)
        return html

    @staticmethod
    def find_type_references(dom):
        """
        Finds @type='URL/URI' references.
        :param html: lxml tree
        :return: lxml tree
        """
        for item in dom.xpath(HTMLT_CFG['XPATH']['type_reference']):
            url = item.text
            if url:
                line = HTMLT_CFG['PATTERNS']['ref'].format(url, item.text)
                line = etree.XML(line)
                item.text = ""
                item.append(line)
        return dom

    def find_wiki_references(self, html):
        """
        Finds wikidata references
        :param html: lxml tree
        :return: lxml tree
        """
        for pattern in ['type', 'key']:
            qname = "wikidata_id_{}".format(pattern)
            results = html.xpath(HTMLT_CFG['XPATH'][qname])
            if results:
                self.parse_wiki_results(results)
        return html

    def parse_wiki_results(self, results):
        """
        Finds wikidata ID matches. Forms wikipedia links.
        :param results: list
        :return: None
        """
        for item in results:
            if not item.text: item.text = ''
            wiki_ids1 = re.findall("(Q\d+)\\b", item.text)
            wiki_ids2 = re.findall("(Q\d+)\\b", item.attrib.get('key', ''))
            wiki_ids = wiki_ids1 + wiki_ids2
            for wiki_id in wiki_ids:
                self.prepare_wiki_link(item, wiki_id)
                # wiki_url = self.get_wiki_link(wiki_id)
                # line = HTMLT_CFG['PATTERNS']['ref'].format(
                #     wiki_url, 'Wikipedia'
                # )
                # line = etree.XML(line)
                # item.text = ""
                # item.append(line)

    @staticmethod
    def get_wiki_link(qid):
        """
        Accesses wikidata. Tries to get wiki page link.
        :param qid: str
        :return: str/None
        """
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
        except:
            return None

    def prepare_wiki_link(self, item, wiki_id):
        """
        Extracts wiki ID.
        Adds link to the element.
        :param item: lxml element
        :param wiki_id: str
        :return: lxml element
        """
        wiki_url = self.get_wiki_link(wiki_id)
        text = item.text
        if not text: textcustom_css_path: PV = "(Wikipedia)"

        if wiki_url:
            line = HTMLT_CFG['PATTERNS']['ref'].format(
                wiki_url, text)
            line = etree.XML(line)
            item.text = ""
            item.append(line)
        return item


class HTMLBuilder(FullPageMaker, ReferenceFinder):

    """
    Interface for converting to HTMl format.
    """

    def __init__(self, scenario="drama", output_format='html'):
        """
        :param scenario: str
        :param output_format: str
        """
        self.scenario = check_scenario(scenario)
        self.CB = CSSBuilder(scenario=scenario, output_format=output_format)
        self.format = output_format
        self.modules_available = load_directories(
            HTMLT_CFG['PATHS']['xsl_dir']
        )

    def add_css(self, html_tree, custom_css_path=None):
        """
        Adds CSS line to the lxml tree.
        :param html_tree: lxml object
        :param custom_css_path: str
        :return:
        """
        style_tag = etree.Element("style")
        self.css = self.CB.create_css(custom_css_path=custom_css_path)
        style_tag.text = self.css.css_text()
        html_tree.find("/head").append(style_tag)
        return html_tree

    def get_modules_list(self):
        """
        Defines what thematic modules are available.
        :return: list
        """
        return self.modules_available

    @staticmethod
    def get_modules_by_scenario(scenario):
        """
        Get modules by scenario
        :param scenario: str
        :return: list
        """
        return HTMLT_CFG['MODULES'][scenario]

    def check_modules(self, modules, scenario):
        """
        Checks user modules.
        Selects available modules.
        :param modules: list
        :param scenario: str
        :return: list
        """
        if modules:
            modules = set(modules) & set(self.modules_available)
        else:
            modules = self.get_modules_by_scenario(scenario)
        return modules

    def create_template(self, scenario="drama", keep_all=False, modules=[]):
        """
        Create transformation template.
        :param scenario: str
        :param keep_all: bool
        :param modules: list
        :return: lxml object
        """
        modules = self.check_modules(modules, self.scenario)
        xslt_model = self.load_xslt(
            scenario=scenario,
            keep_all=keep_all,
            modules=modules
        )
        return xslt_model

    @staticmethod
    def parse_odd(tei, odd_path):
        """
        Parse ODD file.
        Extract head elements.
        :param tei: TEI XML object
        :param odd_path: str
        :return: TEI XML object, set
        """
        odd = TEIXML(odd_path, tei_ns=True)
        ignore_set = ODD.create_tag_set(odd, type_='odd_omit')
        tei = ODD.delete_ignored(tei, ignore_set)
        header_set = ODD.create_tag_set(odd, type_='heading')
        header_set = ODD.form_content(tei, header_set)
        return tei, header_set

    @staticmethod
    def check_transform_params(
            modules, keep_all, full_page, links,
            output_filename, custom_css_path, odd_path):
        """
        Checks transform function input parameters.
        :param modules: list
        :param keep_all: bool
        :param full_page: bool
        :param links: bool
        :param output_filename: str
        :param custom_css_path: str
        :param odd_path: str
        :return: None
        """
        if modules: check_iterable(modules, 'modules')
        if custom_css_path: PV.validate_path(custom_css_path, 'css')
        if odd_path: PV.validate_path(odd_path, 'odd')
        check_bool(keep_all, 'keep_all')
        check_bool(full_page, 'full_page')
        check_bool(links, 'links')
        PV.check_extension(output_filename, 'html_output')

    def perform_transformation(self, *args, **kwargs):
        """
        Performs TEI to HTML transformation.
        :param args: args for html_template function
        :param kwargs: kwargs for create_template function
        :return: lxml object
        """
        html_template = self.create_template(**kwargs)
        html_tree = html_template(*args)
        return html_tree

    def prepare_html_page(self, dom, html_tree, content, links, full_page):
        """
        Prepares HTML page
        :param dom: TEI XML lxml tree
        :param html_tree: lxml html tree
        :param content: list
        :param links: bool
        :param full_page: bool
        :return: lxml html tree
        """
        if links:
            self.find_references(html_tree)
        if full_page:
            html_tree = self.create_full_page(dom, html_tree, content)
        return html_tree

    def prepare_output(self, html_tree, *args, custom_css_path=None):
        """
        Prepares output product.
        html_tree: lxml html tree
        args: args for prepare_html_page function
        custom_css_path: None
        """
        if self.format == 'html':
            html_tree = self.prepare_html_page(*args)
        html_tree = self.add_css(html_tree, custom_css_path=custom_css_path)
        return html_tree

    def transform(self, tei, modules=[],
                  keep_all=False, output_filename='output.html',
                  odd_path=None, custom_css_path=None,
                  links=True, full_page=False):
        """
        Transforms TEI XML to HTML
        :param tei: TEI XML object
        :param modules: list
        :param keep_all: bool
        :param output_filename: str
        :param odd_path: str
        :param custom_css_path: str
        :param links: bool
        :param full_page: bool
        :return: None/str
        """

        self.check_transform_params(
            modules, keep_all, full_page, links,
            output_filename, custom_css_path, odd_path)

        content = []

        if odd_path:
            tei, content = self.parse_odd(tei, odd_path)

        html_tree = self.perform_transformation(
            tei.dom, scenario=self.scenario,
            keep_all=keep_all, modules=modules
        )

        html_tree = self.prepare_output(
            html_tree, tei.dom, html_tree,
            content, links, full_page,
            custom_css_path=custom_css_path
        )

        if self.format == 'html' and output_filename:
            write_html(output_filename, html_tree, full_page=full_page)
        return html_tree
