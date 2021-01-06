#!/bin/python

from os import path

class VARS():
    def __init__(self, project_vars):
        self.materials_DIR = project_vars["materials_DIR"][1]

    def f_source(self):
        return path.join(self.materials_DIR,
                'source','WM_Stats to Alex_22 dec 2020.xlsx')
