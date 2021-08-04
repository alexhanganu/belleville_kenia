#!/bin/python
# -*- coding: utf-8 -*-
#Alexandru Hanganu, 20200107

''' Read the source file with data
    extract corresponding variables
    checks all variables
    populate missing variables
    excludes columns or subjects from analysis
Args:
    project variables (nimb style), and Table (from nimb)
Return:
    create the grid database (csv or xlsx)
    True or False if all steps are correct and finished
'''

import os
import sys
from .vars import VARS


class MakeGroupFile:

    def __init__(self, project_vars, Table, Preprocess, load_json, rois = False):
        self.tab           = Table()
        self.preproc       = Preprocess()
        self.load_json     = load_json
        self.project_vars  = project_vars
        self.materials_DIR = self.project_vars["materials_DIR"][1]
        self.vars          = VARS(project_vars)
        self._id           = project_vars['id_col']
        self.files         = self.vars.f_source()
        self.miss_val_file = os.path.join(self.materials_DIR, "missing_values.json")
        self.rois          = rois
        self.run()


    def run(self):
        df    = self.get_source_data()
        df_fs = self.get_freesurfer_data()
        if self.rois:
            df_fs = self.make_rois_grid()
        self.grid_df = self.tab.join_dfs(df, df_fs, how='outer')
        self.groups = self.preproc.get_groups(self.grid_df[self.project_vars["group_col"]].tolist())
        self.grid_df.index.name = self._id
        self.populate_missing_data()
        self.create_data_file()


    def make_rois_grid(self):
        print("    making rois grid")
        fs_rois = self.rois()
        df_fs   = self.get_freesurfer_data()
        return df_fs


    def populate_missing_data(self):
        """Some values are missing. If number of missing values is lower then 5%,
            missing values are changed to group mean
            else: columns is excluded
        """
        self.populate_exceptions()
        _, cols_with_nans = self.tab.check_nan(self.grid_df, self.miss_val_file)
        df_groups = dict()
        for group in self.groups:
            df_group = self.tab.get_df_per_parameter(self.grid_df, self.project_vars['group_col'], group)
            df_group = self.preproc.populate_missing_vals_2mean(df_group, cols_with_nans)
            df_groups[group] = df_group
        frames = (df_groups[i] for i in df_groups)
        df_meaned_vals = pd.concat(frames, axis=0, sort=True)
        for col in cols_with_nans:
            self.grid_df[col] = df_meaned_vals[col]


    def populate_exceptions(self):
        exceptions = self.vars.values_exception()
        for ix in exceptions:
            for col in exceptions[ix]:
                self.grid_df.at[ix, col] = exceptions[ix][col]


    def rois(self):
        f_rois = self.files['rois']['file']
        if os.path.exists(f_rois):
            rois = self.load_json(f_rois)
            return [i for k in rois.values() for i in k]
        else:
            print(f"    file with rois is missing: {f_rois}")
            sys.exit(0)


    def get_source_data(self):
        src_file    = self.files['source']
        return = self.tab.get_df(src_file['file'],
                                src_file['sheet'],
                                src_file['cols'],
                                src_file['ids'])


    def get_freesurfer_data(self):
        src_fs_file = self.files['freesurfer']
        return = self.tab.get_df(src_fs_file['file'],
                                src_fs_file['sheet'],
                                src_fs_file['cols'],
                                src_fs_file['ids'])


    def create_data_file(self):
        file_path_name = os.path.join(self.materials_DIR, self.project_vars["GLM_file_group"])
        print('creating file with groups {}'.format(file_path_name))
        self.tab.save_df(self.grid_df, file_path_name, sheet_name = 'grid')
