from tei_auxiliary import read_yaml, load_directories


TT_CFG = read_yaml("data/config/tei_transformer.yaml")
HTMLT_CFG = read_yaml("data/config/html_transformer.yaml")
DOCX_CFG = read_yaml("data/config/docx_constructor.yaml")

SCHEMA_PATH = TT_CFG["PATHS"]["schema_dir"]
SCENARIOS = load_directories(SCHEMA_PATH)
