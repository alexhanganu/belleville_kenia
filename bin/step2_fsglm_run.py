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
    def __init__(self, project_vars, utils, Table, Preprocess, manage_archive):
        self.tab           = Table()
        self.preproc       = Preprocess()
        self.Zip           = manage_archive.ZipArchiveManagement
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
        # ids_fs_grid = dict()
        self.grid_ids = self.grid_df[self.files['grid']['ids']].tolist()
        # ROI_grid = self.grid_df[self.get_ROI()['nimb_ROI']].tolist()
        _id_fsproc_roival = self.get_ROIs_ids()
        # for _id in list(_id_fsproc_roival.keys()):#[:3]:
        #     for proc_id in _id_fsproc_roival[_id]:
        #         proc_val = _id_fsproc_roival[_id][proc_id]
        #         # print(_id, _id_fsproc_roival[_id], proc_val)
        #         if proc_val in ROI_grid:
        #             print('yes', proc_val)
        #         else:
        #             print('NO', proc_val)


        # fs_processed = self.get_fs_processed()
        # for _id in self.grid_ids:
        #     fs_proc_id = _id.replace('A','').lower()
        #     if fs_proc_id in fs_processed:
        #         ids_fs_grid[fs_proc_id] = fs_processed[fs_proc_id]
        #     else:
        #         ids_fs_grid[fs_proc_id] = list()
        #         miss.append(fs_proc_id)
            # d = self.populate_dict(d, i, proc_id)
        # print(ids_fs_grid)

    def get_ROIs_ids(self):
        _id_fsproc = self.extract_fs_proc()
        # stats_file = self.get_ROI()['stats_file']
        # _id_fsproc_roival = dict()

        # for _id in list(_id_fsproc.keys()):#[:3]:
        #     _id_fsproc_roival[_id] = dict()
        #     for proc_id in _id_fsproc[_id]:
        #         stats_roi = (os.path.join(self.vars.fs_processed_path(),
        #                                   proc_id, "mri", stats_file))
        #         if os.path.exists(stats_roi):
        #             content = open(stats_roi, 'r').readlines()
        #             for ROI in content:
        #                 if ROI.split(' ')[0] == self.get_ROI()['FS_ROI']:
        #                     ROI_val = float(ROI.split(' ')[-1].strip('\n'))
        #                     _id_fsproc_roival[_id][proc_id] = ROI_val
        #         else:
        #             pass
        #             # print(proc_id, ' NO file ', stats_file)
        # # print(_id_fsproc_roival)
        # return _id_fsproc_roival

    def get_ROI(self):#medulla_Brainstem', 'pons_Brainstem', 'scp_Brainstem'
        return {'nimb_ROI' : 'wholeBrainstem_Brainstem',
                'FS_ROI'   : 'Whole_brainstem',
                'stats_file': 'brainstemSsVolumes.v10.txt'}

    def extract_fs_proc(self):
        '''fs processed are zipped
            this will unzip the surf and label folders
        '''
        ready, _id_fsproc = self.get_fs_processed()
        if ready:
            for _id_grid in _id_fsproc:
                print(_id_fsproc[_id_grid])
            print('ready')
            print(project_vars)
        return True


    def get_fs_processed(self):
        '''use ids from the grid_ids
           extract processed ids from the FreeSurfer processed folder
            
        '''
        _id_fsproc = dict()
        fs_processed_all = os.listdir(self.vars.fs_processed_path())
        # print(fs_processed_all)
        for _id in self.grid_ids:
            for i in fs_processed_all:
                if _id in i:
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
        file_path_name = os.path.join(self.materials_DIR, self.project_vars["GLM_file_group"])
        print('creating file with groups {}'.format(file_path_name))
        self.tab.save_df(self.grid_df, file_path_name, sheet_name = 'grid')

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
