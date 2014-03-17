#!/usr/bin/env python
#-*-encoding:utf-8-*-
""" """

import os
import re 
import shutil
import json
import time
from utils import *
from parsersettings import *

#TODO Use re to parse some expressions

class WitbeLogFile(object):
    """ Class of logsTM files """
    def __init__(self, filename):
        self.filename = filename
        self.tag = filename.split('-')[-1].split('.')[0]
        self.error_step = self.getErrorStep()
        self.dependances = self.getDependances()
        self.projet = self.getProjet()
        self.version = self.getVersion()
        self.scenario = self.getScenario()
        self.theme = self.getTheme()
        self.test = self.getTest()
        self.projet_slug = self.projet #TODO Write get*slug function for each propriete
        self.version_slug = self.version
        self.campagne_slug = ""
        self.scenario_slug = ""
        self.theme_slug = self.getTheme()
        self.test_slug = self.getTest()
        self.projet_fields = self.serialize_projet(1) #TODO Remove hard pk=1 in pamameter and use the method get_last_pk in utils to get lask pk+1 from database
        self.campagne_fields = self.serialize_campagne(1) #TODO Remove hard pk=1 in pamameter and use the method get_last_pk in utils to get lask pk+1 from database
        self.version_fields = self.serialize_version(1) #TODO Remove hard pk=1 in pamameter and use the method get_last_pk in utils to get lask pk+1 from database
        self.scenario_fields = self.serialize_scenario(1) #TODO Remove hard pk=1 in pamameter and use the method get_last_pk in utils to get lask pk+1 from database
        self.theme_fields = self.serialize_theme(1) #TODO Remove hard pk=1 in pamameter and use the method get_last_pk in utils to get lask pk+1 from database
        self.test_fields = self.serialize_test(1) #TODO Remove hard pk=1 in pamameter and use the method get_last_pk in utils to get lask pk+1 from database

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
        res={'failed_stp':None}
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

    def getDependances(self):
        dep = []
        for filename in os.listdir(os.path.dirname(self.filename)):
            if self.tag in filename:
                dep.append(filename)
        return dep

    def getProjet(self):
        if os.path.isfile(self.filename):
            #openedFile = open(self.filename)
            self.projet = self.filename.split('/')[PROJET_INDEX] 
        return self.projet             

    def getVersion(self):
        if os.path.isfile(self.filename):
            #openedFile = open(self.filename)
            self.version = self.filename.split('/')[VERSION_INDEX] 
        return self.version             

    def getScenario(self):
        if os.path.isfile(self.filename):
            #openedFile = open(self.filename)
            self.scenario = self.filename.split('_')[SCENARIO_INDEX] 
        return "scenario" + self.scenario + ".txt"             

    def getTheme(self):
        if os.path.isfile(self.filename):
            #openedFile = open(self.filename)
            self.theme = self.filename.split('-')[2]
            if 'TI_Sys' in self.theme:
                self.theme = "Systeme"
            elif 'TI_User_APPLI' in self.theme:
                self.theme = "Applications"
            elif 'TI_User_CPCS' in self.theme:
                self.theme = "Canal Plus - Canal Sat" 
            elif 'TI_User_DIAG' in self.theme:
                self.theme = "DIAG"
            elif 'TI_User_EPG' in self.theme:
                self.theme = "EPG"
            elif 'TI_User_GOD' in self.theme:
                self.theme = "GOD"
            elif 'TI_User_MOSAIC' in self.theme:
                self.theme = "MODAIC"
            elif 'TI_User_MC' in self.theme:
                self.theme = "MEDIA CENTER"
            elif 'TI_User_OPTIONSTV' in self.theme:
                self.theme = "OPTIONS TV"
            elif 'TI_User_RADIOS' in self.theme:
                self.theme = "RADIOS"
            elif 'TI_User_SEARCH' in self.theme:
                self.theme = "RECHERCHE"
            elif 'TI_User_HELP' in self.theme:
                self.theme = "AIDE"
            elif 'TI_User_PVR' in self.theme:
                self.theme = "PVR"
            elif 'TI_User_TNT' in self.theme:
                self.theme = "TNT"
            elif 'TI_User_TV' in self.theme:
                self.theme = "Television"
            elif 'TI_User_VOD' in self.theme:
                self.theme = "VOD"
        self.theme = self.theme.lower()
        return self.theme.lower()           

    def getTest(self):
        if os.path.isfile(self.filename):
            openedFile = open(self.filename)
            for line in openedFile:
                if 'ALIAS' in line:
                    self.test = line.split('=')[1].rstrip()
        return self.test             


    #TODO REWORK SERIALIZE METHODS TO FACTORISE CODE

    def serialize_projet(self, pk): 
        
        fields_dict={}
        openedFile = open(self.filename)
        for line in openedFile:
            if 'DATE=' in line:
                date_debut_tests = line.split('=')[1].rstrip()
                date = re.match(r"(....)(..)(..)(..)(..)(..)", date_debut_tests)
                date_debut_tests = date.groups(0)[0] +'-'+ date.groups(0)[1] +'-'+ date.groups(0)[2] +' '+ date.groups(0)[3] +':'+ date.groups(0)[4] +':'+ date.groups(0)[5]
            if 'DATE' in line: #TODO rework because it  gets the last occurence 'DATE' in wrs file
                date_debut = line.split('=')[1].rstrip()

        projet_fields = {"fields":{"nom":self.projet, "nbr_versions":None, "date_debut_tests":date_debut_tests, "slug": self.projet_slug, "nbr_mesures":None, "nbr_success_mesures":None,"nbr_failed_mesures":None,\
                         "date_debut":date_debut, "date_dernier_tests":None}, "model":"stbattack.projet", "pk":pk}

        projet_fields = json.dumps(projet_fields)
        data = '['+ projet_fields +']'
        
        f = open('fixture/projet.json','w')
        f.write(data)
        f.close()
        
        return data 

    def serialize_campagne(self, pk):

        fields_dict={}
        openedFile = open(self.filename)
        for line in openedFile:
            if 'DATE=' in line:
                date_debut_tests = line.split('=')[1].rstrip()
                date = re.match(r"(....)(..)(..)(..)(..)(..)", date_debut_tests)
                date_debut_tests = date.groups(0)[0] +'-'+ date.groups(0)[1] +'-'+ date.groups(0)[2] +' '+ date.groups(0)[3] +':'+ date.groups(0)[4] +':'+ date.groups(0)[5]
            if 'DATE' in line: #TODO rework because it  gets the last occurence 'DATE' in wrs file
                date_debut = line.split('=')[1].rstrip()

        campagne_fields = {"fields":{"date_debut_tests":date_debut_tests, "slug": self.campagne_slug, "nbr_mesures":None, "nbr_success_mesures":None,"nbr_failed_mesures":None,\
                "date_debut":date_debut, "date_fin":date_debut , "date_dernier_tests":None}, "model":"stbattack.campagne", "pk":pk}

        campagne_fields = json.dumps(campagne_fields)
        data = '['+ campagne_fields +']'
        
        f = open('fixture/campagne.json','w')
        f.write(data)
        f.close()
        
        return data 

    def serialize_version(self, pk):

        fields_dict={}
        openedFile = open(self.filename)
        for line in openedFile:
            if 'DATE=' in line:
                date_debut_tests = line.split('=')[1].rstrip()
                date = re.match(r"(....)(..)(..)(..)(..)(..)", date_debut_tests)
                date_debut_tests = date.groups(0)[0] +'-'+ date.groups(0)[1] +'-'+ date.groups(0)[2] +' '+ date.groups(0)[3] +':'+ date.groups(0)[4] +':'+ date.groups(0)[5]
            if 'DATE' in line: #TODO rework because it  gets the last occurence 'DATE' in wrs file
                date_debut = line.split('=')[1].rstrip()

        version_fields = {"fields":{"date_debut_tests":date_debut_tests, "projet":[self.projet,date_debut_tests],"numero":self.version,"slug": self.version_slug, "nbr_mesures":None,\
                "nbr_success_mesures":None,"nbr_failed_mesures":None,"date_debut":date_debut, "date_dernier_tests":None}, "model":"stbattack.version", "pk":pk}

        version_fields = json.dumps(version_fields)
        data = '['+ version_fields +']'
        
        f = open('fixture/version.json','w')
        f.write(data)
        f.close()
        
        return data 
    
    def serialize_scenario(self, pk):

        fields_dict={}
        openedFile = open(self.filename)
        for line in openedFile:
            if 'DATE=' in line:
                date_debut_tests = line.split('=')[1].rstrip()
                date = re.match(r"(....)(..)(..)(..)(..)(..)", date_debut_tests)
                date_debut_tests = date.groups(0)[0] +'-'+ date.groups(0)[1] +'-'+ date.groups(0)[2] +' '+ date.groups(0)[3] +':'+ date.groups(0)[4] +':'+ date.groups(0)[5]
            if 'DATE' in line: #TODO rework because it  gets the last occurence 'DATE' in wrs file
                date_debut = line.split('=')[1].rstrip()

        scenario_fields = {"fields":{"date_debut_tests":date_debut_tests, "nom":self.scenario,"slug": self.scenario_slug, "nbr_mesures":None,\
                "nbr_success_mesures":None,"nbr_failed_mesures":None,"date_debut":date_debut, "date_dernier_tests":None}, "model":"stbattack.scenario", "pk":pk}

        scenario_fields = json.dumps(scenario_fields)
        data = '['+ scenario_fields +']'
        
        f = open('fixture/scenario.json','w')
        f.write(data)
        f.close()
        
        return data 
    
   
    def serialize_theme(self, pk):

        fields_dict={}
        openedFile = open(self.filename)
        for line in openedFile:
            if 'DATE=' in line:
                date_debut_tests = line.split('=')[1].rstrip()
                date = re.match(r"(....)(..)(..)(..)(..)(..)", date_debut_tests)
                date_debut_tests = date.groups(0)[0] +'-'+ date.groups(0)[1] +'-'+ date.groups(0)[2] +' '+ date.groups(0)[3] +':'+ date.groups(0)[4] +':'+ date.groups(0)[5]
            if 'DATE' in line: #TODO rework because it  gets the last occurence 'DATE' in wrs file
                date_debut = line.split('=')[1].rstrip()

        theme_fields = {"fields":{"date_debut_tests":date_debut_tests, "nom":self.theme,"slug": self.theme_slug, "nbr_mesures":None,\
                "nbr_success_mesures":None,"nbr_failed_mesures":None,"date_debut":date_debut, "date_dernier_tests":None}, "model":"stbattack.theme", "pk":pk}

        theme_fields = json.dumps(theme_fields)
        data = '['+ theme_fields +']'
        
        f = open('fixture/theme.json','w')
        f.write(data)
        f.close()
        
        return data 

    def serialize_test(self, pk):

        fields_dict={}
        openedFile = open(self.filename)
        for line in openedFile:
            if 'DATE=' in line:
                date_debut_tests = line.split('=')[1].rstrip()
                date = re.match(r"(....)(..)(..)(..)(..)(..)", date_debut_tests)
                date_debut_tests = date.groups(0)[0] +'-'+ date.groups(0)[1] +'-'+ date.groups(0)[2] +' '+ date.groups(0)[3] +':'+ date.groups(0)[4] +':'+ date.groups(0)[5]
            if 'DATE' in line: #TODO rework because it  gets the last occurence 'DATE' in wrs file
                date_debut = line.split('=')[1].rstrip()

        test_fields = {"fields":{"date_debut_tests":date_debut_tests, "nom":self.test,"slug": self.test_slug, "nbr_mesures":None,"theme":[self.theme],\
                "nbr_success_mesures":None,"nbr_failed_mesures":None,"date_debut":date_debut, "date_dernier_tests":None}, "model":"stbattack.test", "pk":pk}

        test_fields = json.dumps(test_fields)
        data = '['+ test_fields +']'
        
        f = open('fixture/test.json','w')
        f.write(data)
        f.close()
        
        return data 

    def getFields(self, pk):
        """ Get needed fields in task report """
        fields_dict={}
        openedFile = open(self.filename)
        for line in openedFile:
            if 'ALIAS' in line:
                test_name = line.split('=')[1].rstrip()
            if 'DATE' in line: #TODO rework because it  gets the last occurence 'DATE' in wrs file
                start_date = line.split('=')[1].rstrip()
        try:
            data={"fields":{"scenario_failed":"","error_code":0,"start_date":start_date,"file_report":self.filename,"test_name":test_name},"model":"stbattack.tasktest","pk":pk}
        except NameError:
            data={"fields":{"scenario_failed":"","error_code":0,"start_date":start_date,"file_report":self.filename,"test_name":test_name},"model":"stbattack.tasktest"}

        if self.getErrorStep()['failed_stp']:
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
    """ Class of daily logs TM folder """
    def __init__(self, dirname):
        self.dirname = dirname
    
    def serialize(self):
        lines = '' 
        #time.sleep(10)
        pk = get_last_pk(DATABASE) 
        print pk
        for filename in os.listdir(self.dirname):
            filename = os.path.join(self.dirname, filename)
            if os.path.isfile(filename):
                pk += 1
                filelog = WitbeLogFile(filename)
                line = filelog.getFields(pk)
                lines = str(line) + ',' + lines
                #os.remove(filename)
                #print "%s deleted."%self.dirname
        "Making a table with the json data like django fixture"
        lines = '['+lines+']'
        "SERIALIZING: Clean the the table in compliance with django fixture "
        lines = lines.replace("},]","}]").replace(",{}","").replace("{},","")
        
        if not os.path.isdir(FIXTURE_DIR):
            os.makedirs(FIXTURE_DIR)
        nm = str(self.dirname.split('/')[5:]).replace("['","").replace("']","").replace("', '","-")
        fixture_file = os.path.join(FIXTURE_DIR,'fixtures-%s.json' %nm)
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
