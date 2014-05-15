#!/usr/bin/env python
#-*-encoding:utf-8-*-
import os

cur_path = os.path.abspath(__file__)
cur_folder = os.path.dirname(cur_path)


#Value to check to have the global result of test in wrs file
GLOBAL_RESULT = "RETURN=0"

#In wrs file, if these codes are not in SCENARIO DL_RETURN, that's means it's a failed scenario
SUCCESS_CODE_1 = "=0"
SUCCESS_CODE_2 = "=-201"

#Full path to the folder where parser get the wrs files, direct parent folder of version folder
RAW_RESULTS_DIR = "/home/bouable/workspace/project/sfr/neufbox-evol/integration/testi/"

#Full path to the folder where parser push the json format fixture. WARNING!!!, It will be generated and may overwrite an existant folder.
FIXTURE_DIR = os.path.join(cur_folder,'fixture') 

#Full path to the log folder
LOG_DIR = os.path.join(cur_folder,'log')  

#Only for dev version
DATABASE = os.path.join(cur_folder, os.pardir, 'guiwi/witbe/ti.db')

#Index position in the path
PROJET_INDEX = 9 
VERSION_INDEX = 10
SCENARIO_INDEX = 2 

#For my Personnal PC
#PROJET_INDEX = 4 
#VERSION_INDEX = 5 
