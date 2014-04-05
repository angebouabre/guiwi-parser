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

def genFixture(output_file, data):
    if not os.path.isfile(output_file):  
        print output_file
        f = open(output_file,'w')
        f.write(data)
        f.close()
        res = True
    else:
        res = False
    return res

class WitbeLogFile(object):
    """ Class of logsTM files """
    def __init__(self, filename):
        
        self.filename = filename #filename's Full path
        self.tag = filename.split('-')[-1].split('.')[0]
        self.error_step = self.getErrorStep()
        self.test_principal = None      #Doit être déclaré avant l'appel de getDependances()
        self.test_is_principal = False  #Doit être déclaré avant l'appel de getDependances()
        self.dependances = self.getDependances()
        self.projet = self.getProjet()
        self.version = self.getVersion()
        self.campagne = self.getCampagne()
        self.scenario = self.getScenario()
        self.theme = self.getTheme()
        self.test = self.getTest()
        self.mesure = self.getMesure() 
        self.resultat = self.checkFile()
        ###########################################
        self.test_name = ""
        self.scenario_failed ="" 
        self.start_time = None
        self.end_time =  None
        self.start_date = None
        self.error_code = self.getErrorCode() 
        self.error_code_scenario = None 
        self.video_report = ""
        self.date_debut = self.getCampagne()
        #######  Get slug  ##############
        self.projet_slug = self.projet #TODO Write get*slug function for each propriete
        self.version_slug = self.version
        self.campagne_slug = ""
        self.scenario_slug = ""
        self.theme_slug = self.getTheme()
        self.test_slug = self.getTest()
        
        self.date_debut_tests = self.getDateDebutTests()
        ####### Get tables fields #######
        #self.projet_fields = self.serialize_projet(1) #TODO Remove hard pk=1 in pamameter and use the method get_last_pk in utils to get lask pk+1 from database
        #self.campagne_fields = self.serialize_campagne(pk_campagne) #TODO Remove hard pk=1 in pamameter and use the method get_last_pk in utils to get lask pk+1 from database
        #self.version_fields = self.serialize_version(1) #TODO Remove hard pk=1 in pamameter and use the method get_last_pk in utils to get lask pk+1 from database
        #self.scenario_fields = self.serialize_scenario(pk_scenario) #TODO Remove hard pk=1 in pamameter and use the method get_last_pk in utils to get lask pk+1 from database
        #self.theme_fields = self.serialize_theme(pk_theme) #TODO Remove hard pk=1 in pamameter and use the method get_last_pk in utils to get lask pk+1 from database
        #self.test_fields = self.serialize_test(pk_test) #TODO Remove hard pk=1 in pamameter and use the method get_last_pk in utils to get lask pk+1 from database
        #self.mesure_fields = self.serialize_mesure(pk_mesure) #TODO Remove hard pk=1 in pamameter and use the method get_last_pk in utils to get lask pk+1 from database
      

    def checkFile(self):
        """ Check succes of task by global return in task report Success = True, Failed = False"""
        res = False 
        if os.path.isfile(self.filename):
            openedFile = open(self.filename)
            for line in openedFile:
                if GLOBAL_RESULT in line:
                    res = True
                    break
        return res             
    
    def getErrorCode(self):
        if os.path.isfile(self.filename):
            openedFile = open(self.filename)
            for line in openedFile:
                if "RETURN=" in line:
                    self.error_code = line.split('=')[1].rstrip()
        return self.error_code            


    def getErrorStep(self):
        """ Return the scenario's step number of failed task in dictionnary"""
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
        """ Get dependances and set principal""" 
        dep = []
        tab = []
        ranks = []
        for filename in os.listdir(os.path.dirname(self.filename)): #< Construit un tableau de dependances en comparant les tags >
            if self.tag in filename:
                dep.append(filename)
        self.shortname = self.filename.split('/')[-1]                
        for item in dep :                                           #< Contruit une table à 2 dimensions avec le numero d'ordre de la dependance et exclue le test courant >
            if item != self.shortname:
                tab.append(item)
                ranks.append([item.split('.')[1],item])
        dep = tab
        my_rank = self.shortname.split('.')[1]
        principale = self.shortname                                 
        for rank in ranks:                                         #< Compare les numeros d'ordre des tests et determine le test principal > 
            if int(rank[0]) > int(my_rank):
                principale = rank[1]
                my_rank = rank[0] 
        self.test_principal = [principale] 
        if self.test_principal[0] == self.shortname:
            self.test_is_principal = True
            self.test_principal = None 
        return dep


    def getProjet(self):
        """ Parse file's full path and get the project name """
        if os.path.isfile(self.filename):
            #openedFile = open(self.filename)
            self.projet = self.filename.split('/')[PROJET_INDEX] 
        return self.projet             

    def getVersion(self):
        """ Parse file's full path and get the version number """
        if os.path.isfile(self.filename):
            #openedFile = open(self.filename)
            self.version = self.filename.split('/')[VERSION_INDEX] 
        return self.version             

    def getCampagne(self):
        if os.path.isfile(self.filename):
            #openedFile = open(self.filename)
            self.campagne = self.filename.split('/')[VERSION_INDEX+1:VERSION_INDEX+4]
            if len(self.campagne[-2]) != 2:
                self.campagne[-2] = '0'+ self.campagne[-2]
            if len(self.campagne[-1]) != 2:
                self.campagne[-1] = '0'+ self.campagne[-1]
            self.campagne = self.campagne[-3]+'-'+self.campagne[-2]+'-'+self.campagne[-1]
        return self.campagne             

    
    def getScenario(self):
        """ Parse file's full path and split to build scneario name"""
        if os.path.isfile(self.filename):
            #openedFile = open(self.filename)
            self.scenario = self.filename.split('_')[SCENARIO_INDEX].lower() 
        return self.scenario + ".txt"             

    
    def getDateDebutTests(self):
        
        openedFile = open(self.filename)
        for line in openedFile:
            if 'DATE=' in line:
                date_debut_tests = line.split('=')[1].rstrip()
                date = re.match(r"(....)(..)(..)(..)(..)(..)", date_debut_tests)
                date_debut_tests = date.groups(0)[0] +'-'+ date.groups(0)[1] +'-'+ date.groups(0)[2] +' '+ date.groups(0)[3] +':'+ date.groups(0)[4] +':'+ date.groups(0)[5]
        return date_debut_tests  
    
    
    def getTheme(self):
        if os.path.isfile(self.filename):
            #openedFile = open(self.filename)
            self.theme = self.filename.split('-')[2]
            if 'TI_Sys' in self.theme:
                self.theme = "Systeme"
            elif 'TI_User_ACCUEIL' in self.theme:
                self.theme = "accueil"
            elif 'TI_User_SETTINGS' in self.theme:
                self.theme = "reglages"
            elif 'TI_User_APPLI' in self.theme:
                self.theme = "applications"
            elif 'TI_User_CPCS' in self.theme:
                self.theme = "canal" 
            elif 'TI_User_DIAG' in self.theme:
                self.theme = "diagnostic"
            elif 'TI_User_EPG' in self.theme:
                self.theme = "epg"
            elif 'TI_User_GOD' in self.theme:
                self.theme = "god"
            elif 'TI_User_MOSAIC' in self.theme:
                self.theme = "mosaic"
            elif 'TI_User_MC' in self.theme:
                self.theme = "media center"
            elif 'TI_User_OPTIONSTV' in self.theme:
                self.theme = "options tv"
            elif 'TI_User_RADIOS' in self.theme:
                self.theme = "radios"
            elif 'TI_User_SEARCH' in self.theme:
                self.theme = "recherche"
            elif 'TI_User_HELP' in self.theme:
                self.theme = "aide"
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

    def getMesure(self):
        if os.path.isfile(self.filename):
            self.mesure = self.filename.split('/')[-1] 
        return self.mesure             


    #TODO REWORK SERIALIZE METHODS TO FACTORISE CODE

    def serialize_projet(self, pk): 
        """ This method generate the projet's fixture file"""
        #I will return True and use this function in the main program
        
        projet_fields = {"fields":{"nom":self.projet, "nbr_versions":None, "date_debut_tests":self.date_debut_tests, "slug": self.projet_slug, "nbr_mesures":None, "nbr_success_mesures":None,"nbr_failed_mesures":None,\
                         "date_debut":self.date_debut, "date_dernier_tests":None}, "model":"stbattack.projet", "pk":pk}

        projet_fields = json.dumps(projet_fields)
        data = '['+ projet_fields +']'
        
        output_file = "fixture/projet_%s.json" %self.projet
        
        res = genFixture(output_file, data)
        return res 

    def serialize_campagne(self, pk):
        """ This method generate the campagne's fixture file"""
        #I will return True and use this function in the main program

        campagne_fields = {"fields":{"date_debut_tests":None, "slug": self.campagne_slug, "nbr_mesures":None, "nbr_success_mesures":None,"nbr_failed_mesures":None,\
                "date_debut":self.date_debut, "date_fin":self.date_debut , "date_dernier_tests":None}, "model":"stbattack.campagne", "pk":pk}

        campagne_fields = json.dumps(campagne_fields)
        data = '['+ campagne_fields +']'
        
        output_file = "fixture/campagne_du_%s.json" %self.campagne
        
        res = genFixture(output_file, data)
        return res 

    def serialize_version(self, pk):
        """ This method generate the version's fixture file"""
        #I will return True and use this function in the main program

        version_fields = {"fields":{"date_debut_tests":self.date_debut_tests, "projet":[self.projet,self.date_debut_tests],"numero":self.version,"slug": self.version_slug, "nbr_mesures":None,\
                "nbr_success_mesures":None,"nbr_failed_mesures":None,"date_debut":self.date_debut, "date_dernier_tests":None}, "model":"stbattack.version", "pk":pk}

        version_fields = json.dumps(version_fields)
        data = '['+ version_fields +']'
        
        output_file = "fixture/version_%s.json" %self.version
        
        res = genFixture(output_file, data)
        return res 
    
    def serialize_scenario(self, pk):
        """ This method generate the scenario's fixture file"""
        #I will return True and use this function in the main program

        scenario_fields = {"fields":{"date_debut_tests":self.date_debut_tests, "nom":self.scenario,"slug": self.scenario_slug, "nbr_mesures":None,\
                "nbr_success_mesures":None,"nbr_failed_mesures":None,"date_debut":self.date_debut, "date_dernier_tests":None}, "model":"stbattack.scenario", "pk":pk}

        scenario_fields = json.dumps(scenario_fields)
        data = '['+ scenario_fields +']'
        
        output_file = "fixture/scenario_%s.json" %self.scenario
        
        res = genFixture(output_file, data)
        return res 
    
   
    def serialize_theme(self, pk):
        """ This method generate the theme's fixture file"""
        #I will return True and use this function in the main program

        theme_fields = {"fields":{"date_debut_tests":self.date_debut_tests, "nom":self.theme,"slug": self.theme_slug, "nbr_mesures":None,\
                "nbr_success_mesures":None,"nbr_failed_mesures":None,"date_debut":self.date_debut, "date_dernier_tests":None}, "model":"stbattack.theme", "pk":pk}

        theme_fields = json.dumps(theme_fields)
        data = '['+ theme_fields +']'
        
        output_file = "fixture/theme_%s.json" %self.theme
        
        res = genFixture(output_file, data)
        return res 

    def serialize_test(self, pk):
        """ This method generate the test's fixture file"""
        #I will return True and use this function in the main program

        test_fields = {"fields":{"date_debut_tests":self.date_debut_tests, "nom":self.test,"slug": self.test_slug, "nbr_mesures":None,"theme":[self.theme],\
                "nbr_success_mesures":None,"nbr_failed_mesures":None,"date_debut":self.date_debut, "date_dernier_tests":None}, "model":"stbattack.test", "pk":pk}

        test_fields = json.dumps(test_fields)
        data = '['+ test_fields +']'
        
        output_file = "fixture/test_%s.json" %self.test
        
        res = genFixture(output_file, data)
        return res 

    
    def serialize_mesure(self, pk):
        """ This method generate the mesure's fixture file"""
        #I will return True and use this function in the main program
        
        openedFile = open(self.filename)
        for line in openedFile:
            
            dico = self.getErrorStep()
            stp_nb = dico['failed_stp']
            self.file_report = self.filename.rstrip()
            
            if 'ALIAS' in line:
                self.test_name = line.split('=')[1].rstrip()
            if 'DL_ACTION_%s'%stp_nb in line:
                self.scenario_failed = line.split('=')[1].rstrip()
            if 'DL_ACTIONSTART_%s'%stp_nb in line:
                self.start_time = line.split('=')[1].rstrip() #Value Not used
            if 'DL_ACTIONEND_%s'%stp_nb in line:
                self.end_time = line.split('=')[1].rstrip() #Value Not used
            if 'DL_ACTIONSTARTDATE_%s'%stp_nb in line:
                self.start_date = line.split('=')[1].rstrip() #Value Not used
            if 'DL_RETURN%s'%stp_nb in line:
                self.error_code_scenario = line.split('=')[1].rstrip()
            if 'capture=video' in line:
                self.video_report = 'https:%s'%(line.split('=https:')[1].rstrip())
        
        if self.resultat == True:
            self.scenario_failed = ""  

        mesure_fields = {"fields":{"nom":self.mesure, "code_erreur":self.error_code,"scenario":[self.scenario],\
                "test":[self.test],"principal":self.test_principal,"resultat_test":self.resultat, "scenario_failed":self.scenario_failed,"date_fin":self.date_debut,"version":[self.version],\
                "is_principal":self.test_is_principal,"video_report":self.video_report, "campagne":[self.date_debut], "file_report":self.filename, "date_debut":self.date_debut}, "model":"stbattack.mesure", "pk":pk}

        mesure_fields = json.dumps(mesure_fields)
        data = '['+ mesure_fields +']'
        
        output_file = "fixture/mesure_%s.json" %self.mesure
        
        res = genFixture(output_file, data)
        return res 

if __name__ == '__main__':
    dossier = '/home/bouable/workspace/project/sfr/neufbox-evol/integration/testi/fusion/13.2.20/2014/3/18/'
    cnt = 0
    print '{:<55}|{:<6}|{:<6}|{:<10}|{:<30}|{:<70}'.format("Nom du test","parent", "Result", " EC ","Scenario echoue", "Filename")
    for fic in os.listdir(dossier):
        fic = os.path.join(dossier,fic)
        f=WitbeLogFile(fic)
        if f.principale == True:
            print '{:<55}|{:<6}|{:<6}|{:<10}|{:<30}|{:<70}'.format(f.test_name,str(f.principale), str(f.resultat), f.error_code,f.scenario_failed, f.shortname)
            cnt += 1
    print cnt
    cnt = 0
    for fic in os.listdir(dossier):
        fic = os.path.join(dossier,fic)
        f=WitbeLogFile(fic)
        if f.principale == False:
            print '{:<55}|{:<6}|{:<6}|{:<10}|{:<30}|{:<70}'.format(f.test_name,str(f.principale), str(f.resultat), f.error_code,f.scenario_failed, f.shortname)
            cnt += 1
    print cnt
