# -*- coding: utf-8 -*-
import os
from setup import TT_CFG


class PathValidator:

    @staticmethod
    def if_exists(filepath):
        if os.path.isfile(filepath):
            return True
        return False

    @staticmethod
    def check_extension(filepath, extension_type):
        filename, extension = os.path.splitext(filepath)
        return extension in TT_CFG['FORMATS'][extension_type]

    def validate_path(self, filepath, extension_type):
        exists = self.if_exists(filepath)
        cor_extension = self.check_extension(filepath, extension_type)
        if exists and cor_extension: return True
        raise OSError("Incorrect extension or file not found")



