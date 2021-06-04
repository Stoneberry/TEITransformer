from tei_transformer import TEITransformer
import os
from lxml import etree


if __name__ == '__main__':
    
    # TT = TEITransformer(scenario='drama')

    # TEST 0

    # directory = "/Users/Stoneberry/Desktop/papers/master/2course/tei_transformer/data/test/test2"
    # tei_path = "test.xml"
    # os.chdir("/Users/Stoneberry/Desktop/papers/master/2course/FINAL_TEI/tei_transformer")

    # tei_path = "/Users/Stoneberry/Desktop/papers/master/2course/tei_transformer/data/test/test2/test.xml"
    # TT.load_tei(tei_path)


    # TEST 1

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

    # xslt = etree.parse('/Users/Stoneberry/Desktop/papers/master/2course/FINAL_TEI/tei_transformer/data/xsl/base.xsl')
    # root = xslt.getroot()
    # print(root)
    # # xslt_model = etree.XSLT(xslt)
    #
    # a = '<include href="drama/drama_all.xsl"/>'
    # xml = etree.Element("{http://www.w3.org/1999/XSL/Transform}include")
    # xml.attrib['href'] = "drama/drama_all.xsl"
    # root.insert(0, xml)
    #
    # print(etree.tostring(xslt))