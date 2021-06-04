from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from tei_auxiliary import check_if_rgb


measures = {
    "pt": Pt,
    "cm": Cm,
    "int": Inches
}

FONT_VALUES = {
    "bold": ("bold", True),
    "italic": ("italic", True),
    "underline": ("underline", True),
    "uppercase": ("all_caps", True),
    "lowercase": ("all_caps", False)
 }


class DocxConstructor:

    def __init__(self):
        self.docx = Document()
        self.paragraph_format = self.docx.styles['Normal'].paragraph_format
        self.paragraph_format.space_after = Pt(5)

    def add_line(self, text):
        p = self.docx.add_paragraph()
        run = p.add_run(text)
        font = run.font
        return p, run, font

    @staticmethod
    def add_text_align(p, run, font, value):
        member_index = WD_ALIGN_PARAGRAPH._xml_to_member.get(value)
        if member_index:
            p.alignment = member_index

    @staticmethod
    def add_text_indent(p, run, font, value, measure=""):
        mfunc = measures.get(measure)
        if mfunc:
            p.paragraph_format.first_line_indent = mfunc(value)

    @staticmethod
    def add_margin_left(p, run, font, value, measure=""):
        mfunc = measures.get(measure)
        if mfunc:
            p.paragraph_format.left_indent = mfunc(value)

    @staticmethod
    def add_margin_right(p, run, font, value, measure=""):
        mfunc = measures.get(measure)
        if mfunc:
            p.paragraph_format.right_indent = mfunc(value)

    @staticmethod
    def add_margin_bottom(p, run, font, value, measure=""):
        mfunc = measures.get(measure)
        if mfunc:
            p.paragraph_format.space_after = mfunc(value)

    @staticmethod
    def add_margin_top(p, run, font, value, measure=""):
        mfunc = measures.get(measure)
        if mfunc:
            p.paragraph_format.space_before = mfunc(value)

    @staticmethod
    def add_line_height(p, run, font, value, measure=""):
        mfunc = measures.get(measure)
        if mfunc:
            p.paragraph_format.line_spacing = mfunc(value)

    @staticmethod
    def add_font_weight(p, run, font, value):
        params = FONT_VALUES.get(value)
        if params:
            font.__setattr__(*params)

    @staticmethod
    def add_font_style(p, run, font, value):
        params = FONT_VALUES.get(value)
        if params:
            font.__setattr__(*params)

    @staticmethod
    def add_color(p, run, font, value):
        if check_if_rgb(value):
            font.color.rgb = RGBColor(*value)

    @staticmethod
    def add_font_size(p, run, font, value, measure=""):
        mfunc = measures.get(measure)
        if mfunc:
            font.size = mfunc(value)

    @staticmethod
    def add_text_transform(p, run, font, value):
        params = FONT_VALUES.get(value)
        if params:
            font.__setattr__(*params)

    @staticmethod
    def add_text_decoration(p, run, font, value):
        params = FONT_VALUES.get(value)
        if params:
            font.__setattr__(*params)

    @staticmethod
    def add_pb(p, run, font):
        run.add_break(WD_BREAK.PAGE)
        # p.paragraph_format.page_break_before = True

    def save(self, out_path):
        self.docx.save(out_path)
