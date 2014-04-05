from parser import *
import os
import shutil
    
    
dossier = '/home/bouable/sfr-workspace/fusion/13.2.20/2014/3/31'

pk_scenario = 1
pk_theme = 1
pk_test = 1
pk_campagne = 15 
pk_mesure = 2003  

tab_campagne = []
tab_scenario = []
tab_theme = []
tab_test = []
tab_mesure = []

for fic in os.listdir(dossier):
    fic = os.path.join(dossier,fic)
    f = WitbeLogFile(fic)
    res_campagne = f.serialize_campagne(pk_campagne)
    if res_campagne == True:
        pk_campagne += 1
        tab_campagne.append(pk_campagne)
    res_scenario = f.serialize_scenario(pk_scenario)
    if res_scenario == True:
        pk_scenario += 1
        tab_scenario.append(pk_scenario)
    res_theme = f.serialize_theme(pk_theme)
    if res_theme == True:
        pk_theme += 1
        tab_theme.append(pk_theme)
    res_test = f.serialize_test(pk_test)
    if res_test == True:
        pk_test += 1
        tab_test.append(pk_test)
    res_mesure = f.serialize_mesure(pk_mesure)
    if res_mesure == True:
        pk_mesure += 1 
        tab_mesure.append(pk_mesure)

print tab_campagne
print tab_scenario
print tab_theme
print tab_test
print tab_mesure


#shutill.rmtree()
#os.makedirs(fixture)
#os.makedirs(fixture+'/principal')
