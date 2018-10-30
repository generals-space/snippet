#!/usr/bin/python

from pathlib import Path
import time
import importlib

RootDir = Path.cwd().joinpath(Path(__file__).parent)
import sys, os
if str(RootDir) not in sys.path: sys.path.append(str(RootDir))

sitePath = Path.joinpath(RootDir, 'sites')

try:
    while True:
        sites = os.listdir(str(sitePath))
        for site in sites:
            if site.rfind('.py') == -1: continue
            site = site.split('.')[0]
            mod = importlib.import_module('sites.' + site)
            print(mod.name)
            time.sleep(3)
except KeyboardInterrupt as e:
    print('ctrl + c...')