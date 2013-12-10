#!/usr/bin/env python
#-*-encoding:utf-8-*-
""" """

import os
import shutil
import json
from utils import *
from parsersettings import GLOBAL_RESULT, SUCCESS_CODE_1, SUCCESS_CODE_2, FIXTURE_DIR, RAW_RESULTS_DIR

def checkFile(filename):
    """ Check succes of task by global return in task report """
    if os.path.isfile(filename):
        openedFile = open(filename)
        for line in openedFile:
            if GLOBAL_RESULT in line:
                return True
         

def getErrorStep(filename):
    """ Return the scenario's step number of failed task """
    res={}
    openedFile = open(filename)
    for line in openedFile:
        key_field = 'DL_RETURN'
        if key_field in line:
            if SUCCESS_CODE_1 in line:
                pass
            elif SUCCESS_CODE_2 in line:
                pass
            else:
                failed_step = line.split('=')[0].split("N")[1]
                res = {'failed_stp':failed_step, 'filename':filename}
                return res
                    
def getFields(filename, pk):
    """ Get needed fields in task report """
    fields_dict={}
    openedFile = open(filename)
    for line in openedFile:
        if 'ALIAS' in line:
            test_name = line.split('=')[1].rstrip()
        if 'DATE' in line: #To rework because it  gets the last occurence 'DATE' in wrs file
            start_date = line.split('=')[1].rstrip()
    data={"fields":{"scenario_failed":"","error_code":0,"start_date":start_date,"file_report":filename,"test_name":test_name},"model":"stbattack.tasktest","pk":pk}
    if getErrorStep(filename):
        stp_nb = getErrorStep(filename)['failed_stp']
        fields_dict['file_report'] = getErrorStep(filename)['filename'].rstrip()
        openedFile = open(filename)
        for line in openedFile:
            if 'ALIAS' in line:
                fields_dict['test_name'] = line.split('=')[1].rstrip()
            if 'DL_ACTION_%s'%stp_nb in line:
                fields_dict['scenario_failed'] = line.split('=')[1].rstrip()
            if 'DL_ACTIONSTART_%s'%stp_nb in line:
              fields_dict['start_time'] = line.split('=')[1].rstrip()
            if 'DL_ACTIONEND_%s'%stp_nb in line:
              fields_dict['end_time'] = line.split('=')[1].rstrip()
            if 'DL_ACTIONSTARTDATE_%s'%stp_nb in line:
              fields_dict['start_date'] = line.split('=')[1].rstrip()
            if 'DL_RETURN%s'%stp_nb in line:
              fields_dict['error_code'] = int(line.split('=')[1].rstrip())
            if 'capture=video' in line:
                fields_dict['video_report'] = 'https:%s'%(line.split('=https:')[1].rstrip())
        data['fields']=fields_dict
    data = json.dumps(data)
    return str(data) 

def serialize(daily_wrs_dir):
    lines = '' 
    pk = 0 
    for filename in os.listdir(daily_wrs_dir):
        filename = os.path.join(daily_wrs_dir,filename)
        if os.path.isfile(filename):
            pk += 1
            line = getFields(filename, pk)
            lines = line + ',' + lines
            os.remove(filename)
            print "%s deleted."%filename
    "Making a table with the json data like django fixture"
    lines = '['+lines+']'
    "SERIALIZING: Clean the the table in compliance with django fixture "
    lines = lines.replace("},]","}]")
    lines = lines.replace(",{}","")
    lines = lines.replace("{},","")
    
    if not os.path.isdir(FIXTURE_DIR):
        os.makedirs(FIXTURE_DIR)
    fixture_file = os.path.join(FIXTURE_DIR,'fixture.json')
    f = open(fixture_file,'w')
    f.write(lines)
    f.close()
    write_logs("Fixture Done\t\t%s" %daily_wrs) 
    return True

if __name__ == '__main__':
    all_wrs = get_daily_wrs_results(RAW_RESULTS_DIR)
    for daily_wrs in all_wrs: 
        serialize(daily_wrs)
    shutil.rmtree(RAW_RESULTS_DIR)
