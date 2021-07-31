# !/usr/bin/env python
# coding: utf-8
# last update: 20210730

class RUNProject:

	def __init__(self, all_vars):
		

	STEP0_make_groups        = False
	STEP1_run_fslgm          = False
	STEP2_extract_fslgm_img  = True


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

	if STEP2_extract_fslgm_img:
		print('ready to extract FreeSurfer GLM images')
		import os
		os.chdir(NIMB_HOME)
		os.system('python3 nimb.py -process fs-glm-image -project {}'.format(project))



def get_parameters():
    """get parameters for nimb"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Documentation at https://github.com/alexhanganu/nimb
            """,
    )

    parser.add_argument(
        "-step", required=True,
        help="absolute path to MR data to be classified",
    )

    parser.add_argument(
        "-test", required=False,
        default=0,
        help="testing ? (yes = 1 = True) or NOT testing but running (no = 0 = False); default is 0",
    )

    params = parser.parse_args()
    return params


if __name__ == "__main__":

	project = "belleville_kenia"

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

    # from pathlib import Path
    # top = Path(__file__).resolve().parents[1]
    # sys.path.append(str(top))

    params      = get_parameters()
    DCM2BIDS_tester(params, project).run()



