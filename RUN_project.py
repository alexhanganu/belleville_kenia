# !/usr/bin/env python
# coding: utf-8
# last update: 20210102

STEP0_make_groups        = True
STEP1_prep1_fs711_dir    = False # this step was needed temporarily to clean the FS711 folder. Probably not needed anymore
STEP1_prep2_fs_processed = False
STEP3_run_stats          = False

from os import path, system
from bin.db_processing import Table
from bin.vars import VARS
from bin import nimb_link
NIMB_HOME = nimb_link.link_with_nimb()
from setup.get_vars import Get_Vars, SetProject
all_vars = Get_Vars()
project_vars = all_vars.projects[project]
#nimb_stats = SetProject(all_vars.location_vars['local']['NIMB_PATHS']['NIMB_tmp'], all_vars.stats_vars, project).stats

if STEP0_make_groups:
    from bin.step1_make_groups import MakeGroupFile
    MakeGroupFile()
 
# if STEP1_prep1_fs711_dir:
#     from bin import step1_prep1_fs711_dir
#     step1_prep1_fs711_dir.CleanFS711Dir(NIMB_HOME, path_derivatives_fs7, path_derivatives_fs7_from6, path2xtrct, path_err)

# if STEP1_prep2_fs_processed:
#     from bin import step1_prep2_fs_processed
#     step1_prep2_fs_processed.LinkIDstoProcessed(project_vars)


# if STEP3_run_stats:
#     chdir(NIMB_HOME)
#     system('python3 nimb.py -process run-stats -project {}'.format(project))


