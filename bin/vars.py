#!/bin/python

from os import path, environ, sep
from .nimb_link import get_Nimb_Home, get_home_dir
import pandas as pd
import time
date = str(time.strftime('%Y%m%d', time.localtime()))
import logging

log = logging.getLogger(__name__)
logging.basicConfig(format='%(message)s')
log.setLevel(logging.INFO)

# from datetime import date
# dt = date.today().strftime('%Y%m%d')
# dt=str(datetime.now().year)+str(datetime.now().month)+str(datetime.now().day)

class VARS():
    def __init__(self, project_vars):
        self.home               = get_home_dir()
        self.project_vars       = project_vars
        self.tmp_MR_data_file   = 'tmp/step0_prep1_path_2MR_files.json'
        self.tmp_FSnotprocessed = 'tmp/step0_prep1_fs_scans_notprocessed.json'
        self.f_missing_values   = 'tmp/step0_prep2_values_missing.json'

    def cimaq_projects(self):
        return ['HINT','SEM','WM', 'Substrat', 'Training_ATT', 'CogCtrl', 'Cognition', 'ADVN', 'Plasticity', 'Vasculaire']

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

    def read_xlsx_file(self, path2_file, sheetname, cols, rename=False):
        log.info('    reading file: {},\n    sheet: {}'.format(path2_file, sheetname))
        xls = pd.read_excel(path2_file, sheet_name = sheetname, usecols = cols)
        if rename:
            xls.rename(columns = rename, inplace=True)
        return xls

    def dirsMR(self):
        connect, path2ext = self.external_disk_connected()
        if connect:
            project_dirs = {'HINT': 'Zendel_HINT/dcm', 'SEM':'Frederic_SEM/dcm', 'Substrat':'Stéphanie_Substrat/dcm',
                            'WM':'Nicolas_WM/dcm', 'Training_ATT':'Bianca_Training_ATT/dcm',
                            'CogCtrl':'CogCtrl','Cognition':'Francis_Cognition-structurelle/dcm', 'ADVN':'Chloe_ADVN/dcm',
                            'Plasticity': 'Joni_Plasticity/dcm', 'Vasculaire': 'Sylvie_Vasculaire/format_dcm'}
            return {i: path.join(path2ext, project_dirs[i]) for i in project_dirs}
        else:
            return False

    def path_SUBJECTS_DIR_source(self):
        return 'C:/Users/Jessica/Desktop/db_sylvie_belleville/source'

    def params_other(self):
        return ['Code_Study', 'Code Labo', 'Code_Participant', 'Code_SCAN','SCANNER','NB de cannaux','Année_SCAN','séance longitudinal', 'Doublon']

    def params_demographics(self):
        params_x = ['Age',]
        params_y = ['education','Gender','MOCA',]
        return params_x, params_y


    def get_id_ca(self, ls_id_labo):
        '''Extract IDs from the Code Labo column
           define the id that start with CA and has 3 numbers
        '''
        return {i[:5]:[] for i in ls_id_labo}

    def fs7_data(self, v):
        if v == 7:
            return "{}/datasets/cimaq/bids/derivatives/freesurfer711".format(self.home) #path to data processed with FreeSurfer 7.1.1
        else:
            return "{}/datasets/cimaq/bids/derivatives/freesurfer711_from600".format(self.home) #path to data processed with FreeSurfer 6.0.0 initialy and processed repeatedely with FreeSurfer 7.1.1

    def MRpaths_exceptions(self):
        return {'CogCtrl_CA397_CT_Pre': ['CogCtrl', 'CogCrtl_CA397_CT_Pre'],
                'HINT_Mus_13_Pre': ['HINT', 'Hint_Mus_13_Pre']}

    def external_disk_connected(self):
        connect = False
        disk_path = 'backup_samira/IRM_Structurelle/'
        potential_links = ['E:/', '/media/ssp/Samira_Rouge_structurelle']
        for p in potential_links:
            path2ext = path.join(p, disk_path)
            if path.exists(path2ext):
                connect = True
                break
        return connect, path2ext

    def path_f_clin_FS_data(self):
        return path.join(self.project_vars['materials_DIR'], '3.data_for_analysis_{}'.format(date)).replace(sep, '/')

    def path_f_clin_data(self):
        return path.join(self.project_vars['materials_DIR'], '0.data_clinical_20200306.xlsx').replace(sep, '/')

    def work(self):
        path2xtrct = '{}/tmp'.format(self.home) #path to extract temporary data
        path_err = '{}/tmp_err'.format(self.home) #path to save error data
        return path2xtrct, path_err

    def groups(self):
        return {'BACC':'>=','HS':'<'} #group names: below 16 years = HS (High School), 16 and above = BACC

    def group_thresh(self):
        return 16 #threshold used to define groups = above/below 16 years of education

    def create_groups(self, df, group_param):
        # thresh_for_groups = 16 #threshold used to define groups = above/below 16 years of education
        groups = self.groups()
        thresh = self.group_thresh()
        for group in groups:
            if groups[group] == '>=':
                df_group = df[df[params[group_param]] >= thresh]
            elif groups[group] == '<':
                df_group = df[df[params[group_param]] < thresh]
        return df_group

    def tmp_f_raw_used(self):
        return path.join(self.project_vars['materials_DIR'], "processed_fs600_i_cmd.json").replace(sep, '/')

    def tmp_fs600_dcm_files_used(self):
        return path.join(self.project_vars['materials_DIR'], "processed_fs600_dcm_files.json").replace(sep, '/')

    def tmp_ids_proc(self):
        return path.join(self.project_vars['materials_DIR'], "f_ids_processed.json").replace(sep, '/')

    def long_names(self):
        return ['pre','mid','post', 'T1', 'T2']

    def sex(self):
        return {1:'male', 2:'female'}

    def fs_atlas(self, name):
        if name == 'Destrieux':
            return 'DS'
        elif name == 'Desikan':
            return 'DK'
        else:
            return 'DKDS'

    def processed_exceptions(self):
        return {
            'SEM_CA102'               :'SEM_AD_HC_102_ses-01.zip',
            'SEM_CA119'               :'SEM_AD_HC_119_ses-01.zip',
            'Training_ATT_CA409_MD_T1':'Training_ATT_CA409_MD_T1_ses-01.zip',
            'WM_CA180_LA_T1'          :'WM_CA180_LA_T1_ses-01.zip',
            'WM_CA486_FL_T1'          :'WM_CA486_FL_T1_ses-01.zip',
            }

    def values_exception(self):
        # HINT_Con6_pre has the Age errouneously introduced, same registrations of CA340 give the age 78
        return {
        'HINT_Mus_11_Pre': {'MOCA': 30},
        'SEM_CA112'      : {'MOCA': 30},
        'SEM_CA114'      : {'MOCA': 27},
        'SEM_CA118'      : {'Gender': 1, 'MOCA': 30},
        'WM_CA330_JB3_T1': {'education': 14, 'MOCA': 29},
        'WM_CA256_AR_T1' : {'MOCA': 30}, #because doublons Training_ATT_CA256 has MOCA 30
        'Substrat_C258'  : {'MOCA': ''},
                        }

    def moca_subj_to_average_by_group(self):
        return ['WM_CA183_EDV_T1', 'WM_CA282_HA', 'WM_CA315_GB3_T1',
                'WM_CA323_DM_T1', 'WM_CA327_JC4_T1', 'WM_CA340_JGP_T1',
                'WM_CA424_HA2_T1',
                'HINT_CA327_JC4_Pilote', 'HINT_Con6_pre', 'HINT_Con14_Pre', 'HINT_Con15_Pre',
                'HINT_mus01_Pre=CA391', 'HINT_mus03_pre', 'HINT_mus05_pre', 'HINT_Mus_14_pre',
                'HINT_Vid01_pre',
                'CA149_T2', 'CA183_T2',
                'SEM_CA101', 'SEM_CA107',
                'Substrat_C258']

    def doublons_alternate(self):
        return {
            'CA106': ['SEM_CA106', 'HINT_Con15_Pre'],
            'CA107': ['SEM_CA107', 'CogCtrl_CA431CL2_Pre_V1'],
            'CA109': ['SEM_CA109', 'WM_CA424_HA2_T1'],
            'CA149': ['CA149_T2', 'SEM_CA101'],
            'CA183': ['CA183_T2', 'WM_CA183_EDV_T1'],
            'CA256': ['WM_CA256_AR_T1', 'Training_ATT_CA256_AR_T1'],
            'CA281': ['CA281_DO_Pre', 'CogCtrl_CA281_DO_Pre'],
            'CA293': ['CA293_FC2_Pre', 'Substrat_C293'],
            'CA315': ['Substrat_C315', 'WM_CA315_GB3_T1'],
            'CA323': ['CA323_DM_Pre', 'WM_CA323_DM_T1'],
            'CA324': ['CA324_JT2_Pre', 'HINT_Mus_11_Pre', 'Training_ATT_CA324_JT2_T1'],
            'CA327': ['CA327_JC4_Pre', 'HINT_CA327_JC4_Pilote', 'WM_CA327_JC4_T1'],
            'CA330': ['HINT_Vid01_pre', 'WM_CA330_JB3_T1', 'CA330_JB3_Pre'],
            'CA340': ['CA340_JGP_Pre', 'HINT_Con6_pre','WM_CA340_JGP_T1'],
            'CA386': ['CA386_SB_Pre', 'HINT_mus03_pre'],
            'CA387': ['SEM_CA118', 'WM_CA387_BT_T1', 'CA387_BT_Pre'],
            'CA282': ['CA282_HA_Pre', 'WM_CA282_HA', 'HINT_Con14_Pre'],
            'CA355': ['CA355_LF2_Pre', 'Substrat_C355', 'HINT_Mus_14_pre'],
            'CA374': ['Substrat_C374', 'Training_ATT_CA374_RP_T1'],
            'CA391': ['HINT_mus01_Pre=CA391', 'CogCtrl_CA391_MDL_Pre'],
            'CA397': ['CogCtrl_CA397_CT_Pre', 'Training_ATT_CA397_CT_T1', 'SEM_CA112'],
                        }

    def doublons_alternate_on_age(self):
        return {
            'Training_ATT_CA397_CT_T1': 'CogCtrl_CA397_CT_Pre',
                }

    def doublons_with_alternates(self):
        return {
            'CA149_T2'                : 'doublons de SEM_CA101, younger',
            'CA183_T2'                : 'doublons de WM_CA183_EDV_T1, younger',
            'CA355_LF2_Pre'           : 'doublons de Substrat_C355, HINT_Mus_14_pre, annee 2009',
            'CA281_DO_Pre'            : 'doublons de CogCtrl_CA281_DO_Pre, excluded because annee 2014-2015',
            'CA282_HA_Pre'            : 'doublons de HINT_Con14_Pre, WM_CA282_HA, annee 2009',
            'CA293_FC2_Pre'           : 'doublons de Substrat_C293, younger',
            'CA323_DM_Pre'            : 'doublons de WM_CA323_DM_T1, younger',
            'CA324_JT2_Pre'           : 'doublons de Training_ATT_CA324_JT2_T1, HINT_Mus_11_Pre, mais annees 2009',
            'CA327_JC4_Pre'           : 'doublons de HINT_CA327_JC4_Pilote, WM_CA327_JC4_T1, annee 2009',
            'CA330_JB3_Pre'           : 'doublons de WM_CA330_JB3_T1, HINT_Vid01_pre, mais annees 2009',
            'CA340_JGP_Pre'           : 'doublons de HINT_Con6_pre,  WM_CA340_JGP_T1, younger',
            'CA384_JPB_Pre'           : 'doublons de WM_CA384_JPB_T1, mais annees 2011',
            'CA386_SB_Pre'            : 'doublons de HINT_mus03_pre, mais annees 2011',
            'CA387_BT_Pre'            : 'doublons de WM_CA387_BT_T1, mais annees 2011',
            'HINT_CA327_JC4_Pilote'   : 'doublons de CA327_JC4_Pre, WM_CA327_JC4_T1, annee 2009',
            'HINT_Con6_pre'           : 'doublons de CA340_JGP_Pre,  WM_CA340_JGP_T1, younger',
            'HINT_Vid01_pre'          : 'doublons de WM_CA330_JB3_T1, CA330_JB3_Pre, mangue MOCA',
            'HINT_mus01_Pre=CA391'    : 'doublons de CogCtrl_CA391_MDL_Pre, excluded because year 2014-2015',
            'HINT_Mus_11_Pre'         : 'doublons de Training_ATT_CA324_JT2_T1, CA324_JT2_Pre',
            'SEM_CA106'               : 'doublons de  HINT_Con15_Pre, annee 2012 vs 2013',
            'SEM_CA107'               : 'doublons de CogCtrl_CA431CL2_Pre_V1, annee 2012 vs 2018',
            'SEM_CA109'               : 'doublons de  WM_CA424_HA2_T1, annee 2012 vs 2013',
            'SEM_CA112'               : 'doublons de CogCtrl_CA397_CT_Pre, annee 2012 vs 2018',
            'SEM_CA114'               : 'doublons de HINT_mus05_pre, annee 2012 vs 2014',
            'SEM_CA118'               : 'doublons de WM_CA387_BT_T1, annee 2012 vs 2014',
            'WM_CA256_AR_T1'          : 'doublons de  Training_ATT_CA256_AR_T1, mangue MOCA',
            'WM_CA282_HA'             : 'doublons de HINT_Con14_Pre, CA282_HA_Pre, annee 2009',
            'Substrat_C315'           : 'doublons de WM_CA315_GB3_T1, annees 2009',
            'Substrat_C355'           : 'doublons de CA355_LF2_Pre, HINT_Mus_14_pre, annee 2009',
            'Substrat_C374'           : 'doublons de Training_ATT_CA374_RP_T1, excluded because year 2010',
                }

    def doublons_excluded(self):
        return {
            'CA291_LGI_Pre'        : 'doublons de WM_CA291_LGL_T1, MOCA 23',
            'WM_CA291_LGL_T1'      : 'doublons de CA291_LGI_Pre, MOCA 23',
            'CA150_T2'             : 'doublons de CA150_AB_Pre, manque MOCA',
            'CA232_MH3_Pre'        : 'doublons de WM_CA232_MH3_T1, MOCA 25',
            'CA256_T2'             : 'doublons de Training_ATT_CA256_AR_T1, manque MOCA, annee 2009',
            'WM_CA417_DRL_T1'      : 'doublons de Training_ATT_CA417_DRL_T1, manque MOCA',
            'WM_CA232_MH3_T1'      : 'doublons de CA232_MH3_Pre, MOCA 25',
            'HINT_con03_pre'       : 'doublons de Training_ATT_CA447_LR6_T1, manque MOCA',
            'HINT_Mus_13_Pre'      :'probably not processed with fs711',
            'HINT_Mus15_Pre'       : 'doublons de Training_ATT_CA416_CD5_T1, manque MOCA',
            'SEM_CA119'            : 'doublons de CA388_AG4_Pre, manque MOCA',
            'Substrat_C258'        : 'doublons de WM_CA258_AS_T1, annees 2009',
            'Substrat_C335'        : 'doublons de CA335_DSP_Pre, Moca 25',
            'Vasculaire_CAS215_MR2': 'doublons de WM_CA215_MR2_T1, manque tous',
            'Vasculaire_CAS234_VL' : 'doublons de CA234_T2, manque tous',
            'Vasculaire_CAS232_MH' : 'doublons de WM_CA232_MH3_T1, CA232_MH3_Pre, manque tous',
            'Vasculaire_CAS265_RL' : 'doublons de CA265_T2, CA232_MH3_Pre, manque tous',
            'Vasculaire_CAS208_SL2': 'manque tous',
            'Vasculaire_CAS223_AG' : 'manque tous',
            'Vasculaire_CAS235_MM4': 'manque tous',
            'Vasculaire_CA288_MB'  : 'manque tous',
            'Vasculaire_CA305_GP'  : 'manque tous',
                                }
