import cssutils
import os

CSS_PATH = "data/css"
css_filename = "{}.css"


class CSS:

    def __init__(self, path):
        self.sheet = self.read_css(path)
        self.valid = self.sheet.valid

    def css_dict(self):
        return {
            rule.selectorText: rule
            for rule in self.sheet.cssRules
            if rule.type == rule.STYLE_RULE
        }

    def css_text(self):
        return self.sheet.cssText.decode("utf-8")

    def is_valid(self):
        return self.sheet.valid

    @staticmethod
    def read_css(path):
        with open(path, "r", encoding='utf-8') as f:
            css = f.read()
            sheet = cssutils.parseString(css)
        return sheet


class CSSBuilder:

    def __init__(self, scenario="drama", format='html'):
        self.scenario = scenario
        self.format = format
        self.default_css_object = self.load_default_css()
        self.default_sheet = self.default_css_object.sheet
        self.default_dict = self.default_css_object.css_dict()

    def load_default_css(self):
        filename = css_filename.format(self.scenario)
        css_path = os.path.join(CSS_PATH, self.scenario, self.format, filename)
        return CSS(css_path)

    @staticmethod
    def get_difference(custom_dict, default_dict):
        return set(custom_dict) - set(default_dict)

    @staticmethod
    def get_intersection(custom_dict, default_dict):
        return set(custom_dict) & set(default_dict)

    @staticmethod
    def change_existing(custom_dict, default_dict, tag):
        params = custom_dict[tag].style.keys()
        for param in params:
            default_dict[tag].style[param] = custom_dict[tag].style[param]

    def add_tag(self, custom_tag):
        new_style = custom_tag.cssText
        self.default_css_object.sheet.add(new_style)

    def add_difference(self, custom_dict):
        diff = self.get_difference(custom_dict, self.default_dict)
        for tag in diff:
            self.add_tag(custom_dict[tag])

    def add_intersection(self, custom_dict):
        inter = self.get_intersection(custom_dict, self.default_dict)
        for tag in inter:
            self.change_existing(custom_dict, self.default_dict, tag)

    def load_custom_css(self, custom_css_path):
        custom_css_object = CSS(custom_css_path)
        if custom_css_object.valid:
            custom_dict = custom_css_object.css_dict()
            self.add_difference(custom_dict)
            self.add_intersection(custom_dict)
        else:
            raise ValueError("css is not valid")

    def create_css(self, custom_css_path=None, as_string=False):
        if custom_css_path:
            self.load_custom_css(custom_css_path)
        if as_string:
            return self.default_css_object.css_text()
        return self.default_css_object
