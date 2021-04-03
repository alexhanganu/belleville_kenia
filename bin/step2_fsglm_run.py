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
    def __init__(self, project_vars,
                utils, Table, Preprocess,
                manage_archive, FS_SUBJECTS_DIR,
                all_data):
        self.tab            = Table()
        self.preproc        = Preprocess()
        self.SUBJECTS_DIR   = FS_SUBJECTS_DIR
        self.Zip            = manage_archive.ZipArchiveManagement
        self.fs_definitions = all_data
        self.project_vars   = project_vars
        self.materials_DIR  = self.project_vars["materials_DIR"][1]
        self.vars           = VARS(project_vars)
        self._id            = project_vars['id_col']
        self.files          = self.vars.f_source()
        self.col_fs_proc    = 'fs_id'
        self.run()

    def run(self):
        grid_df = self.tab.get_df(os.path.join(self.materials_DIR, self.project_vars["fname_groups"]))

        if self.col_fs_proc in grid_df.columns:
            return True
        else:
            self.grid_df = self.tab.get_df(self.files['grid']['file'])
            ready, _ids_fsproc = self.get_fs_processed()
            if ready:
                d_ids = {self.files['grid']['ids']: [i for i in list(_ids_fsproc.keys())],
                         self.col_fs_proc: [i[0].replace('.zip','') for i in list(_ids_fsproc.values())]}
                fs_proc_df = self.tab.create_df_from_dict(d_ids)
                fs_proc_df = self.tab.change_index(fs_proc_df, self.files['grid']['ids'])
                grid_fs_df_pre = self.tab.change_index(self.grid_df, self.files['grid']['ids'])
                self.grid_df = self.tab.join_dfs(grid_fs_df_pre, fs_proc_df, how='outer')
                # _id_fsproc = self.extract_fs_proc()
                return self.create_data_file()
            else:
                return False

    def extract_fs_proc(self):
        '''fs processed are zipped
            this will unzip the surf and label folders
        '''
        for _id_zipped in [i[0] for i in _ids_fsproc.values()]:
            _id_in_subj_dir = (os.path.join(self.SUBJECTS_DIR, _id_zipped.replace('.zip','')))
            if not os.path.exists(_id_in_subj_dir):
                print(_id_zipped,' missing')
                zip_file_path = (os.path.join(self.vars.fs_processed_path(), _id_zipped))
                dirs2xtrct = ['surf', 'label']
                self.Zip(zip_file_path, path2xtrct = self.SUBJECTS_DIR, dirs2xtrct = dirs2xtrct)
                if not os.path.exists(_id_in_subj_dir):
                    print(_id_zipped,' not extracted')
            else:
                print(_id_zipped,' ready for FS glm')
        return True


    def get_fs_processed(self):
        '''use ids from the grid_ids
           extract processed ids from the FreeSurfer processed folder
           parameters present in the name: presence of WM, absence of T2, absence of T1B
        '''
        _id_fsproc = dict()
        fs_processed_all = os.listdir(self.vars.fs_processed_path())
        grid_ids = self.grid_df[self.files['grid']['ids']].tolist()
        for _id in grid_ids:
            for i in fs_processed_all:
                if _id in i and 'WM' in i and 'T2' not in i and 'T1B' not in i:
                    _id_fsproc = self.populate_dict(_id_fsproc, _id, i)
        missing = [i for i in _id_fsproc if not _id_fsproc[i]]
        if missing:
            print('missing IDs:', len(missing), missing)
            return False, missing
        else:
            return True, _id_fsproc


    def populate_dict(self, d, cle, val):
        if cle not in d:
            d[cle] = list()
        if val not in d[cle]:
            d[cle].append(val)
        return d

    def create_data_file(self):
        file_path_name = os.path.join(self.materials_DIR, self.project_vars["fname_groups"])
        print('creating file with groups {}'.format(file_path_name))
        self.tab.save_df(self.grid_df, file_path_name, sheet_name = 'grid')
        return True


    # def get_ROI(self):
    #     '''written with the intent to search for the right ids based on 
    #         the values of ROIs. Now ids are taken based on present of 'WM' in their names
    #         Script is NOT needed anymore
    #     '''
    #     ROIs = {'nimb_ROI' : 'wholeBrainstem_Brainstem',
    #             'FS_ROI'   : 'Whole_brainstem',
    #             'stats_file': 'brainstemSsVolumes.v10.txt'}
    #             #     stats_file = ROIs['stats_file']
    #         _id_fsproc_roival = dict()
    #         for _id in list(_id_fsproc.keys())[:3]:
    #             _id_fsproc_roival[_id] = dict()
    #             for proc_id in _id_fsproc[_id]:
    #                 zip_file_path = (os.path.join(self.vars.fs_processed_path(), proc_id))
    #                 dirs2xtrct = [os.path.join("mri", stats_file)]
    #                 self.Zip(zip_file_path, path2xtrct = self.SUBJECTS_DIR, dirs2xtrct = dirs2xtrct)
    #                 stats_f = (os.path.join(self.SUBJECTS_DIR, proc_id, dirs2xtrct[0]))
    #                 if os.path.exists(stats_f):
    #                     content = open(stats_f, 'r').readlines()
    #                     for ROI in content:
    #                         if ROI.split(' ')[0] == ROIs['FS_ROI']:
    #                             ROI_val = float(ROI.split(' ')[-1].strip('\n'))
    #                             _id_fsproc_roival[_id][proc_id] = ROI_val
    #                 else:
    #                     print(proc_id, ' NO file ', stats_file)
    #                     pass
    #     print(_id_fsproc_roival)

    # def get_fs_processed(self):
    #     '''extracting processed ids from the main processed folder
    #         based on grid_ids
    #         script is not used because it was written on the wrong dataset
    #     '''
    #     _id_fsproc = dict()
    #     fs_processed_all = os.listdir(self.vars.fs_processed_path())
    #     for _id in self.grid_ids:
    #         for i in fs_processed_all:
    #             if _id in i:
    #                 _id_fsproc = self.populate_dict(_id_fsproc, _id, i)
    #     # print(_id_fsproc)
    #     return _id_fsproc


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
