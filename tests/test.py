from tei_transformer import TEITransformer
from lxml import etree
import unittest
import os


class Test(unittest.TestCase):

    def test_validation_no_schema(self):
        """
        Validate against default schema
        """
        TT = TEITransformer(scenario='drama')
        tei_path = "tests/test_user_schema/tei.xml"
        TT.load_tei(tei_path)
        with self.assertRaises(ValueError):
            TT.transform(output_format="html")

    def test_validation_wrong_schema(self):
        """
        Validate against wrong schema
        """
        TT = TEITransformer(scenario='drama')
        tei_path = "tests/test_wrong_schema/tei.xml"
        schema_path = "tests/test_wrong_schema/schema.rng"
        TT.load_tei(tei_path, schema_path=schema_path)
        with self.assertRaises(ValueError):
            TT.transform(output_format="html")

    def test_validation_schema_rng(self):
        """
        Validate against user schema (rng)
        :return:
        """
        TT = TEITransformer(scenario='drama')
        tei_path = "tests/test_user_schema/tei.xml"
        schema_path = "tests/test_user_schema/schema.rng"
        self.assertIsNone(TT.load_tei(tei_path, schema_path=schema_path))

    def test_validation_schema_location(self):
        """
        Validates against schema location.
        Schema has to be located according to the specified path.
        """
        TT = TEITransformer(scenario='drama')
        tei_path = "tests/test_schema_location/tei.xml"
        self.assertIsNone(TT.load_tei(tei_path))

    def test_docx_drama_chosen_no_css_simple_no_links(self):
        """
        Test drama scenario with default css and limited content.
        Simple docx output. Links are not included.
        """
        TT = TEITransformer(scenario='drama')
        tei_path = "tests/test_drama_docx_chosen/tei.xml"
        schema_path = "tests/test_drama_docx_chosen/schema.rng"
        TT.load_tei(tei_path, schema_path=schema_path)
        try:
            TT.transform(
                output_format='docx',
                modules=[],
                keep_all=False,
                enable_valid=False,
                output_filename='tests/test_drama_docx_chosen/output_chosen',
                odd_path=None,
                custom_css_path=None,
                links=False,
                full_page=False)
        except:
            raise ValueError

    def test_html_plain_all_no_css_simple_links(self):
        """
        Test plain scenario with default css and the full content.
        Simple html output. Links are included.
        """
        TT = TEITransformer(scenario='plain')
        tei_path = "tests/test_plain_html_simple/tei.xml"
        schema_path = "tests/test_plain_html_simple/schema.rng"
        TT.load_tei(tei_path, schema_path=schema_path)
        try:
            TT.transform(
                modules=[],
                keep_all=True,
                output_filename='tests/test_plain_html_simple/output_all',
                odd_path=None,
                custom_css_path=None,
                links=True,
                enable_valid=False,
                full_page=False)
        except:
            raise ValueError

    def test_html_plain_chosen_css_full_links(self):
        """
        Test plain scenario with custom css and the full content.
        Full page html output. Links are included.
        """
        TT = TEITransformer(scenario='plain')
        tei_path = "tests/test_css/tei.xml"
        schema_path = "tests/test_css/schema.rng"
        TT.load_tei(tei_path, schema_path=schema_path)
        try:
            TT.transform(
                modules=[],
                keep_all=True,
                output_filename='tests/test_css/output_full',
                odd_path=None,
                custom_css_path="tests/test_css/custom.css",
                links=True,
                enable_valid=False,
                full_page=True)
        except:
            raise ValueError

    def test_html_drama_chosen_full_odd(self):
        """
        Test plain scenario with custom odd and the full content.
        Full page html output. Links are included.
        """
        TT = TEITransformer(scenario='plain')
        tei_path = "tests/test_odd/tei.xml"
        schema_path = "tests/test_odd/schema.rng"
        TT.load_tei(tei_path, schema_path=schema_path)
        try:
            TT.transform(
                modules=[],
                keep_all=False,
                output_filename='tests/test_odd/output_full',
                odd_path="tests/test_odd/odd.odd",
                custom_css_path=None,
                links=True,
                enable_valid=False,
                full_page=True)
        except:
            raise ValueError

    def test_json(self):
        """
        Test json.
        """
        TT = TEITransformer(scenario='plain')
        tei_path = "tests/test_json/tei.xml"
        schema_path = "tests/test_json/schema.rng"
        TT.load_tei(tei_path, schema_path=schema_path)
        try:
            TT.transform(
                output_format='json',
                enable_valid=False,
                output_filename="tests/test_json/output_chosen",
            )
        except:
            raise ValueError


if __name__ == '__main__':
    unittest.main()
