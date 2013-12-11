#!/usr/bin/env python
#-*-encoding:utf-8-*-
""" """

import os
import shutil
import json
from utils import *
from parsersettings import GLOBAL_RESULT, SUCCESS_CODE_1, SUCCESS_CODE_2, FIXTURE_DIR, RAW_RESULTS_DIR

class WitbeLogFile(object):

    def __init__(self, filename):
        self.filename = filename
        
    def checkFile(self):
        """ Check succes of task by global return in task report """
        res = {'result_test':"KO"}
        if os.path.isfile(self.filename):
            openedFile = open(self.filename)
            for line in openedFile:
                if GLOBAL_RESULT in line:
                    res = "OK"
                    break
        return res             
             

    def getErrorStep(self):
        """ Return the scenario's step number of failed task """
        res={}
        openedFile = open(self.filename)
        res = {'failed_stp':'', 'filename':self.filename}
        for line in openedFile:
            key_field = 'DL_RETURN'
            if key_field in line:
                if SUCCESS_CODE_1 in line:
                    pass 
                elif SUCCESS_CODE_2 in line:
                    pass
                else:
                    failed_step = line.split('=')[0].split("N")[1]
                    res = {'failed_stp':failed_step}
        return res               

    def getFields(self, pk):
        """ Get needed fields in task report """
        fields_dict={}
        openedFile = open(self.filename)
        for line in openedFile:
            if 'ALIAS' in line:
                test_name = line.split('=')[1].rstrip()
            if 'DATE' in line: #To rework because it  gets the last occurence 'DATE' in wrs file
                start_date = line.split('=')[1].rstrip()
        try:
            data={"fields":{"scenario_failed":"","error_code":0,"start_date":start_date,"file_report":self.filename,"test_name":test_name},"model":"stbattack.tasktest","pk":pk}
        except NameError:
            data={"fields":{"scenario_failed":"","error_code":0,"start_date":start_date,"file_report":self.filename,"test_name":test_name},"model":"stbattack.tasktest"}

        if self.getErrorStep():
            stp_nb = self.getErrorStep()['failed_stp']
            fields_dict['file_report'] = self.filename.rstrip()
            openedFile = open(self.filename)
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
        return data 


class WitbeDailyFolder(object):
    
    def __init__(self, dirname):
        self.dirname = dirname
    
    def serialize(self):
        lines = '' 
        pk = 0 
        for filename in os.listdir(self.dirname):
            filename = os.path.join(self.dirname, filename)
            if os.path.isfile(filename):
                pk += 1
                filelog = WitbeLogFile(filename)
                line = filelog.getFields(pk)
                lines = str(line) + ',' + lines
                #os.remove(filename)
                print "%s deleted."%self.dirname
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
        write_logs("Fixture Done\t\t%s" %self.dirname) 
        return True

if __name__ == '__main__':
    all_wrs = get_daily_wrs_results(RAW_RESULTS_DIR)
    for daily_wrs in all_wrs: 
        daily_wrs = WitbeDailyFolder(daily_wrs)
        daily_wrs.serialize()
    shutil.rmtree(RAW_RESULTS_DIR)
