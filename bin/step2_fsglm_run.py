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
        self.run()

    def run(self):
        self.grid_df = self.tab.get_df(self.files['grid']['file'])
        ids_fs_grid  = self.find_correspondance()

        print(ids_fs_grid)

        # self.grid_df = self.tab.join_dfs(df, df_fs, how='outer')
        # self.groups = self.preproc.get_groups(self.grid_df[self.project_vars["group_col"]].tolist())
        # self.grid_df.index.name = self._id
        # self.populate_missing_data()
        # self.create_data_file()

    def find_correspondance(self):
        '''ids in the grid are different from ids that were processed with freesurfer
            script finds the correspondance
        '''
        ids_fs_grid = dict()
        miss = list()
        grid_ids = self.grid_df[self.files['grid']['ids']].tolist()
        fs_processed = self.get_fs_processed_classified(grid_ids)
        for _id in grid_ids:
            fs_proc_id = _id.replace('A','').lower()
            if fs_proc_id in fs_processed:
                ids_fs_grid[fs_proc_id] = fs_processed[fs_proc_id]
            else:
                ids_fs_grid[fs_proc_id] = list()
                miss.append(fs_proc_id)
        # print(ids_fs_grid)
        # print(miss)


    def get_fs_processed_classified(self, grid_ids):
        d = dict()
        fs_processed = os.listdir(self.vars.fs_processed_path())
        # print(fs_processed)
        for i in grid_ids:
            for proc_id in fs_processed:
                if i in proc_id:
                    d = self.populate_dict(d, i, proc_id)
        for key in d:
            if len(d[key]) > 1:
                print(key, d[key])
        '''first script was written on data from the Brarin_training folder
            but multiple ids were missing from that folder,
            this meant that the main processed folder must be used anyway
        '''
        # for i in [i for i in fs_processed if 'long' in i]:
        #     long_ids = i.split('.')
        #     id_long = long_ids[-1]
        #     if id_long not in d:
        #         d[id_long] = list()
        #         d[id_long].append(long_ids[0])
        #     else:
        #         d[id_long].append(long_ids[0])
        # print(d)
        return d

    def populate_dict(self, d, i, val):
        if i not in d:
            d[i] = list()
        else:
            if not val.endswith('.mat'):
                d[i].append(val)
        return d

    def create_data_file(self):
        file_path_name = os.path.join(self.materials_DIR, self.project_vars["GLM_file_group"])
        print('creating file with groups {}'.format(file_path_name))
        self.tab.save_df(self.grid_df, file_path_name, sheet_name = 'grid')
