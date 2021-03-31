# !/usr/bin/env python
# coding: utf-8
# last update: 20210102

project = "belleville_kenia"

STEP0_make_groups        = False
STEP1_run_fslgm          = True

from os import path, system
from bin import nimb_link
NIMB_HOME = nimb_link.link_with_nimb()
from setup.get_vars import Get_Vars, SetProject
from stats.db_processing import Table
from stats.preprocessing import Preprocess
from distribution import utilities as utils
from distribution import manage_archive
from processing.freesurfer.fs_definitions import all_data
all_vars = Get_Vars()
project_vars = all_vars.projects[project]
#nimb_stats = SetProject(all_vars.location_vars['local']['NIMB_PATHS']['NIMB_tmp'], all_vars.stats_vars, project).stats

if STEP0_make_groups:
    from bin.step1_make_groups import MakeGroupFile
    MakeGroupFile(project_vars, utils, Table, Preprocess)

if STEP1_run_fslgm:
	FS_SUBJECTS_DIR = all_vars.location_vars['local']['FREESURFER']['FS_SUBJECTS_DIR']
	from bin.step2_fsglm_run import FSGLMrun
	FSGLMrun(project_vars, utils, Table, Preprocess, manage_archive, FS_SUBJECTS_DIR, all_data)