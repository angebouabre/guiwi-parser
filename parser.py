#!/usr/bin/env python

import os
import json
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
        if 'DATE' in line:
            start_date = line.split('=')[1].rstrip()
    data={"fields":{"scenario_failed":"","error_code":0,"start_date":start_date,"file_report":filename,"test_name":test_name},"model":"stbattack.tasktest","pk":pk}
    if getErrorStep(filename):
        stp_nb = getErrorStep(filename)['failed_stp']
        fields_dict['file_report'] = getErrorStep(filename)['filename'].rstrip()
        fields_dict['test_name'] = filename.split('-')[1].split('.')[0].rstrip()
        openedFile = open(filename)
        for line in openedFile:
            if 'DL_ACTION_%s'%stp_nb in line:
                fields_dict['scenario_failed'] = line.split('=')[1].rstrip()
            elif 'DL_ACTIONSTART_%s'%stp_nb in line:
                fields_dict['start_time'] = line.split('=')[1].rstrip()
            elif 'DL_ACTIONEND_%s'%stp_nb in line:
                fields_dict['end_time'] = line.split('=')[1].rstrip()
            elif 'DL_ACTIONSTARTDATE_%s'%stp_nb in line:
                fields_dict['start_date'] = line.split('=')[1].rstrip()
            elif 'DL_RETURN%s'%stp_nb in line:
                fields_dict['error_code'] = int(line.split('=')[1].rstrip())
            elif 'capture=video' in line:
                fields_dict['video_report'] = 'https:%s'%(line.split('=https:')[1].rstrip())
        data['fields']=fields_dict
    data = json.dumps(data)
    #else:
        # Get all results ( success tests too)
    return str(data) 

def call(DIR):
    lines = '' 
    pk = 0 
    for filename in os.listdir(DIR):
        filename = os.path.join(DIR,filename)
        if os.path.isfile(filename):
            pk += 1
            res = checkFile(filename)      
            line = getFields(filename, pk)
            lines = line + ',' + lines
            #lines = json.dumps(lines)
    lines = '['+lines+']'
    lines = lines.replace("},]","}]")
    lines = lines.replace(",{}","")
    lines = lines.replace("{},","")
    CUR_DIR = os.path.dirname(__file__)
    folder_fixture_path = os.path.join(CUR_DIR,FIXTURE_DIR)
    if not os.path.isdir(folder_fixture_path):
        os.makedirs(folder_fixture_path)
    fixture_path = os.path.join(CUR_DIR, FIXTURE_DIR,'fixture.json')
    f = open(fixture_path,'w')
    f.write(lines)
    f.close()


DIR=os.path.join(os.path.dirname(__file__),os.pardir,RAW_RESULTS_DIR)
call(DIR)
