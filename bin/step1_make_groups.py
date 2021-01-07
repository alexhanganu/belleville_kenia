#!/bin/python
# -*- coding: utf-8 -*-
#Alexandru Hanganu, 2020 nov 17

''' Read the source file with data
    extracts the corresponding variables
    checks that ids are present
    checks all variables
    excludes subjects from analysis, based on rules
Args:
    project variables (nimb style)
Return:
    True or False if all steps are correct and finished
'''

from os import listdir, path, walk, sep

from .vars import VARS
import pandas as pd
import numpy as np
import json
import logging

log = logging.getLogger(__name__)
logging.basicConfig(format='%(message)s')
log.setLevel(logging.INFO)

class MakeGroupFile:
    def __init__(self, project_vars, utils, Table):
        self.tab          = Table()
        self.project_vars = project_vars
        self.vars         = VARS(project_vars)
        self._id          = project_vars['id_col']
        self.files             = self.vars.f_source()
        self.exclude_nan  = False
        self.run()

    def run(self):
        src_file    = self.files['source']
        src_fs_file = self.files['freesurfer']
        df    = self.tab.get_df(src_file['file'],
                                    src_file['sheet'],
                                    src_file['cols'],
                                    src_file['ids'])
        df_fs = self.tab.get_df(src_fs_file['file'],
                                    src_fs_file['sheet'],
                                    src_fs_file['cols'],
                                    src_fs_file['ids'])
        self.grid_df = self.tab.join_dfs(df, df_fs, how='outer')
        self.populate_missing_data()
        # self.create_data_file()

    def populate_missing_data(self):
        

    def create_data_file(self):
        file_path_name = path.join(self.project_vars["materials_DIR"][1], self.project_vars["GLM_file_group"])
        log.info('creating file with groups {}'.format(file_path_name))
        self.tab.save_df(self.grid_df, file_path_name, sheet_name = 'grid')
