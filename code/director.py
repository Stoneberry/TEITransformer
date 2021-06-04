from docx_builder import DOCXBuilder
from html_builder import HTMLBuilder
from json_builder import JSONBuilder
from bs4 import BeautifulSoup
from setup import TT_CFG, SCENARIOS


class Director:

    """
    The class that controls the transformation process.
    Appoints workers.
    """

    def __init__(self, scenario='drama'):
        """
        :param scenario: str (drama or plain)
        """
        self.scenario = scenario
        # self.__check_scenario(scenario)
        self.JBuilder = JSONBuilder()

    def transform_html(self, tei, output_filename="output", **kwargs):
        """
        HTML transformation pipeline.
        Calls the HTMLBuilder class and converts TEI to HTML.
        :param tei: TEIXML object
        :param output_filename: str
        :param kwargs: arguments for HTMLBuilder transform method
        :return: None
        """
        output_filename = "{}.html".format(output_filename)
        self.HBuilder = HTMLBuilder(scenario=self.scenario, format="html")
        self.HBuilder.transform(tei, output_filename=output_filename, **kwargs)

    def transform_docx(self, tei, output_filename="output", **kwargs):
        """
        DOCX transformation pipeline.
        Calls the HTMLBuilder class and converts TEI to HTML.
        Calls the DOCXBuilder class and converts HTML to DOCX.
        :param tei: TEIXML object
        :param output_filename: str
        :param kwargs: arguments for DOCXBuilder transform method
        :return: None
        """
        output_filename = "{}.docx".format(output_filename)
        self.HBuilder = HTMLBuilder(scenario=self.scenario, format="docx")
        html_tree = self.HBuilder.transform(tei, **kwargs)
        soup = BeautifulSoup(str(html_tree), 'html.parser')
        self.DBuilder = DOCXBuilder(css=self.HBuilder.css)
        self.DBuilder.transform(soup, output_filename=output_filename)

    def transform_json(self, tei, output_filename="output"):
        """
        JSON transformation pipeline.
        Calls the JSONBuilder transformation metod and converts TEI to JSON.
        :param tei: TEIXML object
        :param output_filename: str
        :return: None
        """
        output_filename = "{}.json".format(output_filename)
        self.JBuilder.transform(tei, output_filename=output_filename)

    # def __check_scenario(self, scenario):
    #     if scenario not in SCENARIOS:
    #         raise ValueError('There are only 1 possible scenario: drama')
    #     self.scenario = scenario

    @staticmethod
    def __check_output_format(output_format):
        """
        Checks that output_format is supported.
        :param output_format: str
        :return: None
        """
        formats = TT_CFG['FORMATS']['output']
        if output_format not in formats:
            raise ValueError(
                'There are only following possible formats: {}'.format(formats)
            )

    def select_construction_method(self, output_format):
        """
        Selects the transformation method.
        :param output_format: str
        :return: str
        """
        self.__check_output_format(output_format)
        method_name = "transform_{}".format(output_format)
        return method_name
