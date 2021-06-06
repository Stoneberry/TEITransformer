import cssutils
import os

CSS_PATH = "data/css"
css_filename = "{}.css"


class CSS:

    """
    Class for converting CSS files into Python objects.
    """

    def __init__(self, path):
        """
        :param path: str
        """
        self.sheet = self.read_css(path)
        self.valid = self.sheet.valid

    def css_dict(self):
        """
        Converts the rules to a dictionary.
        CSS selector - key, rules - cssutils rule object.
        :return: dict
        """
        return {
            rule.selectorText: rule
            for rule in self.sheet.cssRules
            if rule.type == rule.STYLE_RULE
        }

    def css_text(self):
        """
        Converts all CSS rules to a string.
        :return: str
        """
        return self.sheet.cssText.decode("utf-8")

    def is_valid(self):
        """
        Checks whether CSS file is valid.
        :return: bool
        """
        return self.sheet.valid

    @staticmethod
    def read_css(path):
        """
        Reading a CCS file using the cssutils module.
        :param path: str
        :return: cssutils object
        """
        with open(path, "r", encoding='utf-8') as f:
            css = f.read()
            sheet = cssutils.parseString(css)
        return sheet


class CSSBuilder:

    """
    Generates a style sheet.
    """

    def __init__(self, scenario="drama", output_format='html'):
        """
        :param scenario: str
        :param output_format: str
        """
        self.scenario = scenario
        self.output_format = output_format
        self.default_css_object = self.load_default_css()
        self.default_sheet = self.default_css_object.sheet
        self.default_dict = self.default_css_object.css_dict()

    def load_default_css(self):
        """
        Loads default style sheet.
        :return: CSS object
        """
        filename = css_filename.format(self.scenario)
        css_path = os.path.join(
            CSS_PATH, self.scenario,
            self.output_format, filename
        )
        return CSS(css_path)

    @staticmethod
    def get_difference(custom_dict, default_dict):
        """
        Defines rules that are not present in the default style sheet.
        :param custom_dict: dict
        :param default_dict: dict
        :return: set
        """
        return set(custom_dict) - set(default_dict)

    @staticmethod
    def get_intersection(custom_dict, default_dict):
        """
        Defines rules that are present in the default style sheet.
        :param custom_dict: dict
        :param default_dict: dict
        :return: set
        """
        return set(custom_dict) & set(default_dict)

    @staticmethod
    def change_existing(custom_dict, default_dict, tag):
        """
        Replaces the default rule with the user rule.
        :param custom_dict: dict
        :param default_dict: dict
        :param tag:
        :return: None
        """
        params = custom_dict[tag].style.keys()
        for param in params:
            default_dict[tag].style[param] = custom_dict[tag].style[param]

    def add_tag(self, custom_tag):
        """
        Adds a rule to the default style sheet.
        :param custom_tag: cssutils rule
        :return: None
        """
        new_style = custom_tag.cssText
        self.default_css_object.sheet.add(new_style)

    def add_difference(self, custom_dict):
        """
        Adds rules that are not present in the default style sheet.
        :param custom_dict: dict
        :return: None
        """
        diff = self.get_difference(custom_dict, self.default_dict)
        for tag in diff:
            self.add_tag(custom_dict[tag])

    def add_intersection(self, custom_dict):
        """
        Changes rules that are present in the default style sheet
        :param custom_dict:
        :return:
        """
        inter = self.get_intersection(custom_dict, self.default_dict)
        for tag in inter:
            self.change_existing(custom_dict, self.default_dict, tag)

    def load_custom_css(self, custom_css_path):
        """
        Loads custom CSS file.
        Defines different rules.
        Changes default styles to match the user's styles.
        :param custom_css_path: str
        :return: None
        """
        custom_css_object = CSS(custom_css_path)
        if custom_css_object.valid:
            custom_dict = custom_css_object.css_dict()
            self.add_difference(custom_dict)
            self.add_intersection(custom_dict)
        else:
            raise ValueError("CSS is not valid.")

    def create_css(self, custom_css_path=None, as_string=False):
        """
        Creates a style object.
        Adds user styles.
        :param custom_css_path: str
        :param as_string: bool
        :return: CSS object/str
        """
        if custom_css_path:
            self.load_custom_css(custom_css_path)
        if as_string:
            return self.default_css_object.css_text()
        return self.default_css_object
