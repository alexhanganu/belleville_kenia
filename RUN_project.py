# !/usr/bin/env python
# coding: utf-8
# last update: 20210730

import os
import argparse

class RUNProject:

    def __init__(self, all_vars):
        self.project      = all_vars.params.project
        self.vars_local   = all_vars.location_vars['local']
        self.project_vars = all_vars.projects[self.project]
        self.get_steps(all_vars)


    def run(self):
        print("running")
        for step in self.steps:
            step2run = self.steps[step]['name']
            if self.steps[step]["run"]:
                print(f"    running step: {step2run}")
                self.run_step(step2run)


    def run_step(self, step2run):
        if step2run == "STEP0_make_groups":
            from bin.step1_make_groups import MakeGroupFile
            MakeGroupFile(self.project_vars, Table, Preprocess)

        if step2run == "STEP1_run_fsglm":
            FS_SUBJECTS_DIR = all_vars.location_vars['local']['FREESURFER']['FS_SUBJECTS_DIR']
            from bin.step2_fsglm_run import FSGLMrun
            ready = FSGLMrun(self.project_vars, self.vars_local, save_json, Table, manage_archive, FS_SUBJECTS_DIR)
            if ready:
                print('ready for FreeSurfer GLM')
                os.chdir(NIMB_HOME)
                os.system('python3 nimb.py -process fs-glm -project {}'.format(self.project))
            else:
                print('    file for GLM is not ready')

        if step2run == "STEP2_extract_fsglm_img":
            print('ready to extract FreeSurfer GLM images')
            os.chdir(NIMB_HOME)
            os.system('python3 nimb.py -process fs-glm-image -project {}'.format(self.project))

        if step2run == "STEP3_ger_ROIs_grid":
            print('    ready to create ROIs grid')
            from bin.step1_make_groups import MakeGroupFile
            MakeGroupFile(self.project_vars,
                            Table,
                            Preprocess,
                            rois = True)


    def get_steps(self, all_vars):
        self.steps = {
            "0": {"name" : "STEP0_make_groups",
                "run" : False},
            "1": {"name" : "STEP1_run_fsglm",
                "run" : False},
            "2": {"name" : "STEP2_extract_fsglm_img",
                "run" : False},
            "3": {"name" : "STEP3_ger_ROIs_grid",
                "run" : False},
        }
        if all_vars.params.step == 00:
            for i in (0, 1, 2, 3, 4):
                self.steps[i]["run"] = True
        else:
            self.steps[all_vars.params.step]["run"] = True


def get_parameters(project):
    """get parameters for nimb"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Documentation at https://github.com/alexhanganu/nimb
            """,
    )

    parser.add_argument(
        "-step", required=True,
        default='4',
        choices = ['00', '0', '1', '2', '3'],
        help="choice ; 00 = run all steps \
                0 = make groups;\
                1 = run fsglm;\
                2 = extract fsglm images;\
                3 = redo grid with ROIs",
    )

    parser.add_argument(
        "-project", required=False,
        default=project,
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

    params   = get_parameters(project)
    all_vars = Get_Vars(params)

    # from pathlib import Path
    # top = Path(__file__).resolve().parents[1]
    # sys.path.append(str(top))

    RUNProject(all_vars).run()
