#!/bin/python
# -*- coding: utf-8 -*-
#Alexandru Hanganu, 20200107

''' Read the source file with data
    extract corresponding variables
    checks all variables
    populate missing variables
    excludes columns or subjects from analysis
Args:
    project variables (nimb style), utils (from nimb) and Table (from nimb)
Return:
    create the grid database (csv or xlsx)
    True or False if all steps are correct and finished
'''

import os
from .vars import VARS

class FSGLMrun:
    def __init__(self, project_vars, utils, Table, Preprocess):
        self.tab           = Table()
        self.preproc       = Preprocess()
        self.project_vars  = project_vars
        self.materials_DIR = self.project_vars["materials_DIR"][1]
        self.vars          = VARS(project_vars)
        self._id           = project_vars['id_col']
        self.files         = self.vars.f_source()
        self.miss_val_file = os.path.join(self.materials_DIR, "missing_values.json")
        self.run()

    def run(self):
        fs_processed = os.listdir(self.vars.fs_processed_path())
        fs_processed = [i for i in fs_processed if 'long' not in i]
        grid_df    = self.tab.get_df(self.files['grid']['file'])
        grid_ids = grid_df[self.files['grid']['ids']].tolist()

        print(grid_ids)
        print(fs_processed)

        # self.grid_df = self.tab.join_dfs(df, df_fs, how='outer')
        # self.groups = self.preproc.get_groups(self.grid_df[self.project_vars["group_col"]].tolist())
        # self.grid_df.index.name = self._id
        # self.populate_missing_data()
        # self.create_data_file()


    def create_data_file(self):
        file_path_name = os.path.join(self.materials_DIR, self.project_vars["GLM_file_group"])
        print('creating file with groups {}'.format(file_path_name))
        self.tab.save_df(self.grid_df, file_path_name, sheet_name = 'grid')
