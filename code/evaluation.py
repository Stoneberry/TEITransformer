from tei_transformer import TEITransformer
import os


if __name__ == '__main__':

    dir_path = "../../test/data"
    schema_path = "../../schema.rng"
    TT = TEITransformer(scenario='drama')

    for filename in os.listdir(dir_path):
        tei_path = os.path.join(dir_path, filename)
        TT.load_tei(tei_path, schema_path=schema_path)
        TT.load_tei(tei_path, schema_path=schema_path)



