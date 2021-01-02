#!/bin/python

from os import path

class VARS():
    def __init__(self):
        self.materials_DIR = "~/Dropbox/pKenia"

    def f_source(self):
        return path.join(self.materials_DIR,
                'source','WM_Stats to Alex_22 dec 2020.xlsx')
