# -*- coding: utf-8 -*-
from tei_auxiliary import prepare_func_name, clean_text, css_value_parser
from docx_constructor import DocxConstructor
from css_builder import CSSBuilder, CSS


class DocxCommon:

    """
    A class of auxiliary functions for DOCXBuilder
    """

    @staticmethod
    def empty(*args, **kwargs):
        """
        Stub function. Does nothing.
        """
        pass

    @staticmethod
    def is_nested(elem, child):
        """
        Checks if the vertex has children of a certain type.
        :param elem: html node
        :param child: str
        :return: bool
        """
        if len(elem.find_all(child)) > 0:
            return True
        return False

    @staticmethod
    def if_display_block(cls):
        """
        Checks whether node has display_block class
        :param cls: list
        :return: bool
        """
        if "display-block" in cls:
            return True
        return False

    def execute_elem_func(self, elem):
        """
        Selects a function for element parsing.
        :param elem: html node
        :return: None
        """
        cls = elem.attrs['class']
        if cls:
            func = prepare_func_name(cls[0])
            getattr(self, func, self.empty)()

    def execute_p_func(self, elem, p):
        cls = elem.attrs['class']
        if cls:
            func = prepare_func_name(cls[0], ftype="style")
            getattr(self, func, self.empty)(*p)

    def find_children(self, parent, child_type, **kwargs):
        """
        Finds children elements by type.
        :param parent: html node
        :param child_type: node selector str
        :param kwargs: b4s find_all arguments
        :return: None
        """
        children = parent.find_all(child_type, **kwargs)
        func = prepare_func_name(child_type)
        for child in children:
            getattr(self, func, self.empty)(child)


class DOCXBuilder(DocxCommon):

    """
    Interface for converting to DOCX format.
    """

    def __init__(self, css=None):
        self.DC = DocxConstructor()
        if isinstance(css, CSS):
            self.css = css.css_dict()
        else:
            self.css = {}

    def transform(self, soup, output_filename="output.docx"):
        """
        The function starts the transformation process.
        :param soup: b4s object
        :param output_filename: str
        :return: None
        """
        self.find_children(soup, "p")
        self.DC.save(output_filename)

    def parse_article(self, doc):
        for elem in doc:
            if elem.name and elem.text != "\n":
                self.find_children(elem, "p")

    def parse_p(self, part):
        classes = part.attrs.get("class", [])
        spans = part.find_all("span")
        if spans:
            self.parse_sp(classes, spans)
        else:
            self.parse_lowest_level(classes, part)

    def parse_sp(self, classes, spans):
        params = self.DC.add_line('')
        self.apply_class_styles(classes, params)
        paragraph = params[0]
        for span in spans:
            if not self.is_nested(span, "span"):
                paragraph = self.parse_span(span, paragraph)

    # def parse_sp(self, part):
    #     spans = part.find_all("span")
    #     params = self.DC.add_line('')
    #     self.apply_custom_style(".sp", params)
    #     paragraph = params[0]
    #     for span in spans:
    #         if not self.is_nested(span, "span"):
    #             paragraph = self.parse_span(span, paragraph)

    def parse_span(self, span, paragraph):
        classes = span.attrs.get("class", [])
        if self.if_display_block(classes):
            params = self.parse_display_block(classes, span)
        else:
            text = clean_text(span.text)
            run = paragraph.add_run(" " + text)
            params = (paragraph, run, run.font)
            self.apply_class_styles(classes, params)
        return params[0]

    def parse_display_block(self, classes, part):
        self.parse_lowest_level(classes, part)
        params = self.DC.add_line('')
        return params

    def parse_lowest_level(self, classes, part):
        text = clean_text(part.text)
        if text:
            params = self.DC.add_line(text)
            self.apply_class_styles(classes, params)
            return params
        elif 'pb' in classes:
            self.add_new_page()

    def add_new_page(self):
        params = self.DC.add_line('')
        self.DC.add_pb(*params)

    def apply_class_styles(self, classes, params):
        for cl in classes:
            cl_tag = '.{}'.format(cl)
            self.apply_custom_style(cl_tag, params)

    def apply_custom_style(self, tag, params):
        rule = self.css.get(tag)
        if rule:
            style_obj = rule.style
            for key in style_obj.keys():
                self.parse_style_rule(style_obj, key, params)

    def parse_style_rule(self, style_obj, key, params):
        line = style_obj[key]
        func = prepare_func_name(key, ftype='add')
        value = css_value_parser(line)
        if value.get('measure'):
            getattr(self.DC, func, self.empty)(
                *params, eval(value['value']),
                measure=value['measure'])
        elif list(value.keys()) == ['r', 'g', 'b']:
            values = [int(i) for i in value.values()]
            getattr(self.DC, func, self.empty)(*params, values)
        else:
            getattr(self.DC, func, self.empty)(*params, line)
