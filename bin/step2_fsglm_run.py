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

        # print(ids_fs_grid)

        # self.grid_df = self.tab.join_dfs(df, df_fs, how='outer')
        # self.groups = self.preproc.get_groups(self.grid_df[self.project_vars["group_col"]].tolist())
        # self.grid_df.index.name = self._id
        # self.populate_missing_data()
        # self.create_data_file()

    def find_correspondance(self):
        '''ids in the grid are different from ids that were processed with freesurfer
            extract all processed ids that match the grid ids
            for each ids extract the values of whole hippocampus
            chk the values with the values present in the grid file
            retain the processed ids based on those values
        '''
        ids_fs_grid = dict()
        self.grid_ids = self.grid_df[self.files['grid']['ids']].tolist()
        print(self.grid_df['wholeBrainstem_Brainstem'])
        # fs_proc_proc = self.get_fs_processed_processed()
        # for _id in self.grid_ids:
        #     fs_proc_id = _id.replace('A','').lower()
        #     if fs_proc_id in fs_processed:
        #         ids_fs_grid[fs_proc_id] = fs_processed[fs_proc_id]
        #     else:
        #         ids_fs_grid[fs_proc_id] = list()
        #         miss.append(fs_proc_id)
            # d = self.populate_dict(d, i, proc_id)
        # print(ids_fs_grid)


    def get_fs_processed_processed(self):
        '''extracting processed ids from the main processed folder
            based on grid_ids
        '''
        d = dict()
        fs_processed = os.listdir(self.vars.fs_processed_path()['processed'])
        for _id in self.grid_ids:
            for i in fs_processed:
                if _id in i:
                    d = self.populate_dict(d, _id, i)
        print(d)
        return d


    def populate_dict(self, d, cle, val):
        if cle not in d:
            d[cle] = list()
        else:
            if not val.endswith('.mat'):
                d[cle].append(val)
        print(d)
        return d

    def create_data_file(self):
        file_path_name = os.path.join(self.materials_DIR, self.project_vars["GLM_file_group"])
        print('creating file with groups {}'.format(file_path_name))
        self.tab.save_df(self.grid_df, file_path_name, sheet_name = 'grid')

    # def get_fsprocessed_from_project(self):
    #     '''extracting processed ids from the "Brain_training" folder
    #         script not used, because multiple ids are missing, and other ids
    #         are not present in the main grid file.
    #     '''
    #     grid_ids_to_proc = {}
    #     for _id in self.grid_ids:
    #         fs_proc_id = _id.replace('A','').lower()
    #         grid_ids_to_proc[fs_proc_id] = _id
    #     print(grid_ids_to_proc)

    #     fs_processed_proj = os.listdir(self.vars.fs_processed_path()['project'])
    #     processed_proj = [i for i in fs_processed_proj if 'long' in i]
    #     d = dict()
    #     for _id_long in processed_proj:
    #         _id_proc = _id_long.split('.')[0]
    #         if _id_proc[:4] in grid_ids_to_proc:
    #             d = self.populate_dict(d, grid_ids_to_proc[_id_proc[:4]], _id_proc)
    #         else:
    #             print('not in grid ids:', _id_proc)
    #     return d