'''
Was used for a previous version script. Will be removed probably because the reason of excluding subjects is missing
    subjs_excluded on first analysis but kept on current analysis
        'CA149_T2', 'CA150_T2', 'CA183_T2', 
            'CA232_MH3_Pre', 'CA252', 'CA256_T2', 
            'CA282_HA_Pre', 'CA291_LGI_Pre', 'CA291_LGL_T1', 'CA293', 
            'CA304', 'CA315', 'CA323_DM_Pre', 'CA324_JT2', 'CA324_JT2_Pre', 
            'CA327_JC4_Pilote_HINT', 'CA327_JC4_Pre', 'CA330_JB3', 'CA330_JB3_Pre', 
            'CA340_JGP', 'CA340_JGP_Pre', 'CA344', 'CA350', 'CA351', 'CA352', 'CA355', 
            'CA355_LF2_Pre', 'CA357', 'CA359', 'CA363_YC2_Pre', 'CA373', 'CA374', 'CA375', 
            'CA376', 'CA378', 'CA379', 'CA380', 'CA381', 'CA384_JPB_Pre', 'CA386_SB_Pre', 'CA387_BT', 
            'CA387_BT_Pre', 'CA388_AG4_Pre', 'CA391_MDL_Pre', 'CA397_CT', 'CA397_CT_Pre', 'CA410_CE_T1', 
            'CA416_CD5', 'CA424_HA2', 'CA431CL2_Pre_V1', 'CA441_GR3', 'CA442_LT', 'CA444_MCM', 
            'CA445_NB', 'CA447_LR6', 'CA464_JB4_T1', 'CA490_AP3_T1', 'CA491_DB4', 'CA523_NP3_Pre']
'''

