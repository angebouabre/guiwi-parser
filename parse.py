from parser import *
import os
import shutil
    
    
dossier = '/home/bouable/workspace/project/sfr/neufbox-evol/integration/testi/fusion/14.1.2/2014/4/13/'

#TODO Get the last pk in database fo fill these initials values
pk_scenario = 1
pk_version = 2
pk_theme = 1
pk_test = 1
pk_campagne = 15 
pk_mesure = 9150  

for fic in os.listdir(dossier):
    fic = os.path.join(dossier,fic)
    f = WitbeLogFile(fic)
    res_campagne = f.serialize_campagne(pk_campagne)
    res_version = f.serialize_version(pk_version)
    if res_campagne == True:
        pk_campagne += 1
    res_scenario = f.serialize_scenario(pk_scenario)
    if res_scenario == True:
        pk_scenario += 1
    res_theme = f.serialize_theme(pk_theme)
    if res_theme == True:
        pk_theme += 1
    res_test = f.serialize_test(pk_test)
    if res_test == True:
        pk_test += 1
    res_mesure = f.serialize_mesure(pk_mesure)
    if res_mesure == True:
        pk_mesure += 1 
try:
    os.makedirs('fixture/todo')
except:
    pass
#shutill.rmtree()
#os.makedirs(fixture)
