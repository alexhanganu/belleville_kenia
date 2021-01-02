#!/bin/python

from os import path, environ, sep

class VARS():
    def __init__(self):
        self.materials_dir      = "~/Dropbox/p"

    def f_and_sheets(self):
        f_source = path.join(self.project_vars['materials_DIR'],
                'source','0.data_samira_main_20180614.xlsx').replace(sep, '/')
        f_WM_subj = path.join(self.project_vars['materials_DIR'],
                'source','0.data_samira_sujets_WM_20201125.xlsx').replace(sep, '/')
        f_SEM_subj = path.join(self.project_vars['materials_DIR'],
                'source','0.data_samira_sujets_SEM_20201125.xlsx').replace(sep, '/')
        params_x, params_y = self.params_demographics()
        return {'source':{'file': f_source, 'sheet' : 'ALL_DATA_STRUCTURELLE', 'ids':'Code_SCAN',
                          'cols': params_x+params_y+self.params_other(), 'rename': ''},
                'HINT': {'file': f_source, 'sheet' : 'HINT', 'ids':'Unnamed: 0',
                         'cols':['Unnamed: 0', 'âge au moment scan', 'sexe', 'MOCA'],
                         'rename': {'âge au moment scan': 'Age', 'sexe': 'Gender'}},
                'WM':{'file': f_WM_subj, 'sheet' : 'Feuil1', 'ids':'fMRI_Code',
                      'cols': ['fMRI_Code', 'Age', 'Gender', 'Scol', 'MoCA'],
                      'rename': {'MoCA': 'MOCA', 'Scol': 'education'}},
                'SEM':{'file': f_SEM_subj, 'sheet' : 'Feuille 1 - Tableau 1', 'ids':'',
                       'cols': '', 'rename': ''}}
