# -*- coding: utf-8 -*-
from xml_validators import XMLValidator
from tei_auxiliary import get_filename, check_scenario, check_bool, check_str
from director import Director
from tei_xml import TEIXML
import logging


class TEITransformer:

    """
    Client interface of the algorithm.
    """

    def __init__(self, scenario='plain'):
        """
        :param scenario: str
        """
        self.scenario = check_scenario(scenario)
        self.director = Director(scenario=self.scenario)
        self.validator = XMLValidator()
        self.valid = False

    def load_tei(self, tei_path, schema_path=None):
        """
        Creates an TEIXML object from a file and validates it against schema.
        :param tei_path: str
        :param schema_path: str
        :return: None
        """
        self.valid = False
        self.filename = get_filename(tei_path)
        self.validator.validate_path(tei_path, "file")
        self.tei = TEIXML(tei_path, tei_ns=True)
        self.valid = self.validator.validate(
            self.tei, schema_path=schema_path,
            scenario=self.scenario)

    def transform(self, output_format='html',
                  output_filename=None,
                  enable_valid=True, **kwargs):
        """
        Defines the transformation method.
        Performs a transformation.
        :param output_format: str
        :param output_filename: str
        :param enable_valid: bool
        :param kwargs: arguments for selected transformation method
        :return: None
        """
        check_bool(enable_valid, 'enable_valid')
        if not output_filename:
            output_filename = self.filename
        else:
            check_str(output_filename, 'output_filename')
        if self.valid or enable_valid is False:
            construction_method = self.director.select_construction_method(output_format)
            getattr(self.director, construction_method)(
                self.tei, output_filename=output_filename, **kwargs)
            logging.warning("The file was successfully transformed")
            return None
        raise ValueError("Unable to perform conversion for invalid file.")