'''
    def name_exceptions(self):
        return {
            "CA152_T2":"Cognition2_CA152_MP",
            "CA234_T2":"Cognition2_CA234_VL",
            "CA257_T2":"Cognition2_CA257_MD",
            "CA265_T2":"Cognition2_CA26_RL",
            "CA271_T2":"Cognition2_CA271_JPM",
            "CA278_T2":"Cognition2_CA278_MT",
            "CA319_RM2_Pre":"ADVN_C319_RM2_Pre",
            "CA383_AL2_Pre":"ADVN_CA383_AL2_VA_Pre",
            "CA389_MF_pre":"ADVN_CA389_MF_VB_Pre",
            "HINT_con02_pre":"HINT_Con_2",
            "HINT_con04_pre":"HINT_Pre_con4",
            "HINT_Con11_pre":"HINT_CON11_pre",
            "HINT_mus01_Pre=CA391":"HINT_CA391_MDL_Pre",
            "HINT_mus03_pre":"HINT_Mus_3_Pre",
            "HINT_mus04_pre":"HINT_Mus_4",
            "HINT_MUS07_pre":"HINT_MUS_7",
            "HINT_Mus10_Pre_plusdevol":"HINT_Mus10_Pre",
            "HINT_Vid_06_pre":"HINT_Vid_6_pre",
            "HINT_Vid_07_pre":"HINT_Vid_7_pre",
            "HINT_Vid04_pre":"HINT_Vid4",
            "HINT_vid05_pre":"HINT_vid5",
            "HINT_Vid08_Pre":"HINT_Vil8_Pre",
            "SEM_CA101":"Sem_AD_HC_101",
            "SEM_CA102":"Sem_AD_HC_102",
            "SEM_CA103":"Sem_AD_HC_103",
            "SEM_CA104":"SEM_AD_HC_104",
            "SEM_CA105":"SEM_AD_HC_105",
            "SEM_CA106":"Sem_AD_HC_106",
            "SEM_CA107":"Sem_AD_HC_107",
            "SEM_CA108":"Sem_AD_HC_108",
            "SEM_CA110":"SEM_AD_HC_110",
            "SEM_CA111":"SEM_AD_HC_111",
            "SEM_CA113":"SEM_AD_HC_113",
            "SEM_CA114":"SEM_AD_HC_114",
            "SEM_CA115":"SEM_AD_HC_115",
            "SEM_CA116":"SEM_AD_HC_116",
            "SEM_CA119":"Sem_AD_HC_119",
            "WM_CA384_JPB_T1":"CA384_JPB_WM_T1",
            "WM_CA392_MR3_T1":"Plasticity_WM_MR",
            "Training_ATT_CA374_RP_T1":"Training_ATT_CA_RP_T1",
            "Training_ATT_CA447_LR6_T1":"Training_ATT_CA447_LR6_T3-0001.dcm",
            "WM_CA144_CK_T1":"WM_CA144_NM_T1-0106.dcm",
            "WM_CA212_CD3_T1_CA214":"WM_CA212_CD3_T1-0001.dcm",
            "WM_CA466_RF_T1":"WM_CA486_FL_T1-0001.dcm",
            }
'''
