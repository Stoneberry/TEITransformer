from tei_transformer import TEITransformer
import os
from lxml import etree


if __name__ == '__main__':

    tei_path = "/Users/Stoneberry/Desktop/papers/master/2course/FINAL_TEI/rus000167-afinogenov-mashenka.tei.xml"
    schema_path = "/Users/Stoneberry/Desktop/papers/master/2course/FINAL_TEI/schema.rng"

    TT = TEITransformer(scenario='drama')
    TT.load_tei(tei_path, schema_path=schema_path)
    TT.transform(
        output_format='json',
        # keep_all=False,
        # full_page=True,
        enable_valid=False,
        # odd_path="/Users/Stoneberry/Desktop/new_xsls/tei_drama_odd.xml"
        # output_filename="output/output_chosen.docx",
        # custom_css_path=None
    )
