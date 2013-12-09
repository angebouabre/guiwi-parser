#!/usr/bin/env python
#-*-encoding:utf-8-*-


#Value to check to have the global result of test in wrs file
GLOBAL_RESULT = "RETURN=0"

#In wrs file, if these codes are not in SCENARIO DL_RETURN, that's means it's a failed scenario
SUCCESS_CODE_1 = "=0"
SUCCESS_CODE_2 = "=-201"

#Full path to the folder where parser get the wrs files, direct parent folder of version folder
RAW_RESULTS_DIR = "/home/bouable/sfr-workspace/raw-ws"

#Full path to the folder where parser push the json format fixture. It will be generated.
FIXTURE_DIR = "/home/bouable/sfr-workspace/guiwi/witbe/stbattack/fixture"

#Full path to the log folder
LOG_DIR = '/home/bouable/sfr-workspace/guiwi-parser/log' 
