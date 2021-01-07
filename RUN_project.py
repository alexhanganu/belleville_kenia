# !/usr/bin/env python
# coding: utf-8
# last update: 20210102
project = "belleville_kenia"

STEP0_make_groups        = True


from os import path, system
from bin import nimb_link
NIMB_HOME = nimb_link.link_with_nimb()
from setup.get_vars import Get_Vars, SetProject
from stats.db_processing import Table
from stats.preprocessing import get_groups
from distribution import utilities as utils
all_vars = Get_Vars()
project_vars = all_vars.projects[project]
#nimb_stats = SetProject(all_vars.location_vars['local']['NIMB_PATHS']['NIMB_tmp'], all_vars.stats_vars, project).stats

if STEP0_make_groups:
    from bin.step1_make_groups import MakeGroupFile
    MakeGroupFile(project_vars, utils, Table, get_groups)
 
# if STEP1_prep1_fs711_dir:
#     from bin import step1_prep1_fs711_dir
#     step1_prep1_fs711_dir.CleanFS711Dir(NIMB_HOME, path_derivatives_fs7, path_derivatives_fs7_from6, path2xtrct, path_err)

# if STEP1_prep2_fs_processed:
#     from bin import step1_prep2_fs_processed
#     step1_prep2_fs_processed.LinkIDstoProcessed(project_vars)


# if STEP3_run_stats:
#     chdir(NIMB_HOME)
#     system('python3 nimb.py -process run-stats -project {}'.format(project))


