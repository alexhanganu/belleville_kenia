#!/bin/python

from os import path, environ, listdir
import sys
from pathlib import Path

def get_home_dir():
    if sys.platform == 'win32':
        return environ['USERPROFILE']
    else:
        return environ['HOME']

def get_Nimb_Home():
    home = get_home_dir()
    f = '{}/credentials'.format(home)
    if path.exists(f):
        return str(open(f).readlines()[0]).strip('\n').replace("~",home)
    else:
        return define_credentials()

def define_credentials():
    cred_path = input('please provide the path where nimb is installed:')
    while not path.exists(cred_path):
        cred_path = input('path does not exist. Pleaes provide the path where nimb is installed:')
    NIMB_HOME = cred_path.replace("~", get_home_dir())
    if 'nimb.py' in listdir(NIMB_HOME):
        NIMB_HOME = NIMB_HOME
    elif 'nimb.py' in listdir(path.join(NIMB_HOME, 'nimb')):
        NIMB_HOME = path.join(NIMB_HOME, 'nimb')
    save_to_file(NIMB_HOME, path.join(get_home_dir(), 'credentials'))
    return NIMB_HOME

def link_with_nimb():
    NIMB_HOME = get_Nimb_Home()
    file = Path(path.join(NIMB_HOME, "nimb.py")).resolve()
    parent, top = file.parent, file.parents[0]
    print(top)
    sys.path.append(str(top))
    return NIMB_HOME

def save_to_file(cred_path, file):
    with open(file, 'w') as f:
        f.write(cred_path)

