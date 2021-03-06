# !/usr/bin/env python
# coding: utf-8
# last update: 20210102

project = "belleville_kenia"

STEP0_make_groups        = False
STEP1_run_fslgm          = True

from bin import nimb_link
NIMB_HOME = nimb_link.link_with_nimb()
from setup.get_vars import Get_Vars, SetProject
from stats.db_processing import Table
from stats.preprocessing import Preprocess
from distribution.utilities import save_json
from distribution import manage_archive

all_vars = Get_Vars()
local_vars   = all_vars.location_vars["local"]
project_vars = all_vars.projects[project]
#nimb_stats = SetProject(all_vars.location_vars['local']['NIMB_PATHS']['NIMB_tmp'], all_vars.stats_vars, project).stats

if STEP0_make_groups:
    from bin.step1_make_groups import MakeGroupFile
    MakeGroupFile(project_vars, utils, Table, Preprocess)

if STEP1_run_fslgm:
	FS_SUBJECTS_DIR = all_vars.location_vars['local']['FREESURFER']['FS_SUBJECTS_DIR']
	from bin.step2_fsglm_run import FSGLMrun
	ready = FSGLMrun(project_vars, local_vars, save_json, Table, manage_archive, FS_SUBJECTS_DIR)
	if ready:
		print('ready for FreeSurfer GLM')
		import os
		os.chdir(NIMB_HOME)
		os.system('python3 nimb.py -process fs-glm -project {}'.format(project))
	else:
		print('file for GLM is not ready')
